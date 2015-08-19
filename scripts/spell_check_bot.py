import sys
import os

import git_wrapper
import datastore
from analysis_bot import AnalysisBot
from enchant.checker import SpellChecker


def has_error(file_path):
    """return boolean indicating whether the file specified by the
    file_path contains spelling mistakes
    """
    with open(file_path, "r") as file_to_check:
        data = file_to_check.read()
        checker = SpellChecker("en_US")
        checker.set_text(data)
        for err in checker:
            return True
        return False


def suggest_correction(file_path):
    """return string representing the spell-corrected content of
    the file specified by the file_path
    """
    with open(file_path, "r") as file_to_check:
        data = file_to_check.read()
        checker = SpellChecker("en_US")
        checker.set_text(data)
        for err in checker:
            # avoid IndexOutOfBounds
            err.replace(checker.suggest()[0])
        return checker.get_text()


def auto_correct(file_path):
    """modify the file specified by the file_path by correcting
    spelling mistakes found in the file
    """
    correction = suggest_correction(file_path)
    with open(file_path, "w") as file_to_correct:
        file_to_correct.write(correction)


class SpellCheckBot(AnalysisBot):
    """Spell check the README.md on the master branch of a repo
    prepare pull requests for corrected spelling mistakes
    """
    BRANCH_NAME = "spell-check-corrections"
    PULL_REQUEST_BODY = ("Conducted automatic correction for " +
                         "auto-detected spelling mistakes")
    PULL_REQUEST_TITLE = "Fix Spelling Mistakes"

    def __init__(self, account):
        AnalysisBot.__init__(self, account, "SpellCheckerBot")

    def ready_to_analyze(self, project):
        if project.has_local_copy():
            return True
        else:
            return ["clone"]

    def analyze(self, project):
        # TODO: be more preventative:
        #       what happens if the branch already exist?
        #       what if we already submitted a pull request? (runtime handles)
        #       should there be more detail in the commit message?
        #       we should make sure we are starting with the master branch and
        #       on a clean slate.
        #       when we handle the above cases, we should consider moving
        #       these functions up as they are applicable to all bots that
        #       submits pull requests
        target_file = "README.md"
        repo_dir_path = os.path.abspath(
            os.path.join(project.local_repo.path, os.pardir))
        print(repo_dir_path)
        print(project.local_repo.path)
        readme_path = os.path.join(repo_dir_path, target_file)
        if has_error(readme_path):
            git_wrapper.create_and_checkout_branch(project.local_repo, self.BRANCH_NAME)
            auto_correct(readme_path)
            git_wrapper.commit_all(project.local_repo, self.account,
                                   "fix spelling mistakes")
            datastore.propose_pull(self, project, self.BRANCH_NAME,
                                   self.PULL_REQUEST_TITLE, self.PULL_REQUEST_BODY)


if __name__ == '__main__':
    """Spell correct the specified file"""
    auto_correct(sys.argv[1])
    sys.exit(0)
