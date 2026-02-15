from retrieval import Retrieval


class Controller(object):
    def __init__(self, retrieval: Retrieval):
        self._retrieval = retrieval

    def answer_on_request(self, request: str):
        candidates = self._retrieval.retrieve(request)
        print(len(candidates))
        return str(candidates)
