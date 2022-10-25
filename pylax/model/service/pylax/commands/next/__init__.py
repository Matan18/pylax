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
from model.service.pylax.commands.start import (
    start
)
from util.room import (
    findRoomInpylaxByPlayerId
)

# Go to the next round
@pylax.bot.command()
async def next(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    for room in pylax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            await context.send('⏩ | Pulando para o próximo participante...')
            room.game.fase_controller = 0
            await start(context)
            break