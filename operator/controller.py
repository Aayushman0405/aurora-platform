import time
from kubernetes import client, watch
from operator.training_job import create_training_job
from operator.status import update_status

GROUP = "aurora.io"
VERSION = "v1alpha1"
PLURAL = "mltrainingjobs"


def run_controller():
    api = client.CustomObjectsApi()
    w = watch.Watch()

    print("🚀 AURORA MLTrainingJob controller started")

    for event in w.stream(
        api.list_cluster_custom_object,
        group=GROUP,
        version=VERSION,
        plural=PLURAL,
        timeout_seconds=0
    ):
        obj = event["object"]
        event_type = event["type"]

        name = obj["metadata"]["name"]
        namespace = obj["metadata"]["namespace"]

        if event_type == "ADDED":
            print(f"📌 New MLTrainingJob detected: {name}")

            create_training_job(obj)
            update_status(obj, phase="Running")
