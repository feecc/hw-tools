import os
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.collection import Collection


class _MongoWrapper:
    def __init__(self) -> None:
        uri = os.environ.get('MONGO_CONN_STR', 'mongodb://admin:admin@localhost:27017')
        self.db: AsyncIOMotorDatabase = AsyncIOMotorClient(uri)["db"]
        self.sync_db = MongoClient(uri)["db"]

        self.devices_collection: Collection = self.db["devices"]

    @staticmethod
    def _prepare_data(entry: dict) -> dict:
        _id = entry.pop("_id", None)
        entry["_id"] = str(_id)
        return entry

    async def test_fill_db(self):
        if await self.devices_collection.count_documents({}) == 0:
            test_devices = list()
            test_devices.append({"name": "testbarrier", "type": "barrier"})
            test_devices.append({"name": "testscales", "type": "scales"})
            await self.devices_collection.insert_many(test_devices)

    async def get_all(self) -> list[dict]:
        devices = await self.devices_collection.find({}).to_list(length=None)
        return list(map(self._prepare_data, devices))

    async def get_by_id(self, id: str) -> dict:
        data = await self.devices_collection.find_one({"_id": ObjectId(id)})
        if not data:
            raise ValueError("Not found")
        return self._prepare_data(data)

    def clear(self):
        self.sync_db.command("dropDatabase")


Mongo = _MongoWrapper()
