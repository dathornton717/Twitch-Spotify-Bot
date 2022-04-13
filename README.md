# Twitch-Spotify-Bot
This repository is used to queue up songs to a Spotify account view Twitch chat commands. There is a little setup that is required to get this working.

## Requirements
* Spotify Premium
* Python3 (https://www.python.org/downloads/)
* Pip3 (https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/)

If you are using Windows 10 or above I would recommend using Linux via "Ubuntu on Windows"

## Setup
1. Go to https://developer.spotify.com/dashboard/applications and sign in to your Spotify account
2. Click on the "Create An App" button and name the app anything
3. You should see a Client ID and a Client Secret. Copy and paste those into the .env file as SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
4. Click on the "Edit Settings" button
5. Under "Redirect URIs" add "https://www.google.com" and save
6. Go to https://accounts.spotify.com/authorize?response_type=code&client_id=<CLIENT_ID>&scope=user-read-currently-playing+streaming&redirect_uri=https://www.google.com (fill in the <CLIENT_ID> with your client id)
7. It should redirect you to sign into your Spotify account. Once you do that you should be redirected to https://www.google.com/?code=<Some_really_long_code>
8. Copy the really long code and paste it into the SPOTIFY_API_CODE field in the .env file
9. Run `python3 utils/access_token.py` in your terminal
10. That should print out a long message
11. Copy everything after "refresh_token:" and paste it in the .env file as SPOTIFY_REFRESH_TOKEN
12. Generate a Twitch Auth Token via https://twitchapps.com/tmi/ and paste it as TWITCH_AUTH_TOKEN
13. Set TWITCH_COMMAND_PREFIX to anything you want. I use !
14. Set TWITCH_CHANNEL to your Twitch channel name
15. Run `python3 bot.py`
16. Go to your chat and try commands such as `!currently_playing`, `!song_request "Linkin Park" "In the End"`
