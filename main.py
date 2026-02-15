import os

from dotenv import load_dotenv

from controller import Controller
from data import clone_repo, split_code_from_repo_into_items
from retrieval import Retrieval
from vector_db import MongoDBClient
from view import launch_ui

load_dotenv('.env')

repo_url = "https://github.com/ultralytics/ultralytics.git"
local_path = "./ultralytics"
target_repo_folder = ['ultralytics/models', 'ultralytics/engine', 'ultralytics/data']
embedding_model = "Qwen/Qwen3-Embedding-0.6B"
uri = os.environ['MONGODB_CONNECTION_STRING']
clone_repo(repo_url, local_path)
items = split_code_from_repo_into_items(repo_path=local_path, target_dirs=target_repo_folder)
# print([asdict(item) for item in items])


mongo_client = MongoDBClient(uri=uri)
mongo_client._delete_all()
r = Retrieval(overlapping_fraction=0.5, embedding_model=embedding_model, vector_db_client=mongo_client)
# r.upload_retrievable_data(items)

controller = Controller(retrieval=r)
launch_ui(controller)
