# --------------- BUILT-IN PACKAGES ---------------

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import Player
from model.instances.pylax import pylax

# --------------- DISCORD PACKAGES ---------------
from discord.channel import (
    TextChannel
)
from discord.member import (
    Member,
    VoiceState
)
from discord.message import (
    Message
)

@pylax.bot.event
async def on_voice_state_update(
    context: Member,
    before: VoiceState,
    after: VoiceState
):

    player = Player(str(context.id))
    player.user = pylax.bot.get_user(int(player.id))
    game_voice_channels: str = [room.id_voice_channel for room in pylax.rooms]

    # Got into a voice channel
    if before.channel == None:
        # Check if it's a game channel
        if str(after.channel.id) in game_voice_channels:
            # ADD IT INTO ITS ROOM
            for room in pylax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break

    # Got out from a voice channel just
    elif before.channel != None and after.channel == None:
        # Check if it's from a game channel
        if str(before.channel.id) in game_voice_channels:

            # REMOVE IT FROM ITS ROOM
            id_auth_message: str = pylax.id_auth_message
            auth_channel: TextChannel = pylax.bot.get_channel(int(pylax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in pylax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break

    # Changed its voice channel
    elif before.channel != None and after.channel != None:
        # Check if it was from a game channel to another game channel
        if str(before.channel.id) in game_voice_channels and\
            str(after.channel.id) in game_voice_channels and\
            before.channel.id != after.channel.id:

            # REMOVE IT FROM ITS ROOM
            id_auth_message: str = pylax.id_auth_message
            auth_channel: TextChannel = pylax.bot.get_channel(int(pylax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in pylax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break

            # ADD IT INTO ITS ROOM
            for room in pylax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break

        # Check if it was not from a game channel to a game channel
        elif str(before.channel.id) not in game_voice_channels and\
            str(after.channel.id) in game_voice_channels:

            # ADD IT INTO ITS ROOM
            for room in pylax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break
            
        # Check if it was from a game channel to a not game channel
        elif str(before.channel.id) in game_voice_channels and\
            str(after.channel.id) not in game_voice_channels:
             # REMOVE IT FROM ITS ROOM
            id_auth_message: str = pylax.id_auth_message
            auth_channel: TextChannel = pylax.bot.get_channel(int(pylax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in pylax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break