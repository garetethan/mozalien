settings = {
	'client_id': 'foo',
	'client_secret': 'foo',
	'username': 'foo',
	'limit': 5,
	'throttle': 10,
	'dry_run': False,
	'verbose': False,
	'subreddits': [
		{
			'name': 'Nodumbquestions',
			'feeds': [
				'https://nodumbqs.libsyn.com/rss'
			],
		},
		{
			'name': 'CGPGrey',
			'feeds': [
				'https://www.youtube.com/channel/UC2C_jShtL725hvbm1arSV9w',
				'https://www.youtube.com/channel/UC127Qy2ulgASLYvW4AuHJZQ',
			],
			'limit': 2,
		},
	],
}

settings['user_agent'] = f'mozalien (by u/{settings["username"]})'
