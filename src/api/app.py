from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.handlers import handle_not_found
from configs import Config
from src.devices import VT009, Barrier

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
    return Config


@app.get("/devices/{device_id}", description="Получение данных об устройстве по id")
async def get_device_by_id(device_id: str):
    with handle_not_found():
        device_name = Config.get_device_name(device_id)
        match device_name:
            case "VT-009-terminal":
                device = VT009(Config.get_device(device_id))
                response = {"id" : device_id, "name": device_name, "data": device.contact_device(request_type="get", data_type="weight")}
            case "barrier":
                device = Barrier(Config.get_device(device_id))
                response = {"id" : device_id, "name": device_name, "data": device.contact_device()}
            case _:
                raise ValueError("No instructions for device")
    return response


@app.post("/devices/{device_id}", description="Отправка устройству команды на действие")
async def startup_action(device_id: str):
    with handle_not_found():
        device = Config
        match device["type"]:
            case "scales":
                device["data"] = {"weight": action_port.action_scales("W0G1")}
            case "barrier":
                device["data"] = {"state": action_port.action_barrier("change")}
            case _:
                raise ValueError("No instructions for device")
    return device
