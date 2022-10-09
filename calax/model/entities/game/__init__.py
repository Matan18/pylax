from discord.ext.commands import (
    Context
)

from model.entities.player import Player

class Game:

    def __init__(
        self, bot_master: Player
    ):
        self.__asker: Player = None
        self.__bot_master: Player = bot_master
        self.__fase_controller: int = 0
        self.__id_voting_message: str = None
        self.__is_victim_a_asker: bool = None
        # Store this context to start next matchs by itself
        self.__master_context: Context = None
        self.__last_context: Context = None
        self.__players: list[Player] = []
        self.__players_pointer: int = 0
        self.__victim: Player = None
        self.__votes: list[Player] = []
    
    @property
    def asker(self) -> Player:
        return self.__asker
    
    @asker.setter
    def asker(self, asker: Player) -> None:
        self.__asker = asker
    
    @property
    def bot_master(self) -> Player:
        return self.__bot_master
    
    @bot_master.setter
    def bot_master(self, bot_master: Player) -> None:
        self.__bot_master = bot_master

    @property
    def fase_controller(self) -> int:
        return self.__fase_controller

    @fase_controller.setter
    def fase_controller(self, fase_controller: int) -> None:
        self.__fase_controller = fase_controller

    @property
    def id_voting_message(self) -> str:
        return self.__id_voting_message

    @id_voting_message.setter
    def id_voting_message(self, id_voting_message: str) -> None:
        self.__id_voting_message = id_voting_message

    @property
    def is_victim_a_asker(self) -> bool:
        return self.__is_victim_a_asker

    @is_victim_a_asker.setter
    def is_victim_a_asker(self, is_victim_a_asker: bool) -> None:
        self.__is_victim_a_asker = is_victim_a_asker

    @property
    def last_context(self) -> Context:
        return self.__last_context

    @last_context.setter
    def last_context(self, last_context: Context) -> None:
        self.__last_context = last_context

    @property
    def master_context(self) -> Context:
        return self.__master_context

    @master_context.setter
    def master_context(self, master_context: Context) -> None:
        self.__master_context = master_context

    @property
    def players(self) -> list[Player]:
        return self.__players
    
    @players.setter
    def players(self, players: list[Player]) -> None:
        self.__players = players
    
    @property
    def players_pointer(self) -> int:
        return self.__players_pointer

    @players_pointer.setter
    def players_pointer(self, players_pointer: int) -> None:
        self.__players_pointer = players_pointer

    @property
    def victim(self) -> Player:
        return self.__victim
    
    @victim.setter
    def victim(self, victim: Player) -> None:
        self.__victim = victim

    @property
    def votes(self) -> list[Player]:
        return self.__votes

    @votes.setter
    def votes(self, votes: list[Player]) -> None:
        self.__votes = votes

    def addVote(self, player: Player) -> None:
        self.__votes.append(player)

    def addPlayer(self, player: Player) -> None:
        self.__players.append(player)

    def removePlayer(self, id_player: str) -> None:
        for player in self.players:
            if player.id == id_player:
                self.players.remove(player)