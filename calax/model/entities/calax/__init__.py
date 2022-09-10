class Calax:
    def __init__(
        self, id_auth_message: str, id_auth_channel: str, bot_token: str
    ):
        self.__id_auth_message: str = id_auth_message
        self.__id_auth_channel: str = id_auth_channel
        self.__bot_token: str = bot_token

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
    