from fastapi import FastAPI
from pydantic import BaseModel

class RiskPoint(BaseModel):
    latitude: float
    longitude: float
    type: str
    description: str | None = None

app = FastAPI()

@app.put("/add")
def add_risk_point(risk_point: RiskPoint):
    return risk_point
