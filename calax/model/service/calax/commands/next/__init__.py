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
from model.instances.calax import (
    calax
)
from model.service.calax.commands.start import (
    start
)
from util.room import (
    findRoomInCalaxByPlayerId
)

# Go to the next round
@calax.bot.command()
async def next(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            await context.send('⏩ | Pulando para o próximo participante...')
            room.game.fase_controller = 0
            await start(context)
            break