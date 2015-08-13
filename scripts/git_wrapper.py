"""A wrapper for git that makes using git in python through pygit2 easiergit_helpers
   
repo is of type pygit2.Repository
"""

import pygit2


class GitException(Exception):
    def __init__(self, message):
        self.message = message


def clone_or_update_repo(github_repo, account, target_path):
    if not os.path.exists(target_path + '/.git/'):
        try:
            return pygit2.clone_repository(github_repo.clone_url, target_path,
                credentials=account.credentials)
        except pygit2.GitError as e:
            raise GitException("Cloning failed. {}".format(e.message))
    else:
        repo = pygit2.Repository(pygit2.discover_repository(target_path))
        for remote in repo.remotes:
            remote.credentials = _credential_lambda(account)
            transfer_progress = remote.fetch()
        return repo

def create_and_checkout_branch(repo, branch_name):
    """git checkout -b [branch_name]"""
    branch = repo.create_branch(branch_name, repo.head.get_object())
    repo.checkout(repo.lookup_reference(branch.name))

def commit_all(repo, account, message):
    """git commit -am [message]"""
    index = repo.index
    index.add_all()
    index.write()
    tree = index.write_tree()
    parents = [repo.head.get_object().hex]
    repo.create_commit('HEAD', account.signature, account.signature, 
        message, tree, parents)

def push_current_branch_up(repo, account):
    # TODO: handle exceptions 
    for remote in repo.remotes:
        remote.credentials = _credential_lambda(account)
        remote.push([repo.head.name])

def _credential_lambda(account):
    return lambda x, y, z : account.credentials