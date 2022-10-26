# --------------- BUILT-IN PACKAGES ---------------


# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import (
    Player
)
from model.entities.room import (
    Room
)
from model.instances.pylax import (
    pylax
)
from model.service.pylax.commands.show_players import (
    showListOfPlayers
)
from util.room import (
    findRoomInpylaxByPlayerId
)

# Starts the turn
@pylax.bot.command()
async def start(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    bot_masters: list[Player] = [room.game.bot_master for room in pylax.rooms]
    if player.id in [bot_master.id for bot_master in bot_masters]:
        for room in pylax.rooms:
            if str(context.channel.id) == room.id_txt_channel:
                room.game.master_context = context
                punished_player_ids: list[str] =\
                    [punished_playes.id for punished_playes in room.game.punished_players]
                if room.game.fase_controller == 0\
                and len([player for player in room.game.players if player.id not in punished_player_ids]) > 1:
                    # [REFACTOR IT]
                    while room.game.players[room.game.players_pointer].id in punished_player_ids:
                        if room.game.players_pointer < len(room.game.players) - 1:
                            room.game.players_pointer += 1
                        else:
                            room.game.players_pointer = 0
                    room.game.asker = room.game.players[room.game.players_pointer]
                    # Every new game goes to the next player;
                    # if the next player is the last one, it goes
                    # to the first one
                    if room.game.players_pointer < len(room.game.players) - 1:
                        room.game.players_pointer += 1
                    else:
                        room.game.players_pointer = 0
                    # Check if the next arker will not be a punished player
                        

                    # Shows which people are in the game
                    await showListOfPlayers(context = context)
                    await context.send(f'\n<@{room.game.asker.id}> gire a garrafa.')
                    room.game.fase_controller = 1
                    break
                else:
                    await context.send(f'🟥 | Não é possível inciar uma partida agora. Veja o número de jogadores ou em que fase estamos.')
                break

# --------------- ALIASES ---------------
def start_aliases() -> None:
    @pylax.bot.command()
    async def iniciar(context: Context):
        await start(context)

    @pylax.bot.command()
    async def comecar(context: Context):
        await start(context)

    @pylax.bot.command()
    async def começar(context: Context):
        await start(context)