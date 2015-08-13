""" Instantiates bots, schedules them,runs them etc."""

import sys


from spell_check_bot import SpellCheckBot
import models
import datastore


def main():
	# Run the analysis bot
	spell_check_bot = SpellCheckBot(models.Account(
		sys.argv[1], sys.argv[2], sys.argv[3]))
	datastore.load_data(spell_check_bot)
	for bot in datastore.get_bots():
		for repo in datastore.get_repos_signed_up_for_bot(bot):
			if bot.ready_to_analyze(repo):
				bot.analyze(repo)
			else: 
				# TODO check whether the repo should be 
				# forked / cloned
				pass
	for pull in datastore.get_proposed_pull_requests():
		pull.submit()
	return 0

if __name__ == '__main__':
	sys.exit(main())