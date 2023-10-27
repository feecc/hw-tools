from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.db import Mongo
from src.api.handlers import handle_not_found
from src.devices import action_port

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)


@app.get("/devices", description="Получение списка всех устройств")
async def get_all_devices():
    return Mongo.get_all()


@app.get("/devices/{device_id}", description="Получение данных об устройстве по id")
async def get_device_by_id(device_id: str):
    with handle_not_found():
        device = Mongo.get_by_id(device_id)
        match device["type"]:
            case "scales":
                device["data"] = {"weight": action_port.action_scales("W0G1")}
            case "barrier":
                device["data"] = {"state": action_port.action_barrier("state")}
            case _:
                raise ValueError("No instructions for device")
    return device


@app.post("/devices/{device_id}", description="Отправка устройству команды на действие")
async def startup_action(device_id: str):
    with handle_not_found():
        device = Mongo.get_by_id(device_id)
        match device["type"]:
            case "scales":
                device["data"] = {"weight": action_port.action_scales("W0G1")}
            case "barrier":
                device["data"] = {"state": action_port.action_barrier("change")}
            case _:
                raise ValueError("No instructions for device")
    return device


@app.on_event("startup")
async def test_start_app():
    Mongo.test_fill_db()
