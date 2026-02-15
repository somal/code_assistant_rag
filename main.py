from dataclasses import asdict

from data import clone_repo, split_code_from_repo_into_items

from retrieval import Retrieval

repo_url = "https://github.com/ultralytics/ultralytics.git"
local_path = "./ultralytics"
target_repo_folder = ['ultralytics/models', 'ultralytics/engine', 'ultralytics/data']
embedding_model = "Qwen/Qwen3-Embedding-0.6B"
clone_repo(repo_url, local_path)
items = split_code_from_repo_into_items(repo_path=local_path, target_dirs=target_repo_folder)
# print([asdict(item) for item in items])


r = Retrieval(overlapping_fraction=0.5, embedding_model=embedding_model)
r.upload_retrievable_data(items)