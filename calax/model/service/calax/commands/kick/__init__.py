# --------------- BUILT-IN PACKAGES ---------------


# --------------- DISCORD PACKAGES ---------------
from discord.channel import (
    TextChannel
)
from discord.ext.commands.context import (
    Context
)
from discord.message import Message

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
from util.room import (
    findRoomInCalaxByPlayerId
)

# Kick player
@calax.bot.command()
async def kick(
    context: Context,
    id_kick_player: str = '',
    option: str = '2'
):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    async def fromGame(room: Room):
        room.game.removePlayer(id_kick_player)

    async def fromRoom(room: Room):
        room.removePlayer(id_kick_player)
        id_auth_message: str = calax.id_auth_message
        auth_channel: TextChannel = calax.bot.get_channel(int(calax.id_auth_channel))
        auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
        await auth_message.remove_reaction("👍", calax.bot.get_user(int(id_kick_player)))

    async def fromEverywhere(room: Room):
        await fromGame(room)
        await fromRoom(room)

    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            places = [fromGame, fromRoom, fromEverywhere]
            try:
                await places[int(option)](room)
            except Exception as exception:
                print(exception)
            break