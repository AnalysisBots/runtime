""" Instantiates bots, schedules them,runs them etc."""

import sys


from spell_check_bot import SpellCheckBot
import git_wrapper
import models
import datastore


def set_up_datastore(account):
    # This is a stub
    spell_check_bot = SpellCheckBot(account)
    test_repo = account.github.repository("AnalysisBots",
                                          "spell-check-bot-tests")
    # TODO: should create fork under organization
    #       might have a problem when testing
    forked_repo = test_repo.create_fork()
    repo_dir = datastore.get_repo_dir(forked_repo.id)
    local_repo = git_wrapper.clone_or_update_repo(forked_repo, account,
                                                  repo_dir)
    datastore.load_data(spell_check_bot,
                        models.Project(test_repo.id, local_repo, forked_repo.id))


def submit(pull):
    """submit the pull request to GitHub"""
    pull.submitted = True
    # TODO handle conditional forking
    git_wrapper.push_current_branch_up(pull.repo.local_repo,
        pull.bot.account)
    original_repo = pull.bot.account.github.repository_with_id(
        pull.repo.repo_id)
    head = pull.bot.account.username + ":" + pull.head_branch
    original_repo.create_pull(pull.title, "master", head, pull.body)


def main(username, password, email):
    # Run the analysis bot
    set_up_datastore(models.Account(username, password, email))
    for bot in datastore.get_bots():
        for repo in datastore.get_repos_signed_up_for_bot(bot):
            if bot.ready_to_analyze(repo):
                bot.analyze(repo)
            else:
                # TODO check whether the repo should be
                # forked / cloned
                pass
    for pull in datastore.get_proposed_pull_requests():
        # submit(pull)
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))