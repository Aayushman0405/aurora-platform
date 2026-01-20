from kubernetes import client


def create_training_job(cr):
    batch = client.BatchV1Api()

    name = cr["metadata"]["name"]
    namespace = cr["metadata"]["namespace"]
    spec = cr["spec"]

    job_name = f"train-{name}"

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            backoff_limit=0,
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[
                        client.V1Container(
                            name="trainer",
                            image="python:3.10-slim",
                            command=["python", "-c"],
                            args=[
                                f"""
print("Training model: {spec['modelName']}")
print("Dataset: {spec['dataset']}")
print("Algorithm: {spec['algorithm']}")
"""
                            ],
                        )
                    ],
                )
            ),
        ),
    )

    batch.create_namespaced_job(namespace=namespace, body=job)
    print(f"✅ Created Job {job_name} in {namespace}")
