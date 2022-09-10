from model.entities.player import Player

class Room:
    def __init__(
        self,
        id_txt_channel: str,
        id_voice_channel: str,
        playersInside:list[Player]
    ):
        self.__id_txt_channel: str = id_txt_channel
        self.__id_voice_channel: str = id_voice_channel
        self.__playersInside: list[Player] = playersInside

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
    def playersInside(self) -> list[Player]:
        return self.__playersInside

    def addPlayer(self, player: Player) -> None:
        self.__playersInside.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.playersInside:
            if player.id == id_player:
                self.playersInside.remove(player)