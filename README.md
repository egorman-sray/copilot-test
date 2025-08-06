# Pub/Sub to GCS Microservice :)

A Python microservice that consumes messages from Google Cloud Pub/Sub and stores them in Google Cloud Storage buckets.

## Overview :)

This microservice provides a simple and reliable way to:
- Listen for messages from a Google Cloud Pub/Sub subscription
- Process and transform messages with metadata
- Store processed messages as JSON files in Google Cloud Storage
- Handle errors gracefully with proper logging and retry mechanisms

## Features :)

- **Environment-based configuration**: All secrets and settings via environment variables
- **Concurrent processing**: Efficient message handling with thread pools
- **Error handling**: Proper message acknowledgment and retry logic
- **Health checks**: Built-in connectivity verification
- **Structured logging**: Comprehensive logging for monitoring and debugging
- **Graceful shutdown**: Clean service termination on interrupt signals

## Prerequisites :)

- Python 3.8+
- Google Cloud Project with:
  - Pub/Sub subscription configured
  - Cloud Storage bucket created
  - Service account with appropriate permissions

## Installation :)

1. Clone the repository:
   ```bash
   git clone https://github.com/egorman-sray/copilot-test.git
   cd copilot-test
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration :)

Set the following environment variables:

### Required Variables :)
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `PUBSUB_SUBSCRIPTION`: Name of the Pub/Sub subscription to consume from
- `GCS_BUCKET_NAME`: Name of the GCS bucket to store messages

### Optional Variables :)
- `MAX_MESSAGES`: Maximum number of messages to process concurrently (default: 10)
- `ACK_DEADLINE_SECONDS`: Message acknowledgment deadline (default: 60)

### Example Configuration :)
```bash
export GOOGLE_CLOUD_PROJECT="my-project-id"
export PUBSUB_SUBSCRIPTION="my-subscription"
export GCS_BUCKET_NAME="my-storage-bucket"
export MAX_MESSAGES="20"
export ACK_DEADLINE_SECONDS="120"
```

## Usage :)

### Running the Microservice :)
```bash
python main.py
```

### Docker Deployment :)
```bash
# Build the image
docker build -t pubsub-gcs-microservice .

# Run with environment variables
docker run -e GOOGLE_CLOUD_PROJECT="my-project" \
           -e PUBSUB_SUBSCRIPTION="my-sub" \
           -e GCS_BUCKET_NAME="my-bucket" \
           pubsub-gcs-microservice
```

## Message Format :)

The microservice stores messages in the following JSON format:
```json
{
  "message_id": "1234567890",
  "data": "Original message content",
  "attributes": {
    "key1": "value1",
    "key2": "value2"
  },
  "publish_time": "2023-12-01T10:30:00.000Z",
  "processed_at": "2023-12-01T10:30:05.123Z"
}
```

## Security Best Practices :)

- **Never commit credentials**: Use environment variables or cloud-native authentication
- **Service Account**: Use least-privilege service accounts for cloud access
- **Network Security**: Deploy in private networks when possible
- **Monitoring**: Enable Cloud Logging and Monitoring for production deployments

## Development :)

### Local Development with .env :)
Create a `.env` file for local development:
```env
GOOGLE_CLOUD_PROJECT=my-project-id
PUBSUB_SUBSCRIPTION=my-subscription
GCS_BUCKET_NAME=my-bucket
```

### Health Check :)
The service includes a health check endpoint that verifies:
- Pub/Sub subscription accessibility
- GCS bucket connectivity

## Monitoring :)

The microservice logs important events:
- Message processing start/completion
- Successful GCS uploads
- Error conditions and retries
- Health check results

## Error Handling :)

- **Message Processing Failures**: Messages are not acknowledged and will be retried
- **Connection Issues**: Service will log errors and attempt to reconnect
- **Invalid Configuration**: Service fails fast with clear error messages

## Contributing :)

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License :)

This project is open source and available under the MIT License.