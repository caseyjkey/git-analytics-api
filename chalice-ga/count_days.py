from github import Github
from datetime import datetime, timedelta
import os.path
import os

gh_token = os.environ['TOKEN']

def loadRepos(Gh, repos):
    gh_user = Gh.get_user()
    return [gh_user.get_repo(repo) for repo in repos]
        

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
    return dates

# Counts the number of consecutive days committing starting from today
# params: Gh - the Github object
# params: repos - a list of repositories to search for commits
# returns: a streak >= 0 as an Integer
def count_commit_streak(Gh, repos):
    gh_user = Gh.get_user()
    dates = []

    for repo in repos:
        dates.extend(getCommits(gh_user, repo))

    dates = [date.date() for date in sorted(dates, reverse=True)]
    today = datetime.date(datetime.now())
    
    count = 1 if today in dates else 0
    today -= timedelta(days=1)

    while(True):
        # Did we make a commit today?
        if today in dates:
            count += 1
        else:
            break
        # Subtract one day
        today -= timedelta(days=1)

    return count

    

if __name__ == "__main__":
    with open("oauth.txt", 'r') as oauthFile:
        gh_token = oauthFile.readline().strip()

    g = Github(oauth)
    gh_user = g.get_user()

    if not os.path.exists('repos.txt'):
        saveReposToFile(gh_user)
    else:
        if input("Define repos? Press enter to skip. "):
            saveReposToFile(gh_user)

    repos = loadReposFromFile(gh_user) 

    count = count_commit_streak(g, repos)

    print("{} consectutive days contributing to Github!".format(count))
