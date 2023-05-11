# fitbit-dash-jms
An interactive dashboard showing James Twose's fitbit data over time

## How to run
- `flask run` to run the data pulling
- open `http://127.0.0.1:5000/` in a browser to see the dashboard
- click login and login with your fitbit account
- if this functions correctly (the redirect is not set up correctly yet) you need to remove the end of the url and go back to `http://127.0.0.1:5000/`
- you should see dates being pulled in the terminal
- BE AWARE: the fitbit API has a max call of 150 per hour, so if you have a lot of data it will take a while to pull it all in