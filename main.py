import time

from git import Repo
import os

remoteurl = "https://github.com/an-tonic/test-repo-for-jetbrains.git"


folder_path = "D:/tmp"
if os.path.exists(folder_path):
    repo = Repo(folder_path)
    # origin = repo.remotes.origin
    # origin.pull()
else:
    repo = Repo.clone_from(remoteurl, folder_path)

for commit in repo.iter_commits():
    print(commit.diff())
    # Extract the list of files/modules modified in the commit
    # modified_files = [item.a_path for item in commit.diff()]
    # for item in commit.diff():
    #     print(item.a_path)
    # # Record contributors for each modified file/module
    # for file_path in modified_files:
    #     contributors_per_file[file_path].add(commit.author.email)





