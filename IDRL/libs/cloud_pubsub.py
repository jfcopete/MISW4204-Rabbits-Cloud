from google.cloud import pubsub_v1
from libs import traer_configuraciones
import os
import json

from functools import lru_cache

class CloudPubSub:

    def __init__(self):
        self.credentials = os.environ.get("CREDENTIAL_FILE_PUBSUB")
        self.topic_name = os.environ.get("PUBSUB_TOPIC_NAME")
        self.subscription_name = os.environ.get("PUBSUB_SUBSCRIPTION_NAME")

        credentials_dict = json.loads(self.credentials)
        self.publisher = pubsub_v1.PublisherClient.from_service_account_info(credentials_dict)
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_info(credentials_dict)
        self.project_id = self.get_project_id_from_credentials(credentials_dict)

    def get_project_id_from_credentials(self, credentials_dict):
        return credentials_dict['project_id']

    def publish_message(self, message_data):
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        future = self.publisher.publish(topic_path, data=message_data)
        future.result()


    def subscribe_to_messages(self, callback):
        subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_name)
        def message_handler(message):
            callback(message.data.decode('utf-8'))
            message.ack()

        self.subscriber.subscribe(subscription_path, callback=message_handler)

@lru_cache
def get_pubsub_instance():
    return CloudPubSub()