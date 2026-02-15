from typing import Any, Dict, List, Tuple

from pymongo.mongo_client import MongoClient

from data import Embedding


class MongoDBClient(object):
    def __init__(self, uri: str):
        self._client = MongoClient(uri)
        self._client.admin.command('ping')

        db = self._client["embeddings"]
        self._collection = db["embeddings"]

    def _delete_all(self):
        self._collection.delete_many({})

    def insert_data(self, data: List[Tuple[Embedding, Dict[str, str | List[float]]]]) -> None:
        uploading_data = []
        for embedding, items_data in data:
            items_data["embedding"] = embedding
            uploading_data.append(items_data)

        result = self._collection.insert_many(uploading_data)
        # print(f"Inserted {len(result.inserted_ids)} mock documents")

    def find_similar(self, embedding: Embedding, top_k: int) -> List[Dict[str, Any]]:
        pipeline1 = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 10000,  # ← Use ALL docs (you only have 3!)
                    "limit": top_k
                }
            },
            {
                "$addFields": {  # Always include score, even without projection
                    "score": {"$meta": "vectorSearchScore"}
                }
            },
            # {
            #     "$project": {
            #         "file_path": 1,
            #         "start_line": 1,
            #         "code": 1,
            #         "description": 1,
            #         "score": 1
            #     }
            # }
        ]

        print("Trying basic vectorSearch...")
        results = list(self._collection.aggregate(pipeline1))
        print(f"Basic search returned {len(results)} results")
        return results
