import os

from dotenv import load_dotenv

from controller import Controller
from data import clone_repo, split_code_from_repo_into_items
from generation import Generation
from retrieval import Retrieval
from vector_db import MongoDBClient
from view import launch_ui

REPO_URL = "https://github.com/ultralytics/ultralytics.git"
REPO_LOCAL_PATH = "./ultralytics"
TARGET_REPO_FOLDER = ['ultralytics/models', 'ultralytics/engine', 'ultralytics/data']
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
GENERATION_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"

load_dotenv('.env')
api_key = os.environ['API_KEY']
uri = os.environ['MONGODB_CONNECTION_STRING']

clone_repo(REPO_URL, REPO_LOCAL_PATH)
items = split_code_from_repo_into_items(repo_path=REPO_LOCAL_PATH, target_dirs=TARGET_REPO_FOLDER)

mongo_client = MongoDBClient(uri=uri)
r = Retrieval(overlapping_fraction=0.5,
              embedding_model=EMBEDDING_MODEL,
              vector_db_client=mongo_client,
              retrieve_top_k=5)
generation = Generation(model_name=GENERATION_MODEL, api_key=api_key)
# mongo_client._delete_all()
# r.upload_retrievable_data(items)

controller = Controller(retrieval=r, generation=generation)
launch_ui(controller)
