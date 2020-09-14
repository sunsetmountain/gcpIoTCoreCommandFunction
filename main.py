import base64
import logging
import json
import datetime
from google.auth import compute_engine
from apiclient import discovery
from google.cloud import iot_v1

def handle_notification(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    logging.info('Command info: {}'.format(pubsub_message))
    projectID = "put project id here"
    cloudRegion = "put cloud region here"
    registryID = "put registry name here"
    deviceID = "put device id here"
    commandResponse = send_command(pubsub_message, projectID, cloudRegion, registryID, deviceID)
    logging.info('Response: {}'.format(commandResponse))

def send_command(command, project_id, cloud_region, registry_id, device_id):
     # from https://cloud.google.com/iot/docs/how-tos/devices#api
     print("Sending command to device")
     client = iot_v1.DeviceManagerClient()
     device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

     #command = 'Hello IoT Core from Cloud Functions!'
     data = command.encode("utf-8")

     return client.send_command_to_device(device_path, data)
