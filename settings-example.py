settings = {
	'client_id': 'foo',
	'client_secret': 'foo',
	'username': 'foo',
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
		},
	],
}

settings['user-agent'] = f'mozalien (by u/{settings["username"]})'
