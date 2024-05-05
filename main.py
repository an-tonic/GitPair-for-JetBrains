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

def display_contributions_by_author(repository, author_email):
    contributions = {}

    # Traverse commits
    for commit in repository.iter_commits(reverse=True):
        if commit.author.email == author_email:
            # skipping the first because has no parents
            if len(commit.parents) == 0:
                continue
            modified_files = [item.a_path for item in commit.parents[0].diff(commit)]

            for file_path in modified_files:
                if file_path in contributions:
                    contributions[file_path] += 1
                else:
                    contributions[file_path] = 1

    sorted_contributors = dict(sorted(contributions.items(), key=lambda item: item[1], reverse=True))

    return sorted_contributors


print(display_contributions_by_author(repo, "96774237+an-tonic@users.noreply.github.com"))
