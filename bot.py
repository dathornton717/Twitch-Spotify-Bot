from dotenv import load_dotenv
from spotify.track import Track
from twitchio.ext import commands
from user.user_timings import UserTimings

import os
import random
import spotify.spotify as spotify

load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.getenv("TWITCH_AUTH_TOKEN"), prefix=os.getenv("TWITCH_COMMAND_PREFIX"), initial_channels=[os.getenv("TWITCH_CHANNEL")])
        self.user_timings = UserTimings()

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    @commands.command()
    async def currently_playing(self, ctx: commands.Context):
        track = spotify.get_currently_playing()
        if (track is None):
            await ctx.send(f"There is no song playing")
        else:
            await ctx.send(f"Currently Playing: \"{track.name}\" by {track.artist}")
    
    @commands.command()
    async def song_request(self, ctx: commands.Context, artist: str = None, track_name: str = None):
        command_name = "!songrequest"
        if artist == None or track_name == None:
            await ctx.send(f"Usage: !song_request \"<artist>\" \"<track-name>\"")
        else:
            username = ctx.author.name
            time_left = self.user_timings.valid_command_for_user(username, command_name)
            if time_left <= 0:
                tracks = spotify.search(artist, track_name, 10)
                track = spotify.queue_first_successful_song(tracks)
                self.user_timings.update_command_for_user(username, command_name)
                self.user_timings.to_string()
                await ctx.send(f"Successfully queued up \"{track.name}\" by {track.artist}")
            else:
                await ctx.send(self.request_song_try_again_message(command_name, time_left))

    @commands.command()
    async def random_song_from_artist(self, ctx: commands.Context, artist: str = None):
        command_name = "!songrequest"
        if artist == None:
            await ctx.send(f"Usage: !random_song_from_artist \"<artist>\"")
        else:
            username = ctx.author.name
            time_left = self.user_timings.valid_command_for_user(username, command_name)
            if time_left <= 0:
                tracks = spotify.search(artist, "", 100)
                random.shuffle(tracks)
                track = spotify.queue_first_successful_song(tracks)
                self.user_timings.update_command_for_user(username, command_name)
                self.user_timings.to_string()
                await ctx.send(f"Successfully queued up \"{track.name}\" by {track.artist}")
            else:
                await ctx.send(self.request_song_try_again_message(command_name, time_left))

    @commands.command()
    async def command_list(self, ctx: commands.Context):
        await ctx.send(f"Current commands: !currently_playing, !song_request, !random_song_from_artist")

    def seconds_to_string(self, timing):
        minutes = int(timing / 60)
        if minutes > 1:
            minutes_desc = "minutes"
        else:
            minutes_desc = "minute"
        seconds = timing - (minutes * 60)
        if seconds > 1:
            seconds_desc = "seconds"
        else:
            seconds_desc = "second"
        if minutes == 0:
            return f"{str(seconds)} {seconds_desc}"
        else:
            if seconds == 0:
                return f"{str(minutes)} {minutes_desc}"
            else:
                return f"{str(minutes)} {minutes_desc} and {str(seconds)} {seconds_desc}"

    def request_song_try_again_message(self, command_name, timing):
        time_left = self.seconds_to_string(timing)
        command_time = self.seconds_to_string(self.user_timings.get_command_timeout(command_name))
        return f"You may only request a song once every {command_time}, you have {time_left} remaining until you can request your next song"

bot = Bot()
bot.run()