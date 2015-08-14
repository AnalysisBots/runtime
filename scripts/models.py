"""Data models
for repository and user account

used as ORM interfacing with the datastore
"""
import pygit2
import github3

class Repo:
    """Wrap the github repo together with the local repo"""

    def __init__(self, repo_id, local_repo=None, fork_id=None):
        """Create a wrapper from the github repo and local repo

        :param repo_id: int 
        :param local_repo: pygit2.Repository
        :param fork_id: int
        """

        self.local_repo = local_repo

        # Note: since github3.repo.Repository contains auth info that
        #       doesn't look like could be changed easily after object
        #       creation, we are storing id so that Repo object can be
        #       easily retreived and constructed with an account
        #       More investigation is needed
        self.repo_id = repo_id
        self.fork_id = fork_id

    def has_local_copy(self):
        return self.local_repo is not None


class Project:
    """GitHub Project"""
    # TODO
    pass


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


    def __init__(self, bot, repo, head_branch, title, body):
        self.bot = bot
        self.repo = repo
        self.head_branch = head_branch
        self.title = title
        self.body = body

