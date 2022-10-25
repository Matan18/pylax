# --------------- BUILT-IN PACKAGES ---------------


# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import (
    Player
)
from model.instances.pylax import (
    pylax
)

async def showListOfPlayers(context: Context) -> None:
    """Show which people are in the game.

    Parameters
    ----------
    context : Context
        Context for the called command.
    """
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    bot_masters: list[str] = [room.game.bot_master.id for room in pylax.rooms]
    if player.id in bot_masters:
        for room in pylax.rooms:
            if room.id_txt_channel == str(context.channel.id):
                punished_player_ids: list[str] =\
                        [punished_playes.id for punished_playes in room.game.punished_players]
                message: list[str] = [
                    'Pessoas participando da brincadeira:',
                    *[f' - {"🚩" * player.faults} | ~~{player.user.name}~~'
                      if player.id in punished_player_ids
                      else f' - <@{player.id}>'
                      for player in room.game.players]
                ]
                await context.send('\n'.join(message))
                break

@pylax.bot.command()
async def show_players(context: Context):
    """Show which people are in the game.

    Parameters
    ----------
    context : Context
        Context for the called command.
    """
    await showListOfPlayers(context = context)