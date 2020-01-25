from github import Github
from datetime import datetime, timedelta
import os.path


def saveReposToFile(gh_user):
    repos = gh_user.get_repos()
    
    for index, repo in enumerate(repos):
        print('{}: {}'.format(index, repo.name))
    selectedRepos = input("Enter the repos you want to track seperated by commas: ")
    indexes = [int(index) for index in selectedRepos.replace(' ', '').split(',')]
    repos = [repo for index, repo in enumerate(repos) if index in indexes]

    with open("repos.txt", 'w') as reposFile:
        for repo in repos:
            reposFile.write(repo.name + '\n')


def loadReposFromFile(gh_user, filename = "repos.txt"):
    repos = []
    with open(filename, 'r') as reposFile:
        for repo in reposFile:
            repo = repo.strip()
            print(repo)
            if repo:
                repos.append(gh_user.get_repo(repo))
    return repos


def getCommits(gh_user, repo):
    username = gh_user.login
    name = gh_user.name
    commits = repo.get_commits()
    dates = []
    print("{} total commits for {}".format(commits.totalCount, repo.name))
    for commit in commits:
        isMe = commit.commit.author.name == name 
        if isMe:
            dates.append(commit.commit.committer.date)
            print("Found commit", commit.commit)
    return dates


if __name__ == "__main__":
    g = Github("923fef7126fc2150e1eb4f8ac40a02acbd06790e")
    gh_user = g.get_user()
    dates = []
    repos = []

    if not os.path.exists('repos.txt'):
        loadReposFromFile(gh_user)
    else:
        if input("Define repos? Press enter to skip."):
            saveReposToFile(gh_user)

    for repo in loadReposFromFile(gh_user): 
        dates.extend(getCommits(gh_user, repo))

    dates = sorted(dates, reverse=True)
    print(dates[0].date(), dates[1].date())
    print(dates[0] - dates[1])
