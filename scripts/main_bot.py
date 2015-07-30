import os
import sys

from github3 import GitHub
from github3 import login
import pygit2
import git_helpers
import spell_checker

# TODO refactor
# This file currently contains the scripts for searching and cloning GitHub 
# repos.
# Most of the functionality will probably be moved out into its seperate files
# at a later point when we have more complete functionalities and are in a 
# position to structure the code better


# TODO Create a class for AnalysisBot 
# capture authentication info for AnalysisBot's own account
# rate-limit will be increased with authentication

# Rate limit info:
#             |  Unauthenticated   |  Using Authentication  | Client id & secret
# ------------------------------------------------------------------------------
# Search API  |  30/min            |  10 per minute         |  ???  (large)
# Other       |  5000/hr           |  60 per hour           |  ???  (large)
class AnalysisBot:
    def __init__(self, username, password):
        self.username = username
        self.github = login(username, password)
        self.dir_manager = git_helpers.DirManager()
        self.credentials = pygit2.UserPass(username, password)


    # search and clone 10 repos of a specified GitHub user into the directory from 
    def cloneReposFrom(self, username, number=-1):
        for repo in GitHub().repositories_by(username, number):
            git_helpers.GitHelper(repo.clone_url, self.dir_manager, self.credentials)
            #os.system("git clone {}".format(repo.clone_url)) # use system's git 

    def cloneRepo(self, owner, repo_name): 
        repo = self.github.repository(owner, repo_name)
        git_helper = git_helpers.GitHelper(repo.clone_url, self.dir_manager, self.credentials)
        return git_helper

    def forkAndCloneRepo(self, owner, repo_name):
        repo = self.github.repository(owner, repo_name)
        forked_repo = repo.create_fork()
        return self.cloneRepo(self.username, repo_name)

    def get_readme_path(self, helper):
        return helper.dir_path + "/README.md"

    def spell_check_readme(self, owner, repo_name):
        repo_dir_path = self.cloneRepo(owner, repo_name).dir_path
        if spell_checker.has_error(repo_dir_path + "/README.md"):
            fork_repo_helper = self.forkAndCloneRepo(owner, repo_name)
            fork_repo_helper.create_and_checkout_branch("patch-spell-check")
            spell_checker.auto_correct(self.get_readme_path(fork_repo_helper))
            print(fork_repo_helper.dir_path)

# TODO: let it take in a username, password, and owner, repo name
#       and create a pull request for that repo based on spell check
if __name__ == '__main__':
    AnalysisBot(sys.argv[1], sys.argv[2]).spell_check_readme(sys.argv[3], sys.argv[4])

