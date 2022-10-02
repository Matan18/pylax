from discord.ext.commands import Bot
from model.entities.room import Room
from model.entities.player import Player

class Calax:

    def __init__(
        self,
        id_auth_message: str,
        id_auth_channel: str,
        bot_token: str,
        bot: Bot
    ):
        self.__id_auth_message: str = id_auth_message
        self.__id_auth_channel: str = id_auth_channel
        self.__bot_token: str = bot_token
        self.__bot: Bot = bot
        self.__rooms: list[Room] = []

    @property
    def id_auth_message(self) -> str:
        return self.__id_auth_message

    @id_auth_message.setter
    def id_auth_message(self, id_auth_message: str) -> None:
        self.__id_auth_message = id_auth_message

    @property
    def id_auth_channel(self) -> str:
        return self.__id_auth_channel

    @id_auth_channel.setter
    def id_auth_channel(self, id_auth_channel: str) -> None:
        self.__id_auth_channel = id_auth_channel

    @property
    def bot_token(self) -> str:
        return self.__bot_token
    
    @bot_token.setter
    def bot_token(self, bot_token: str) -> None:
        self.__bot_token = bot_token

    @property
    def bot(self) -> Bot:
        return self.__bot

    @property
    def rooms(self) -> list[Room]:
        return self.__rooms

    @rooms.setter
    def rooms(self, rooms: list[Room]) -> None:
        self.__rooms = rooms

    def addRoom(self, room: Room) -> None:
        self.__rooms.append(room)