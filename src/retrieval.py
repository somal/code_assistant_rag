from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Tuple

from sentence_transformers import SentenceTransformer

from data import Embedding, FunctionItem, Item
from vector_db import MongoDBClient


class Retrieval(object):
    FUNCTION_ITEM_PARAMS_TO_EMBED = ['name', 'code', 'docstring', 'params', 'file_path']
    CLASS_ITEM_PARAMS_TO_EMBED = ['name', 'code', 'docstring', 'bases', 'file_path']

    def __init__(self,
                 overlapping_fraction: float,
                 embedding_model: str,
                 vector_db_client: MongoDBClient,
                 retrieve_top_k=5):
        self._overlapping_fraction = overlapping_fraction
        self._embedding = SentenceTransformer(embedding_model,
                                              model_kwargs={"device_map": "auto"})
        self._vector_db_client = vector_db_client
        self._retrieve_top_k = retrieve_top_k

    @property
    def chunk_size(self):
        return self._embedding.max_seq_length

    @staticmethod
    def _get_params_to_embed(item: Item) -> Iterable[str]:
        target_list = Retrieval.FUNCTION_ITEM_PARAMS_TO_EMBED if isinstance(item, FunctionItem) \
            else Retrieval.CLASS_ITEM_PARAMS_TO_EMBED
        for param in target_list:
            param_value = getattr(item, param)
            assert isinstance(param_value, str), f'{type(param_value)}'
            yield param_value

    def _split_items_to_chunks(self, data: List[Item]) -> Iterable[Tuple[str, Item]]:
        chunk_size = self.chunk_size
        overlapping_fraction = int(chunk_size * self._overlapping_fraction)
        for item in data:
            for param_value in Retrieval._get_params_to_embed(item):
                start = 0
                end = chunk_size
                while start < len(param_value):
                    chunk = param_value[start: end]
                    start += overlapping_fraction
                    end = start + chunk_size
                    yield chunk, item

    def _get_documents_embeddings(self, documents: List[str]) -> List[Embedding]:
        return self._embedding.encode(documents).tolist()

    def _get_request_embeddings(self, queries: List[str]) -> List[Embedding]:
        return self._embedding.encode(queries, prompt_name="query").tolist()

    def _upload_one_item_to_vector_database(self, embedding: Embedding, item: Item) -> None:
        self._vector_db_client.insert_data([(embedding, asdict(item))])

    def upload_retrievable_data(self, data: List[Item]):
        for chunk, item in self._split_items_to_chunks(data):
            chunk_embedding = self._get_documents_embeddings([chunk])[0]
            self._upload_one_item_to_vector_database(chunk_embedding, item)

    def retrieve(self, request: str) -> List[Dict[str, Any]]:
        embedding = self._get_request_embeddings([request])[0]
        candidates = self._vector_db_client.find_similar(embedding, self._retrieve_top_k)
        return candidates