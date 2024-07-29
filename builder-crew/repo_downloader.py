import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from git import Repo
import get_stack_trace
import shutil

def search_and_copy_files(repo_dir, filenames, destination_dir):
    found_files = set()
    for root, dirs, files in os.walk(repo_dir):
        for filename in filenames:
            if filename in files:
                source_file = os.path.join(root, filename)
                destination_file = os.path.join(destination_dir, filename)
                if filename not in found_files:
                    shutil.copy2(source_file, destination_file)
                    found_files.add(filename)
    return found_files
    

def repo_downloader(repo_dir, error_folder_directory, destinarion_dir):
    repo_url = f"https://{os.environ.get("GIT_AZURE_TOKEN")}@dev.azure.com/HavanLabs/{os.environ.get("GIT_AZURE_SQUAD")}/_git/{os.environ.get("GIT_AZURE_REPO")}"
    if not os.path.exists(repo_dir) or not os.listdir(repo_dir):
        repo = Repo.clone_from(repo_url, repo_dir)
    else:
        print(f"Repositorio já existe {repo_dir}.\n")

    directory_path = Path(error_folder_directory)
    list_file_error = get_stack_trace.get_file_list_error(directory_path=directory_path, log=False)
    os.makedirs(destinarion_dir, exist_ok=True)
    final_result = search_and_copy_files(repo_dir=repo_dir, filenames=list_file_error, destination_dir=destinarion_dir)
    return final_result

def repo_delete(repo_dir):
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

def start_repo_downloader(repo_dir, error_folder_directory, destinarion_dir):
    final_result = repo_downloader(repo_dir, error_folder_directory, destinarion_dir)
    repo_delete(repo_dir=repo_dir)
    return final_result

if __name__ == "__main__":
    repo_dir = "current_repo_temp"
    start_repo_downloader(repo_dir=repo_dir)
