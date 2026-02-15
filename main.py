from data import clone_repo, split_code_from_repo_into_items

repo_url = "https://github.com/ultralytics/ultralytics.git"
local_path = "./ultralytics"
target_repo_folder = ['ultralytics/models', 'ultralytics/engine', 'ultralytics/data']
clone_repo(repo_url, local_path)
items = split_code_from_repo_into_items(repo_path=local_path, target_dirs=target_repo_folder)
print(items)
