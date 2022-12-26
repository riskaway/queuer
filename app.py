# API
from fastapi import FastAPI, HTTPException

# RabbitMQ
from rabbitmq_utils import RabbitMQConfig, RabbitMQProducer

# Risk points
from points import FloodPoint, EarthquakePoint, HurricanePoint

print("RabbitMQ configuration:", RabbitMQConfig)

app = FastAPI()
rmq_client = RabbitMQProducer()


# Add flood point
@app.put("/add/flood")
async def add_flood_point(flood_point: FloodPoint):
    print("[INFO] Received flood point:", flood_point)
    try:
        rmq_client.publish(flood_point.json(exclude_none=True))
        return HTTPException(status_code=200, detail="Successfully added flood point")
    except Exception as e:
        print("[ERROR] Error adding hurricane point:", e)
        return HTTPException(status_code=500, detail="Error adding flood point")


# Add earthquake point
@app.put("/add/earthquake")
async def add_earthquake_point(earthquake_point: EarthquakePoint):
    print("[INFO] Received earthquake_point point:", earthquake_point)
    try:
        rmq_client.publish(earthquake_point.json(exclude_none=True))
        return HTTPException(
            status_code=200, detail="Successfully added earthquake point"
        )
    except Exception as e:
        print("[ERROR] Error adding hurricane point:", e)
        return HTTPException(status_code=500, detail="Error adding earthquake point")


# Add hurricane point
@app.put("/add/hurricane")
async def add_hurricane_point(hurricane_point: HurricanePoint):
    print("[INFO] Received hurricane point:", hurricane_point)
    try:
        rmq_client.publish(hurricane_point.json(exclude_none=True))
        return HTTPException(
            status_code=200, detail="Successfully added hurricane point"
        )
    except Exception as e:
        print("[ERROR] Error adding hurricane point:", e)
        return HTTPException(status_code=500, detail="Error adding hurricane point")


# Close rabbitmq client on shutdown
@app.on_event("shutdown")
def close_client():
    rmq_client.close()
