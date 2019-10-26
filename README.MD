# Reddit Gitbot

This is a Reddit bot built with PRAW to check Reddit comments for erroneous git commands.

## Prerequisites

If you want to try out the bot locally, you only need to install [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html). If the app is to be deployed directly to Heroku, all needed modules are described in the requirements.txt file.

## Deployment

### First steps

First you would probably want to create a new Reddit account for your bot.

* Go to [Reddit](https://www.reddit.com/) and create an account.
* Login and go to Preferences > Apps and click "create another app..."
* Type a name for your app and choose "script". Add a description and provide the "about" and "redirect" URIs.

Next, you will need to create a new heroku account if you don't have one already.

* Go to [Heroku](https://www.heroku.com/) and create an account.
* Create a Heroku app.
* Download and install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
* Open Bash or CMD and login to Heroku CLI ```$ heroku login```.

### Pre-deployment

* Clone the current repository to your local storage.
* Rename the folder name to anything you need.
* Open the friendbot.py and hintbot.py files and add your Reddit user and app info.
* Make changes to both of these files to suit your needs.

### Deployment

* Open Bash or CMD and cd to your project folder.
* Change your remote to ```$ heroku git:remote -a your_heroku_app_name```
* Add a buildpack to Heroku so it can understand that this is a Python app. ```heroku buildpacks:set heroku/python```
* Commit your changes. ```git add .```, ```git commit -m "Ready to be deployed"```.
* Deploy your app by typing ```git push heroku master```.

### Post-deployment

* Go to [Heroku](https://www.heroku.com/) and go to you app administration.
* Select "Resources" and press the pen button beside your dyno.
* Change the slider to active and press confirm. 
* Press "More" on the top right corner and then "View Logs".
* There should be a line ```State changed from starting to up```, that means that your app is up and running.