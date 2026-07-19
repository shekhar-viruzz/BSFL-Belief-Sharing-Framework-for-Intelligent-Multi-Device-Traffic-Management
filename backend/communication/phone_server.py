from fastapi import FastAPI
from pydantic import BaseModel

from ai.belief_manager import BeliefManager


app = FastAPI()


# AI engine (Snapdragon PC)
belief_manager = BeliefManager()


# Store live SUMO vehicle data
latest_vehicles = {}



# -----------------------------
# AI Prediction Data
# -----------------------------

class VehicleData(BaseModel):

    vehicle_id: str
    speed: float
    waiting_time: float
    density: float
    acceleration: float



@app.post("/predict")
def predict(data: VehicleData):

    result = belief_manager.predict(

        data.speed,
        data.waiting_time,
        data.density,
        data.acceleration

    )


    return {

        "vehicle_id": data.vehicle_id,

        "belief": result["belief"],

        "confidence": result["confidence"]

    }



# -----------------------------
# SUMO Vehicle Data
# -----------------------------

class SUMOVehicle(BaseModel):

    vehicle_id: str
    speed: float
    waiting_time: float
    lane: str



@app.post("/sumo_vehicle")
def receive_sumo_vehicle(data: SUMOVehicle):

    latest_vehicles[data.vehicle_id] = {

        "speed": data.speed,

        "waiting_time": data.waiting_time,

        "lane": data.lane

    }


    return {

        "status": "received",

        "vehicle_id": data.vehicle_id

    }




# -----------------------------
# Phone gets live SUMO data
# -----------------------------

@app.get("/vehicles")
def send_vehicles():

    return latest_vehicles




# -----------------------------
# Server Status
# -----------------------------

@app.get("/")
def home():

    return {

        "status": "BSFL Communication Server Running",

        "vehicles": len(latest_vehicles)

    }
