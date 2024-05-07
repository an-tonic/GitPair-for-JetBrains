import time
from collections import defaultdict
from itertools import combinations

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


def contributions_by_author(repository, author_email):
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


def get_contributors_with_files(repository):
    contributors_with_files = defaultdict(lambda: defaultdict(int))

    for commit in repository.iter_commits(reverse=True):
        if len(commit.parents) == 0:
            continue
        # Extract modified files in the commit
        modified_files = {item.a_path: 1 for item in commit.parents[0].diff(commit)}

        # Update contributors_with_files directly
        for modified_file in modified_files:
            contributors_with_files[commit.author.email][modified_file] += 1

    return contributors_with_files


# Extremely inefficient code, for now. Something like O of n^2 or even n3
# Can definitely be improved, up to O of n. For example iterate over commits once not hundreds of times
# Result: a table of all pairs that contribute to files (with number of contributions for each file)
def calculate_git_pairs(repository):
    authors = calculate_top_contributors(repository)
    author_pairs = list(combinations(authors, 2))

    final = {}
    test = {}
    bin = {}
    for author_pair in author_pairs:
        dict_a = contributions_by_author(repository, author_pair[0])
        dict_b = contributions_by_author(repository, author_pair[1])
        print(author_pair[0], dict_a)
        print(author_pair[1], dict_b)
        for dictionary in (dict_a, dict_b):
            for key, value in dictionary.items():
                if key in bin:
                    # min value because if A contributed 5, and B contributed 3, then as a pair they contributed 3 times
                    test[key] = min(bin[key], value)
                else:
                    bin[key] = value
        # We keep only those contributions that *both* authors made, that is why we need a bin
        final[author_pair] = test.copy()
        test.clear()
        bin.clear()
    return final


# for key, value in calculate_git_pairs(repo).items():
#     print(key, value)
