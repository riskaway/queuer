# API
from fastapi import FastAPI, HTTPException

# Modeling and typing
from pydantic import BaseModel
from typing import Literal

# RabbitMQ
import pika

# Config from environment variables
from os import environ

# Model for a risk point
class RiskPoint(BaseModel):
    # Latitude of the risk point
    latitude: float
    # Longitude of the risk point
    longitude: float
    # Type of risk
    type: Literal["flood", "landslide", "hurricane"]
    # Additional information
    description: str | None = None


# Configuration handler
class RabbitMQConfig:
    host = "127.0.0.1"
    port = 5672
    publish_queue_name = "RISKPOINTS_QUEUE"
    username = "riskaway"
    password = "riskaway"

    def __init__(
        self,
        host: str = None,
        port: int = None,
        publish_queue_name: str = None,
        username: str = None,
        password: str = None,
    ) -> None:
        if host:
            self.host = host
        elif "RABBITMQ_HOST" in environ.keys():
            self.host = environ["RABBITMQ_HOST"]

        if port:
            self.port = port
        elif "RABBITMQ_PORT" in environ.keys():
            self.port = int(environ["RABBITMQ_PORT"])

        if publish_queue_name:
            self.publish_queue_name = publish_queue_name
        elif "RABBITMQ_PUBLISH_QUEUE" in environ.keys():
            self.publish_queue_name = environ["RABBITMQ_PUBLISH_QUEUE"]

        if username:
            self.username = username
        elif "RABBITMQ_DEFAULT_USER" in environ.keys():
            self.username = environ["RABBITMQ_DEFAULT_USER"]

        if password:
            self.password = password
        elif "RABBITMQ_DEFAULT_PASS" in environ.keys():
            self.password = environ["RABBITMQ_DEFAULT_PASS"]


# RabbitMQ publisher
class RabbitMQPublisher:
    def __init__(self, config: RabbitMQConfig) -> None:
        self.publish_queue_name = config.publish_queue_name
        credentials = pika.PlainCredentials(
            username=config.username, password=config.password, erase_on_connect=True
        )
        connection_parameters = pika.ConnectionParameters(
            host=config.host, port=config.port, credentials=credentials
        )
        # Connect to RabbitMQ instance
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        # Declare queue
        self.channel.queue_declare(queue=self.publish_queue_name)

    # Publish risk point to queue
    def publish(self, risk_data: str) -> bool:
        try:
            self.channel.basic_publish(
                exchange="", routing_key=self.publish_queue_name, body=risk_data
            )
            return True
        except Exception as e:
            print("[ERROR]", e)
            return False

    # Close connection
    def close(self) -> None:
        self.connection.close()


app = FastAPI()
config = RabbitMQConfig()
rmq_client = RabbitMQPublisher(config)

# Add risk point
@app.put("/add")
async def add_risk_point(risk_point: RiskPoint):
    all_ok: bool = rmq_client.publish(risk_point.json())
    if all_ok:
        return HTTPException(status_code=200, detail="Successfully added risk point")
    return HTTPException(status_code=500, detail="Error adding risk point")


# Close rabbitmq client on shutdown
@app.on_event("shutdown")
def close_client():
    rmq_client.close()
