from model.instances.calax import calax
from model.entities.player import Player

from discord.member import (
    Member
)

from discord.ext.commands.context import (
    Context
)

@calax.bot.command()
async def show_players(context: Context):
    """Show which people are in the game.

    Parameters
    ----------
    context : Context
        Context for the called command.
    """
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    bot_masters: list[str] = [room.game.bot_master.id for room in calax.rooms]
    if player.id in bot_masters:
        for room in calax.rooms:
            if room.id_txt_channel == str(context.channel.id):
                message: list[str] = [
                    'Pessoas participando da brincadeira:',
                    *[f' - <@{player.id}>' for player in room.players]
                ]
                await context.send('\n'.join(message))
                break