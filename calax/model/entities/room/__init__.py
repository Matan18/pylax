from model.entities.player import Player

class Room:
    def __init__(
        self,
        id_txt_channel: str,
        id_voice_channel: str,
        players:list[Player]
    ):
        self.__id_txt_channel: str = id_txt_channel
        self.__id_voice_channel: str = id_voice_channel
        self.__players: list[Player] = players

    @property
    def id_txt_channel(self) -> str:
        return self.__id_txt_channel

    @id_txt_channel.setter
    def id_txt_channel(self, id_txt_channel: str) -> None:
        self.__id_txt_channel = id_txt_channel
        
    @property
    def id_voice_channel(self) -> str:
        return self.__id_voice_channel

    @id_voice_channel.setter
    def id_voice_channel(self, id_voice_channel: str) -> None:
        self.__id_voice_channel = id_voice_channel
    
    @property
    def players(self) -> list[Player]:
        return self.__players

    def addPlayer(self, player: Player) -> None:
        self.__players.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.players:
            if player.id == id_player:
                self.players.remove(player)