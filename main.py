import time

from git import Repo
import os

remoteurl = "https://github.com/an-tonic/CO1111-Shared-Project.git"
folder_path = "D:/tmp"

if os.path.exists(folder_path):
    repo = Repo(folder_path)
    # origin = repo.remotes.origin
    # origin.pull()
else:
    repo = Repo.clone_from(remoteurl, folder_path)


def calculate_top_contributors(repository):
    contributors = {}

    for commit in repository.iter_commits(reverse=True):
        author_email = commit.author.email

        if author_email in contributors:
            contributors[author_email] += 1
        else:
            contributors[author_email] = 1

    # Sort contributors by number of commits
    sorted_contributors = dict(sorted(contributors.items(), key=lambda item: item[1], reverse=True))

    return sorted_contributors


print(calculate_top_contributors(repo))
