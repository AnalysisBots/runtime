import os
import tempfile

import pygit2

## This is originally copied from https://github.com/RepoGrams/RepoGrams/blob/master/app/git_helpers.py
## The file has gone through major changes to delete unused component
## TODO further changes are still needed to adapt the code for use with analysis bots

class DirManager(object):
    def __init__(self, basedir=None):
        if basedir is None:
            basedir = tempfile.mkdtemp()
        self.basedir = basedir
        self.url2dir = {}

    def get_repo_dir(self, url):
        if url in self.url2dir:
            return self.url2dir[url]
        dir_path = tempfile.mkdtemp(dir=self.basedir)
        self.url2dir[url] = dir_path
        return dir_path


class GitException(Exception):
    def __init__(self, message):
        self.message = message


class GitHelper(object):
    def __init__(self, repo_url, dir_manager, credentials, username, email):
        """
        :repo_url: URL of the repository
        :repo_dir: directory where the repository is expected to reside
        """
        self.signature = pygit2.Signature(username, email)
        self.up2date = False
        self.repo_url = repo_url
        self.dir_path = dir_manager.get_repo_dir(repo_url)
        #print(dir_path)

        self.credentials = credentials
        print("@@@@@@@@@@@@@") # TODO remove prints
        print(repo_url, self.dir_path)
        if not os.path.exists(self.dir_path + '/.git/'):
            try:
                self.repo = pygit2.clone_repository(repo_url, self.dir_path, credentials=credentials)
            except pygit2.GitError as e:
                raise GitException("Cloning failed. {}".format(e.message))
        else:
            self.repo = pygit2.Repository(pygit2.discover_repository(dir_path))
            self.up2date = True

            def _remote_credentials(url, username_from_url, allowed_types):
                return credentials

            for remote in self.repo.remotes:
                remote.credentials = _remote_credentials
                transfer_progress = remote.fetch()
                if transfer_progress.received_objects:
                    self.up2date = False

    def create_and_checkout_branch(self, branch_name):
        branch = self.repo.create_branch(branch_name, self.repo.head.get_object())
        self.repo.checkout(self.repo.lookup_reference(branch.name))

    def commit_all(self, message):
        index = self.repo.index
        index.add_all()
        index.write()
        tree = index.write_tree()
        parents = [self.repo.head.get_object().hex]
        self.repo.create_commit('HEAD', self.signature, self.signature, message, tree, parents)

    def push_current_branch_up(self):
        # handle exceptions
        for remote in self.repo.remotes:
            remote.credentials = lambda x, y, z : self.credentials
            remote.push([self.repo.head.name])
