from discord.ext.commands import (
    Context
)

from model.entities.player import Player

class Game:

    def __init__(
        self, bot_master: Player
    ):
        self.asker: Player = None
        self.bot_master: Player = bot_master
        self.fase_controller: int = 0
        self.id_voting_message: str = None
        self.is_victim_a_asker: bool = None
        # Store this context to start next matchs by itself
        self.master_context: Context = None
        self.last_context: Context = None
        self.players: list[Player] = []
        self.players_pointer: int = 0
        self.victim: Player = None
        self.votes: list[Player] = []

    def addVote(self, player: Player) -> None:
        self.votes.append(player)

    def addPlayer(self, player: Player) -> None:
        self.players.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.players:
            if player.id == id_player:
                self.players.remove(player)