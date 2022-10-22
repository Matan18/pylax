from model.entities.player import Player
from model.entities.game import Game

class Room:

    def __init__(
        self,
        id_txt_channel: str,
        id_voice_channel: str,
        game: Game
    ):
        self.id_txt_channel: str = id_txt_channel
        self.id_voice_channel: str = id_voice_channel
        self.game: Game = game
        self.players: list[Player] = []

    def addPlayer(self, player: Player) -> None:
        self.players.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.players:
            if player.id == id_player:
                self.players.remove(player)