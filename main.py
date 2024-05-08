import time
from collections import defaultdict
from itertools import combinations

from git import Repo
import os

remoteurl = "https://github.com/an-tonic/test-repo-for-jetbrains.git"

folder_path = "D:/tmp"

if os.path.exists(folder_path):
    print("Repo exists on disk. Using it.")
    repo = Repo(folder_path)
    # origin = repo.remotes.origin
    # origin.pull()
else:
    print("Starting repository cloning")
    repo = Repo.clone_from(remoteurl, folder_path)
    print("Repo cloned successfully")


def get_all_contributors(repository):
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


# Calculates a pair of programmers who contribute to the same file with O of n speed (if I calculated it correctly)
# Input: a dictionary of authors' names and the files they have commited number of times
# Example input: {"author_name":{"file1":5, "file2": 2}}
# Result: a dictionary of all pairs that contribute to files (with number of contributions for each file)
# How it works: for each pair compars number of contributions and chooses the minimum value. I.e. if author One has
# changed file "X" 5 times and author Two has changed the same file 3 times - it means together they have changed
# it 3 times
def calculate_git_pairs(authors_and_files_data):
    pairs = {}
    if len(authors_and_files_data) == 1:
        print("Only one author found. Cannot generate pairs.")
        return authors_and_files_data

    for key1, key2 in combinations(authors_and_files_data.keys(), 2):
        combined_key = key1 + " + " + key2
        dict1 = authors_and_files_data[key1]
        dict2 = authors_and_files_data[key2]
        minimal_dict = {}

        # Iterate over the keys that are common to both dict1 and dict2 and find minimum value
        for k in set(dict1) & set(dict2):
            min_value = min(dict1.get(k, float('inf')), dict2.get(k, float('inf')))
            minimal_dict[k] = min_value
        sorted_minimal_dict = dict(sorted(minimal_dict.items(), key=lambda item: item[1], reverse=True))

        pairs[combined_key] = sorted_minimal_dict

    pairs = dict(sorted(pairs.items(), key=lambda item: next(iter(item[1].values())), reverse=True))

    return pairs


print("Finding all contributors and files...")
start_time = time.perf_counter()
authors = get_contributors_with_files(repo)
elapsed_time = time.perf_counter() - start_time
print("Found ", len(authors), "contributors in ", elapsed_time, " seconds")

print("Calculating git pairs...")
git_pairs = calculate_git_pairs(authors)
print("Finished calculating git pairs...")

print("Printing git pairs...")
for k, v in git_pairs.items():
    print(k, v)
