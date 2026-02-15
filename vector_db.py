from typing import Dict, List, Tuple

from pymongo.mongo_client import MongoClient

from data import Embeddings


class MongoDBClient(object):
    def __init__(self, uri: str):
        self._client = MongoClient(uri)
        self._client.admin.command('ping')

        db = self._client["embeddings"]
        self._collection = db["embeddings"]

    def insert_data(self, data: List[Tuple[Embeddings, Dict[str, str | List[float]]]]) -> None:
        uploading_data = []
        for embedding, items_data in data:
            items_data["embedding"] = embedding
            uploading_data.append(items_data)

        result = self._collection.insert_many(uploading_data)
        # print(f"Inserted {len(result.inserted_ids)} mock documents")

    def _delete_all(self):
        self._collection.delete_many({})
