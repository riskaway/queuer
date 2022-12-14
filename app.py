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
RabbitMQConfig: dict = {
    "host": environ["RABBITMQ_HOST"]
    if "RABBITMQ_HOST" in environ.keys()
    else "0.0.0.0",
    # RabbitMQ runs on port 5672 by default
    "port": int(environ["RABBITMQ_PORT"])
    if "RABBITMQ_PORT" in environ.keys()
    else 5672,
    # Default user: guest
    "username": environ["RABBITMQ_DEFAULT_USER"]
    if "RABBITMQ_DEFAULT_USER" in environ.keys()
    else "guest",
    # Default password: guest
    "password": environ["RABBITMQ_DEFAULT_PASS"]
    if "RABBITMQ_DEFAULT_PASS" in environ.keys()
    else "guest",
    # Store in queue named "RISKPOINTS_QUEUE"
    "publish_queue_name": environ["RABBITMQ_PUBLISH_QUEUE"]
    if "RABBITMQ_PUBLISH_QUEUE" in environ.keys()
    else "RISKPOINTS_QUEUE",
}

# RabbitMQ publisher
class RabbitMQPublisher:
    def __init__(self) -> None:
        self.publish_queue_name = RabbitMQConfig["publish_queue_name"]
        connection_parameters = pika.URLParameters(
            f"amqp://{RabbitMQConfig['username']}:{RabbitMQConfig['password']}@{RabbitMQConfig['host']}:{RabbitMQConfig['port']}/%2F"
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


print("RabbitMQ configuration:", RabbitMQConfig)

app = FastAPI()
rmq_client = RabbitMQPublisher()

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
