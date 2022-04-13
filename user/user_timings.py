import math
import time

class UserTimings:
    command_timeout_seconds = {
        "default": 600,
        "!songrequest": 600
    }
    def __init__(self):
        self.users = {}

    def get_command_timeout(self, command_name):
        if command_name in self.command_timeout_seconds:
            return self.command_timeout_seconds[command_name]
        return self.command_timeout_seconds["default"]

    def update_command_for_user(self, username, command_name):
        if username not in self.users:
            self.users[username] = {}
        self.users[username][command_name] = time.time()

    def valid_command_for_user(self, username, command_name):
        if username not in self.users:
            return 0
        if command_name not in self.users[username]:
            return 0
        timeout = self.get_command_timeout(command_name)
        user_timeout = self.users[username][command_name]
        return timeout - (math.ceil(time.time()) - math.ceil(user_timeout))
    
    def to_string(self):
        for key in self.users:
            print(key)
            for key_2 in self.users[key]:
                print(key_2 + " " + str(self.users[key][key_2]))
            print()