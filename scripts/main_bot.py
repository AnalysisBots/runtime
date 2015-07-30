import os
import sys

from github3 import GitHub

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



# search and clone 10 repos of a specified GitHub user into the directory from 
# where this program is run
if __name__ == '__main__':
    for repo in GitHub().repositories_by(sys.argv[1], number=10):
        # TODO Use pygit2 to do the cloning later
        os.system("git clone {}".format(repo.clone_url))





