"""An interface to interactact with the common data-store shared 
between various bots and the fetcher bot

Currently, the data-store is simply in memory and acts more or less 
as a stub, but we plan to have the information in a database that 
can be accessed through this module.

May change into class if necessary for maintaining the database 
connections.
"""

import tempfile
import models


# TODO All of the following are supposed to be stored into database later
# currently just a temp dir
BASE_DIR = tempfile.mkdtemp() # TODO set this from a config file
# currently a in-memory git-hub repo id to local repo path mapping
url2dir = {}                  # TODO change to database table 
# currently the population is triggered by runtime with command line 
# args
bots = []                     # TODO load these based on database entries
# bots will add their proposed pulls to this pile
proposed_pulls = []

def load_data(bot):
	"""currently a stub to load necessary information

	This should not be needed in the future as information will
	be stored in a database
	"""
	bots.append(bot)

def get_repos_signed_up_for_bot(bot):
	"""return a list of data_wrappers.Repo that has sigh up to the 
	given bot
	"""
	# TODO hook to the sign up database
	# This is currently a stub for the spelling bot
	return 


def get_repo_dir(url):
    """return the directory path of the project associated with url."""
    if url in url2dir:
        return url2dir[url]
    else:
    	# TODO change this to be using a more permenant data storage
    	#      store the path to the local repo and the repo id on 
    	#      github
        dir_path = tempfile.mkdtemp(dir=BASE_DIR) 
        url2dir[url] = dir_path
        return dir_path

def get_bots():
	"""return a list of available bots"""
	return bots

def get_proposed_pull_requests():
	"""return a list of proposed pull requests that have not been 
	processed
	"""
	return proposed_pulls

def propose_pull(bot, repo, branch_name, title, body):
	"""propose a pull request and enter it into the data-store
	to be reviewed by the runtime
	"""
	proposed_pulls.append(models.PullRequest(bot, 
		repo, branch_name, title, body);