from getpass import getpass
import feedparser
import praw
from sys import argv

from settings import settings

def main():
	dry_run = '-d' in argv or '--dry-run' in argv
	red = praw.Reddit(client_id=settings['client_id'], client_secret=settings['client_secret'], user_agent=settings['user-agent'], username=settings['username'], password=getpass('Reddit password: '))
	for subreddit in settings['subreddits']:
		sub = red.subreddit(subreddit['name'])
		feed_entries = [reversed(feedparser.parse(feed).entries) for feed in subreddit['feeds']]
		for feed in feed_entries:
			for entry in feed:
				print(f'DEBUG: considering submitting "{entry}"')
				try:
					next(r.info(entry.link))
				except StopIteration:
					if dry_run:
						dry_submit(sub, entry)
					else:
						submit(sub, entry)

def dry_submit(subreddit, entry):
	print(f'Submitted "{entry.title}" to r/{subreddit.display_name}.')

def submit(subreddit, entry):
	submission = subreddit.submit(title=entry.title, url=entry.link)
	print(f' "{entry.title}" ({submission.short_link}).')

if __name__ == '__main__':
	main()
