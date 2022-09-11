from model.instances.calax import calax
from model.entities.player import Player
from model.entities.room import Room

from discord.channel import TextChannel
from discord.message import Message

@calax.bot.event
async def on_ready():
    id_auth_message: str = calax.id_auth_message
    id_auth_channel: str = calax.id_auth_channel
    try:
        channel: TextChannel = calax.bot.get_channel(int(id_auth_channel))
        message: Message = await channel.fetch_message(int(id_auth_message))
        # Clear all reaction in auth message
        await message.clear_reaction("👍")
        # Add first reaction in auth message
        await message.add_reaction("👍")
        for room in calax.rooms:
            voice_channel = calax.bot.get_channel(int(room.id_voice_channel))
            voice_channel_members = voice_channel.members

            # Add player that is in game voice channel into its room
            ids_in_room: list[str] = [player.id for player in room.players]
            for voice_channel_member in voice_channel_members:
                # List all rooms to see if this player is in another one
                if str(voice_channel_member.id) in ids_in_room:
                    room.addPlayer(
                        player = Player(str(voice_channel_member.id))
                    )
    except Exception as exception:
        if exception.code == 10008:
            print('Auth-message not found')

@calax.bot.event
async def close():
    id_auth_message: str = calax.id_auth_message
    id_auth_channel: str = calax.id_auth_channel
    try:
        channel: TextChannel = calax.bot.get_channel(int(id_auth_channel))
        message: Message = await channel.fetch_message(int(id_auth_message))
        # Clear all reaction in auth message
        await message.clear_reaction("👍")
        # Add first reaction in auth message
        await message.add_reaction("👍")
    except Exception as exception:
        if exception.code == 10008:
            print('Auth-message not found')

@calax.bot.event
async def on_message(message):
    player = Player(str(message.author.id))
    player.user = calax.bot.get_user(int(player.id))

    id_voice_channel: str = None
    id_text_channel: str = None
    id_bot_master: str = None
    auth_players: list[Player] = []
    # Check if was't Calax who sent it
    if str(calax.bot.user.id) != player.id:
        rooms: list[Room] = calax.rooms
        # Check if the message was sent in a game text channel
        if str(message.channel.id) in [room.id_txt_channel for room in rooms]:
            # Search in each room
            for room in rooms:
                # for the player who sent the mesage
                for player_in_room in room.players:
                    # If it's a player in a room, it stores its id_voice_channel and id_bot_master
                    if player_in_room == player.id:
                        id_voice_channel = room.id_voice_channel
                        id_text_channel = room.id_txt_channel
                        id_bot_master = room.game.bot_master
                        auth_players = room.game.players
                        break
                break
            # Auth-player or bot_master of this room
            if player.id in auth_players or player.id == room.game.bot_master.id:
                await calax.bot.process_commands(message)
            # Not auth-player
            else:
                await message.delete()
                await player.user.send(f'<@{player.id}>, você só pode mandar mensagem nesse chat se estiver jogando.')

        else:
            print('Message in other channel!')