"""Data models
for repository and user account

used as ORM interfacing with the datastore
"""
import pygit2
import github3

class Repo:
    """Wrap the github repo together with the local repo"""

    def __init__(self, github_repo, local_repo=None, github_fork=None):
        """Create a wrapper from the github repo and local repo

        :param github_repo: github3.repos.repo.Repository 
        :param local_repo: pygit2.Repository
        :param github_fork: github3.repos.repo.Repository
        """
        self.github_repo = github_repo
        self.local_repo = local_repo
        self.github_fork = github_fork

    def has_clone(self):
        return self.local_repo is not None

    def create_fork_and_clone(self, account):


class Account:
    """GitHub account information for the bot accounts.

    Captures the credentials and authentication information
    interfacing with git and GitHub
    """

    def __init__(self, username, password, email):
        """
        :param username: string 
        :param password: string
        :param email: string
        """
        self.username = username
        self.email = email
        self.github = github3.login(username, password)
        self.credentials = pygit2.UserPass(username, password)
        self.signature = pygit2.Signature(username, email)


class PullRequest:
    """Captures information of a proposed pull request
    """
    # TODO: will capture more information such as feedback etc.


    def __init__(self, bot, repo, branch_name, title, body):
        self.bot = bot
        self.repo = repo
        self.branch_name = branch_name
        self.title = title
        self.body = body

    def submit():
        """submit the pull request to GitHub"""
        # It feels natural in O-O to put the submit method here
        # but want to limit this method to runtime
        self.submitted = True


def get_all_ready_repo_from_repo_name(owner_name, repo_name):
    """fork the repo to the organization"""