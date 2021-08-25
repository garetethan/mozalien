import argparse
from getpass import getpass
import feedparser
import importlib
import praw
import re
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
	parser.add_argument('-p', '--password', help='The Reddit password. Use of this argument is discouraged. (You will be given a more secure prompt to enter the password unless you provide it in your settings file or here.)')
	args = {k: v for k, v in vars(parser.parse_args()).items() if v}
	settings = importlib.import_module(args['settings_path']).settings
	settings.update(args)
	settings.setdefault('submission_limit', 1000)
	settings.setdefault('password', getpass('Reddit password: '))

	red = praw.Reddit(client_id=settings['client_id'], client_secret=settings['client_secret'], username=settings['username'], password=settings['password'], user_agent=settings['user_agent'])
	for sub_data in settings['subreddits']:
		if settings['verbose']:
			print(f'Checking r/{sub_data["name"]}...')
		sub = red.subreddit(sub_data['name'])
		try:
			limit = min(settings['submission_limit'], sub_data['submission_limit'])
		except KeyError:
			limit = settings['submission_limit']
		feeds = list(feedparser.parse(feed).entries for feed in sub_data['feeds'])
		combined_feed = sorted(list(entry for feed in feeds for entry in feed), key=lambda entry: entry.published_parsed, reverse=True)
		latest_submitted = 0
		try:
			while not next(red.info(url=combined_feed[latest_submitted].link), None):
				latest_submitted += 1
		except IndexError:
			pass

		for entry in reversed(combined_feed[max(latest_submitted - limit, 0) : latest_submitted]):
			submit(sub, entry, submit=not settings['dry_run'], print_=settings['dry_run'] or settings['verbose'])
			sleep(settings['throttle'])

def submit(subreddit, entry, submit=True, print_=False):
	if submit:
		submission = subreddit.submit(title=entry.title, url=entry.link, resubmit=False)
	if print_:
		if submit:
			print(f'Submitted "{entry.title}" <{entry.link}> to r/{subreddit.display_name}: https://redd.it/{submission.id}')
		else:
			print(f'Would submit "{entry.title}" <{entry.link}> to r/{subreddit.display_name}')

if __name__ == '__main__':
	main()
