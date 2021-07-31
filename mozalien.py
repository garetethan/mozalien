import argparse
from getpass import getpass
import feedparser
import importlib
import praw
from sys import argv

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('settings-path', default='settings.py', help='The location of the settings file.')
	parser.add_argument('-l', '--limit', type=int, help='The maximum number of entries that will be submitted to each subreddit. (If the settings file specifies limits for particular subreddits, the minimum of the two will be used.)')
	parser.add_argument('-d', '--dry-run', action='store_true', help='Retrieves feed data as usual, but prints the entries that would be submitted instead of submitting them.')
	parser.add_argument('-v', '--verbose', action='store_true', help='Prints all submittable entries it submits them. Implied by --dry-run.')
	parser.add_argument('-i', '--client-id', help='The Reddit client ID.')
	parser.add_argument('-s', '--client-secret', help='The Reddit client secret.')
	parser.add_argument('-a', '--user-agent', help='The user agent used when making web requests.')
	parser.add_argument('-n', '--username', help='The Reddit username.')
	parser.add_argument('-p', '--password', help='The Reddit password. Use of this argument is discouraged. (You will be given a more secure prompt to enter the password unless you provide it here or in your settings file.)')
	args = parser.parse_args()
	importlib.import(args['settings_path'])
	settings.update(args)
	settings.setdefault('password', getpass('Reddit password: '))

	red = praw.Reddit(client_id=settings['client_id'], client_secret=settings['client_secret'], user_agent=settings['user_agent'], username=settings['username'], password=settings['password'])
	for subreddit in settings['subreddits']:
		sub = red.subreddit(subreddit['name'])
		for feed in (reversed(feedparser.parse(feed).entries) for feed in subreddit['feeds']):
			entry = next(feed)
			limit = min(settings['limit'], subreddit['limit'])
			while submitted < limit:
				# print(f'DEBUG: considering submitting "{entry.title}"')
				try:
					next(red.info(entry.link))
				except StopIteration:
					submit(sub, entry, submit=not dry_run, print_=dry_run or settings['verbose'])
					submitted += 1
				entry = next(feed)

def submit(subreddit, entry, submit=True, print_=False):
	if submit:
		submission = subreddit.submit(title=entry.title, url=entry.link)
	if print_:
		print(f'"{entry.title}" <{entry.link}> to r/{subreddit.display_name} <{submission.short_link if submit else None}>', end='')

if __name__ == '__main__':
	main()
