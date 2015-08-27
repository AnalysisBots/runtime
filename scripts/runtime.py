""" Instantiates bots, schedules them,runs them etc."""

import sys
import os
import json
import requests
import ipaddress

from flask import Flask, request, abort
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

# Webhook handling stuff. It looks like github3py has plans to make a better
# interface for handling webhook payload. It's unclear when that'll happen.
# The current implementation is largely borrowed and simplified from
# razius/github-webhook-handler. The functionality for checking webhook
# secret and use proxy is removed.

app = Flask(__name__)
app.debug = 'true'


def _handle_pull_request(payload):
    print("Hi")
    print(payload)
    return 'OK'


def _handle_payload(payload, event_type):
    if event_type == "ping":
        print(payload)
        return json.dumps({'msg': 'Hi, this is Analysis Bot!'})
    elif request.headers.get('X-GitHub-Event') == "pull-request":
        return _handle_pull_request(payload)
    else:
        return json.dumps({'msg': "wrong event type"})


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'OK'
    if request.method == 'POST':
        # Store the IP address of the requester
        if request.headers.getlist("X-Forwarded-For"):
            # TODO: use a more secure way to deal with proxy
            remote_addr = request.headers.getlist("X-Forwarded-For")[0]
        else:
            remote_addr = request.remote_addr
        request_ip = ipaddress.ip_address(u'{0}'.format(remote_addr))
        print("request_ip")
        print(request_ip)
        # get the hook address blocks from the API.
        whitelist = requests.get('https://api.github.com/meta').json()[
            'hooks']
        print(whitelist)

        # Check if the POST request is from github.com
        for ip in whitelist:
            if request_ip in ipaddress.ip_network(ip):
                break  # the remote_addr is within the network range of github.
        else:
            abort(403)  # the request is not sent from github

        return _handle_payload(json.loads(request.data.decode('utf-8')),
                               request.headers.get('X-GitHub-Event'))


def _start_web_hook_handler():
    """This is currently tested using ngrok for development"""
    # TODO make host and port customizable
    # TODO deal with proxy
    app.run()


if __name__ == '__main__':
    # sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
    _start_web_hook_handler()
