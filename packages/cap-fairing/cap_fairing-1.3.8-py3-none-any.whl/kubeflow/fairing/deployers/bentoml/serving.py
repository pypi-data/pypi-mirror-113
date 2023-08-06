import json

import logging

from kubeflow.fairing import utils
from kubernetes import client as k8s_client
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)

BENTOML_DEFAULT_PORT = 5000
CURRENT_NAMESPACE = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"


class BentomlServing(object):
    """Serves a bentoml server using Kubernetes deployments and services"""

    def __init__(self, serving_image=None, service_type="LoadBalancer",
                 service_name="bentoml-serving", service_tag="0.0.1",
                 replicas=1, namespace=None, port=BENTOML_DEFAULT_PORT):
        """
        :param serving_image: bentoml serving container image
        :param service_type: service type default LoadBalancer
        :param service_name: service name
        :param service_tag: serving model version
        :param namespace: user's namespace
        :param replicas: server replicas amount
        :param port: serving container port
        """
        self.service_name = utils.get_service_name(service_name)
        self.service_tag = service_tag
        self.serving_image = serving_image
        self.service_type = service_type
        self.port = port
        self.replicas = replicas
        if namespace is None:
            namespace = open(CURRENT_NAMESPACE).read()
        self.namespace = namespace
        self.labels = {}
        self.annotations = {}
        self.api_client = k8s_client.ApiClient(utils.get_kubernetes_config_on_pod())

    def deploy(self):
        """deploy a bentoml Server service
        """
        self.labels['fairing-id'] = self.service_tag
        self.labels[self.service_name] = self.service_tag
        pod_spec = self.generate_pod_spec()
        pod_template_spec = self.generate_pod_template_spec(pod_spec)
        deployment_spec = self.generate_deployment_spec(pod_template_spec)
        service_spec = self.generate_service_spec()

        job_output = self.api_client.sanitize_for_serialization(deployment_spec)
        logger.warning(json.dumps(job_output))
        service_output = self.api_client.sanitize_for_serialization(service_spec)
        logger.warning(json.dumps(service_output))

        v1_api = k8s_client.CoreV1Api(self.api_client)
        apps_v1 = k8s_client.AppsV1Api(self.api_client)
        self.deployment = apps_v1.create_namespaced_deployment(self.namespace, deployment_spec)
        self.service = v1_api.create_namespaced_service(self.namespace, service_spec)
        logger.info(self.service)

        service_result = self.api_client.sanitize_for_serialization(self.service)
        port = service_result["spec"]["ports"][0]["nodePort"]
        logging.info("=================================")
        logging.info(f"Serving server AccessPort: {port}")
        logging.info("=================================")
        return port

    def generate_pod_spec(self):
        return k8s_client.V1PodSpec(
            containers=[k8s_client.V1Container(
                name=self.service_name,
                image=self.serving_image,
                security_context=k8s_client.V1SecurityContext(
                    run_as_user=0,
                ),
                ports=[k8s_client.V1ContainerPort(
                    container_port=self.port)
                ],
                env=[k8s_client.V1EnvVar(
                    name='FAIRING_RUNTIME',
                    value='1',
                ),
                ],
            )],
        )

    def generate_pod_template_spec(self, pod_spec):
        """Generate a V1PodTemplateSpec initiazlied with correct metadata
            and with the provided pod_spec

        :param pod_spec: pod spec

        """
        if not isinstance(pod_spec, k8s_client.V1PodSpec):
            raise TypeError('pod_spec must be a V1PodSpec, but got %s'
                            % type(pod_spec))
        if not self.annotations:
            self.annotations = {'sidecar.istio.io/inject': 'false'}
        else:
            self.annotations['sidecar.istio.io/inject'] = 'false'
        self.annotations["prometheus.io/scrape"] = 'true'
        self.annotations["prometheus.io/port"] = str(BENTOML_DEFAULT_PORT)

        return k8s_client.V1PodTemplateSpec(
            metadata=k8s_client.V1ObjectMeta(name=self.service_name,
                                             annotations=self.annotations,
                                             labels=self.labels),
            spec=pod_spec)

    def generate_deployment_spec(self, pod_template_spec):
        """generate deployment spec(V1Deployment)

        :param pod_template_spec: pod spec template

        """
        return k8s_client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=k8s_client.V1ObjectMeta(
                name=self.service_name,
                labels=self.labels,
            ),
            spec=k8s_client.V1DeploymentSpec(
                replicas=self.replicas,
                selector=k8s_client.V1LabelSelector(
                    match_labels=self.labels,
                ),
                template=pod_template_spec,
            )
        )

    def generate_service_spec(self):
        """ generate service spec(V1ServiceSpec)"""
        return k8s_client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=k8s_client.V1ObjectMeta(
                name=self.service_name,
                labels=self.labels,
            ),
            spec=k8s_client.V1ServiceSpec(
                selector=self.labels,
                ports=[k8s_client.V1ServicePort(
                    name="serving",
                    port=BENTOML_DEFAULT_PORT
                )],
                type=self.service_type,
            )
        )

    def delete(self):
        """ delete the deployed service"""
        v1_api = k8s_client.CoreV1Api(self.api_client)
        try:
            v1_api.delete_namespaced_service(self.service.metadata.name,  # pylint:disable=no-value-for-parameter
                                             self.service.metadata.namespace)
            logger.info("Deleted service: {}/{}".format(self.service.metadata.namespace,
                                                        self.service.metadata.name))
        except ApiException as e:
            logger.error(e)
            logger.error("Not able to delete service: {}/{}".format(self.service.metadata.namespace,
                                                                    self.service.metadata.name))
        try:
            api_instance = k8s_client.ExtensionsV1beta1Api()
            del_opts = k8s_client.V1DeleteOptions(propagation_policy="Foreground")
            api_instance.delete_namespaced_deployment(self.deployment.metadata.name,
                                                      self.deployment.metadata.namespace,
                                                      body=del_opts)
            logger.info("Deleted deployment: {}/{}".format(self.deployment.metadata.namespace,
                                                           self.deployment.metadata.name))
        except ApiException as e:
            logger.error(e)
            logger.error("Not able to delete deployment: {}/{}" \
                         .format(self.deployment.metadata.namespace, self.deployment.metadata.name))
