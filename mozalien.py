import argparse
from getpass import getpass
import feedparser
import importlib
import praw
from time import sleep

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--settings-path', default='settings', help='The location of the settings file.')
	parser.add_argument('-l', '--submission-limit', type=int, help='The maximum number of entries that will be submitted to each subreddit. (If the settings file specifies submission limits for particular subreddits, the minimum of the two will be used.)')
	parser.add_argument('-t', '--throttle', type=float, help='The number of seconds to wait between submissions.')
	parser.add_argument('-d', '--dry-run', action='store_true', help='Retrieves feed data as usual, but prints the entries that would be submitted instead of submitting them.')
	parser.add_argument('-v', '--verbose', action='store_true', help='Prints all submittable entries it submits them. Implied by --dry-run.')
	parser.add_argument('-i', '--client-id', help='The Reddit client ID.')
	parser.add_argument('-e', '--client-secret', help='The Reddit client secret.')
	parser.add_argument('-a', '--user-agent', help='The user agent used when making web requests.')
	parser.add_argument('-n', '--username', help='The Reddit username.')
	parser.add_argument('-p', '--password', help='The Reddit password. Use of this argument is discouraged. (You will be given a more secure prompt to enter the password unless you provide it here or in your settings file.)')
	args = {k: v for k, v in vars(parser.parse_args()).items() if v}
	settings = importlib.import_module(args['settings_path']).settings
	settings.update(args)
	settings.setdefault('submission_limit', 1000)
	settings.setdefault('password', getpass('Reddit password: '))

	red = praw.Reddit(client_id=settings['client_id'], client_secret=settings['client_secret'], user_agent=settings['user_agent'], username=settings['username'], password=settings['password'])
	for subreddit in settings['subreddits']:
		sub = red.subreddit(subreddit['name'])
		for feed in (reversed(feedparser.parse(feed).entries) for feed in subreddit['feeds']):
			submitted = 0
			submission_limit = min(settings['submission_limit'], subreddit.get('submission_limit', 1000))
			links = [entry.link for entry in feed]
			existing_submissions = red.info(links)
			# DEBUG
			print(list(existing_submissions))
			exit()
			for i, entry in enumerate(entries):
				# print(f'DEBUG: considering submitting "{entry.title}"')
				if not existing_submissions[i]:
					submit(sub, entry, submit=not dry_run, print_=dry_run or settings['verbose'])
					submitted += 1
				entry = next(feed)
		sleep(settings['throttle'])

def submit(subreddit, entry, submit=True, print_=False):
	if submit:
		submission = subreddit.submit(title=entry.title, url=entry.link)
	if print_:
		print(f'"{entry.title}" <{entry.link}> to r/{subreddit.display_name} <{submission.short_link if submit else None}>', end='')

if __name__ == '__main__':
	main()
