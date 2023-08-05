def manage_pods(replicas, docker_image, name_pod, cpu_limits, cpu_request, namespace_pod):
    config.load_kube_config()
    apps_api = client.AppsV1Api()
    deployment = client.V1Deployment()
    deployment.api_version = "apps/v1"
    deployment.kind = "Deployment"
    deployment.metadata = client.V1ObjectMeta(name=name_pod)
    spec = client.V1DeploymentSpec(
        selector=client.V1LabelSelector(match_labels={"app":name_pod}),
        template=client.V1PodTemplateSpec(),
    )
    container = client.V1Container(
        image=docker_image,
        resources = {"limits": {"cpu":cpu_limits} , "requests": {"cpu":cpu_request}},
        name=name_pod, 
    )
    spec.template.metadata = client.V1ObjectMeta(
        name=name_pod,
        labels={"app":name_pod},
    )
    spec.template.spec = client.V1PodSpec(containers = [container])
    dep = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name_pod),
        spec=spec,
    )
    dep.spec.replicas = replicas
    try:
        apps_api.create_namespaced_deployment(namespace=namespace_pod, body=dep)
    except:
        print("Pod Exist, updating replicas")    
    dep.spec.replicas = replicas
    changeddeploy= apps_api.replace_namespaced_deployment(name=name_pod, namespace=namespace_pod, body=dep)