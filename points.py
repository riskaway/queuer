# Modeling and typing
from pydantic import BaseModel
from typing import Literal

# Model for a flood point
class FloodPoint(BaseModel):
    latitude: float
    longitude: float
    # Depth of the flood at the risk point
    depth: Literal["ankle", "knee", "hip", "chest", "head"]
    # Additional information
    description: str | None = None
    # Risk type for RabbitMQ message
    risktype: str = "flood"


# Model for an earthquake point
class EarthquakePoint(BaseModel):
    latitude: float
    longitude: float
    # Intensity of the earthquake at the risk point
    intensity: Literal["low", "moderate", "high", "extreme"]
    description: str | None = None
    # Risk type for RabbitMQ message
    risktype: str = "earthquake"


# Model for a hurricane point
class HurricanePoint(BaseModel):
    latitude: float
    longitude: float
    # Intensity of the hurricane at the risk point
    intensity: Literal["low", "moderate", "high", "extreme"]
    description: str | None = None
    # Risk type for RabbitMQ message
    risktype: str = "hurricane"
