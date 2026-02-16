from generation import Generation
from retrieval import Retrieval


class Controller(object):
    def __init__(self, retrieval: Retrieval, generation: Generation):
        self._retrieval = retrieval
        self._generation = generation

    def answer_on_request(self, request: str):
        code_items = self._retrieval.retrieve(request)
        answer = self._generation.generate_answer(user_request=request, code_chunks=code_items)
        return answer
