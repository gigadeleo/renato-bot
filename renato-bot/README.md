renato-bot
=============
'renato' is a Slack Bot written in Python who helps you learn a new Maltese word every day.

Installation & Setup
-----------
If you've never built a test bot it is recommended that you learn the basics. Go to [Full Stack Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) for a basic tutorial on how to build a basic Python Slack bot using the official Python-Slack API.

* Install and activate a new [virtualenv](http://virtualenv.readthedocs.org/en/latest/) to isolate your application dependencies from other Python projects.
	`virtualenv renato-bot`
	`source renato-bot/bin/activate`

* Install the [Official Python-Slack API](https://github.com/slackapi/python-slackclient)
	`pip install slackclient`

* Download and enable this bot
	`git add -f git://github.com/gigadeleo/renato-bot.git` ## TOCHECK

* Install all dependencies required by renato ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) 	`pip install -r requirements.txt`

* Obtain an [access token](https://api.slack.com/bot-users) from your Slack team so your bot can use it to connect to the Slack API. Remember to name your bot 'renato'.

* Rename tokens.conf.sample into tokens.conf in the same directory and copy the newly-generated access-token into 'tokens.conf'

* Obtain your bot_id and copy it to tokens.conf

* Start
	`python renato.py`

Running as a Deamon
-----------
If you plan on running renato-bot for long periods of time, you may consider using a process manager
daemon such as [supervisor](http://supervisord.org/) to start and stop renato-bot. A supervisor tutorial is available
[here](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps).

License
-----------
renato-bot is licensed under the MIT License:
  - http://opensource.org/licenses/mit-license.html

Attribution is not required, but much appreciated:
  - `renato-bot by @gigadeleo`

Sources
-----------