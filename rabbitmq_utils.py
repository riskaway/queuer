# RabbitMQ client module
import pika

# Config from environment variables
from os import environ

# Configuration handler
RabbitMQConfig: dict = {
    "host": environ["RABBITMQ_HOST"]
    if "RABBITMQ_HOST" in environ.keys()
    else "0.0.0.0",
    # RabbitMQ runs on port 5672 by default
    "port": int(environ["RABBITMQ_PORT"])
    if "RABBITMQ_PORT" in environ.keys()
    else 5672,
    # Default user: guest
    "username": environ["RABBITMQ_USER"]
    if "RABBITMQ_USER" in environ.keys()
    else "guest",
    # Default password: guest
    "password": environ["RABBITMQ_PASS"]
    if "RABBITMQ_PASS" in environ.keys()
    else "guest",
    # Store in queue named "RISKPOINTS_QUEUE"
    "queue_name": environ["RABBITMQ_RISKPOINTS_QUEUE"]
    if "RABBITMQ_RISKPOINTS_QUEUE" in environ.keys()
    else "RISKPOINTS_QUEUE",
}

# RabbitMQ publisher
class RabbitMQProducer:
    def __init__(self) -> None:
        self.queue_name = RabbitMQConfig["queue_name"]
        connection_parameters = pika.URLParameters(
            f"amqp://{RabbitMQConfig['username']}:{RabbitMQConfig['password']}@{RabbitMQConfig['host']}:{RabbitMQConfig['port']}/%2F"
        )
        # Connect to RabbitMQ instance
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        # Declare queue
        self.channel.queue_declare(queue=self.queue_name)

    # Publish risk point to queue
    def publish(self, risk_data: str) -> bool:
        try:
            self.channel.basic_publish(
                exchange="", routing_key=self.queue_name, body=risk_data
            )
            return True
        except Exception as e:
            print("[ERROR]", e)
            return False

    # Close connection
    def close(self) -> None:
        self.connection.close()
