#!/usr/bin/env python3
"""
A simple microservice that consumes messages from Google Cloud Pub/Sub
and outputs them to Google Cloud Storage bucket. :)
"""

import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from google.cloud import pubsub_v1
from google.cloud import storage
from google.api_core import retry


# Configure logging for better observability :)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PubSubToGCSMicroservice:
    """
    Microservice that processes Pub/Sub messages and stores them in GCS :)
    """
    
    def __init__(self):
        """Initialize the microservice with environment variables :)"""
        # Get configuration from environment variables :)
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.subscription_name = os.getenv('PUBSUB_SUBSCRIPTION')
        self.bucket_name = os.getenv('GCS_BUCKET_NAME')
        self.max_messages = int(os.getenv('MAX_MESSAGES', '10'))
        self.ack_deadline = int(os.getenv('ACK_DEADLINE_SECONDS', '60'))
        
        # Validate required environment variables :)
        self._validate_config()
        
        # Initialize Google Cloud clients :)
        self.subscriber = pubsub_v1.SubscriberClient()
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)
        
        # Create subscription path :)
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, self.subscription_name
        )
        
        logger.info(f"Microservice initialized for project: {self.project_id} :)")
    
    def _validate_config(self):
        """Validate that all required environment variables are set :)"""
        required_vars = {
            'GOOGLE_CLOUD_PROJECT': self.project_id,
            'PUBSUB_SUBSCRIPTION': self.subscription_name,
            'GCS_BUCKET_NAME': self.bucket_name
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            error_msg = f"Missing required environment variables: {missing_vars} :("
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def process_message(self, message):
        """
        Process a single Pub/Sub message and store it in GCS :)
        
        Args:
            message: The Pub/Sub message to process
        """
        try:
            # Decode message data :)
            message_data = message.data.decode('utf-8')
            message_id = message.message_id
            
            logger.info(f"Processing message {message_id} :)")
            
            # Create a unique filename for the message :)
            filename = f"messages/{message_id}.json"
            
            # Prepare message payload :)
            payload = {
                'message_id': message_id,
                'data': message_data,
                'attributes': dict(message.attributes),
                'publish_time': message.publish_time.isoformat(),
                'processed_at': self._get_current_timestamp()
            }
            
            # Upload to GCS bucket :)
            blob = self.bucket.blob(filename)
            blob.upload_from_string(
                json.dumps(payload, indent=2),
                content_type='application/json'
            )
            
            logger.info(f"Successfully uploaded message {message_id} to GCS :)")
            
            # Acknowledge the message after successful processing :)
            message.ack()
            logger.info(f"Message {message_id} acknowledged :)")
            
        except Exception as e:
            logger.error(f"Failed to process message {message.message_id}: {e} :(")
            # Don't acknowledge failed messages so they can be retried :)
            message.nack()
    
    def _get_current_timestamp(self):
        """Get current timestamp in ISO format :)"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    def callback(self, message):
        """
        Callback function for Pub/Sub message processing :)
        
        Args:
            message: The received Pub/Sub message
        """
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.process_message, message)
    
    def start_listening(self):
        """
        Start listening for messages from Pub/Sub subscription :)
        """
        logger.info(f"Starting to listen for messages on {self.subscription_path} :)")
        
        # Configure the subscriber :)
        flow_control = pubsub_v1.types.FlowControl(max_messages=self.max_messages)
        
        try:
            # Start pulling messages :)
            streaming_pull_future = self.subscriber.pull(
                request={
                    "subscription": self.subscription_path,
                    "max_messages": self.max_messages,
                },
                callback=self.callback,
                flow_control=flow_control,
            )
            
            logger.info(f"Listening for messages... :)")
            
            # Keep the main thread running :)
            try:
                streaming_pull_future.result()
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down gracefully :)")
                streaming_pull_future.cancel()
                
        except Exception as e:
            logger.error(f"Error in message listener: {e} :(")
            raise
    
    def health_check(self):
        """
        Simple health check to verify service connectivity :)
        
        Returns:
            bool: True if service is healthy, False otherwise
        """
        try:
            # Check if we can access the subscription :)
            self.subscriber.get_subscription(request={"subscription": self.subscription_path})
            
            # Check if we can access the GCS bucket :)
            self.bucket.exists()
            
            logger.info("Health check passed :)")
            return True
            
        except Exception as e:
            logger.error(f"Health check failed: {e} :(")
            return False


def main():
    """
    Main entry point for the microservice :)
    """
    try:
        # Create and start the microservice :)
        microservice = PubSubToGCSMicroservice()
        
        # Perform health check before starting :)
        if not microservice.health_check():
            logger.error("Health check failed, exiting :(")
            return 1
        
        # Start listening for messages :)
        microservice.start_listening()
        
    except Exception as e:
        logger.error(f"Failed to start microservice: {e} :(")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())