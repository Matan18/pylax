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
from model.instances.pylax import (
    pylax
)
from util.room import (
    findRoomInpylaxByPlayerId
)

# Kick player
@pylax.bot.command()
async def kick(
    context: Context,
    id_kick_player: str = '',
    option: str = '2'
):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    async def fromGame(room: Room):
        room.game.removePlayer(id_kick_player)

    async def fromRoom(room: Room):
        room.removePlayer(id_kick_player)
        id_auth_message: str = pylax.id_auth_message
        auth_channel: TextChannel = pylax.bot.get_channel(int(pylax.id_auth_channel))
        auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
        await auth_message.remove_reaction("👍", pylax.bot.get_user(int(id_kick_player)))

    async def fromEverywhere(room: Room):
        await fromGame(room)
        await fromRoom(room)

    for room in pylax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            places = [fromGame, fromRoom, fromEverywhere]
            try:
                await places[int(option)](room)
            except Exception as exception:
                print(exception)
            break