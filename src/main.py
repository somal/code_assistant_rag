import os

from dotenv import load_dotenv

from controller import Controller
from data import clone_repo, split_code_from_repo_into_items
from retrieval import Retrieval
from vector_db import MongoDBClient
from view import launch_ui
from generation import Generation

load_dotenv('.env')

repo_url = "https://github.com/ultralytics/ultralytics.git"
local_path = "./ultralytics"
target_repo_folder = ['ultralytics/models', 'ultralytics/engine', 'ultralytics/data']
embedding_model = "Qwen/Qwen3-Embedding-0.6B"
generation_model = "nvidia/nemotron-3-nano-30b-a3b:free"
api_key = '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'
uri = os.environ['MONGODB_CONNECTION_STRING']
clone_repo(repo_url, local_path)
items = split_code_from_repo_into_items(repo_path=local_path, target_dirs=target_repo_folder)


mongo_client = MongoDBClient(uri=uri)
r = Retrieval(overlapping_fraction=0.5,
              embedding_model=embedding_model,
              vector_db_client=mongo_client,
              retrieve_top_k=5)
generation = Generation(model_name=generation_model, api_key=api_key)
# mongo_client._delete_all()
# r.upload_retrievable_data(items)

controller = Controller(retrieval=r, generation=generation)
launch_ui(controller)
