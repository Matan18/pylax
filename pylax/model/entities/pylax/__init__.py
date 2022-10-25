from discord.ext.commands import Bot
from model.entities.room import Room
from model.entities.player import Player

class Pylax:

    def __init__(
        self,
        id_auth_message: str,
        id_auth_channel: str,
        bot_token: str,
        bot: Bot
    ):
        self.id_auth_message: str = id_auth_message
        self.id_auth_channel: str = id_auth_channel
        self.bot_token: str = bot_token
        self.bot: Bot = bot
        self.rooms: list[Room] = []

    def addRoom(self, room: Room) -> None:
        self.rooms.append(room)