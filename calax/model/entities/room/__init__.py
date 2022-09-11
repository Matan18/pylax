from model.entities.player import Player
from model.entities.game import Game

class Room:
    __players: list[Player] = []

    def __init__(
        self,
        id_txt_channel: str,
        id_voice_channel: str,
        game: Game
    ):
        self.__id_txt_channel: str = id_txt_channel
        self.__id_voice_channel: str = id_voice_channel
        self.__game: Game = game

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
    
    @property
    def game(self) -> Game:
        return self.__game
    
    @game.setter
    def game(self, room: Game) -> None:
        self.__game = game

    def addPlayer(self, player: Player) -> None:
        self.__players.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.players:
            if player.id == id_player:
                self.players.remove(player)