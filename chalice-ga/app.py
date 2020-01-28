from chalice import Chalice
import count_days as ga
from github import Github

app = Chalice(app_name='chalice-ga')

# '/ouath_token/repo1,repo2,repo3'
@app.route('/streak/{token}/{repos}')
def hello_name(token, repos):
    g = Github(token)
    repos = ga.loadRepos(g, repos.split(','))
    return {"streak": {g.get_user().name: ga.count_commit_streak(g, repos)}}
