from model.instances.calax import calax
from model.entities.player import Player
from discord.channel import TextChannel
from discord.message import Message

@calax.bot.event
async def on_ready():
    # Adicionar todas as pessoas nas salas de voz no objeto sala
    id_auth_message: str = calax.id_auth_message
    id_auth_channel: str = calax.id_auth_channel
    print(f'id_auth_message: {id_auth_message}')
    print(f'id_auth_channel: {id_auth_channel}')
    channel: TextChannel = calax.bot.get_channel(int(id_auth_channel))
    message: Message = await channel.fetch_message(int(id_auth_message))
    await message.clear_reaction("👍")
    await message.add_reaction("👍")
    for room in calax.rooms:
        voice_channel = calax.bot.get_channel(int(room.id_voice_channel))
        voice_channel_members = voice_channel.members

        # Add player that is in game voice channel into its room
        ids_in_room: list[int] = [player.id for player in room.players]
        for voice_channel_member in voice_channel_members:
            # List all rooms to see if this player is in another one
            if str(voice_channel_member.id) in ids_in_room:
                room.addPlayer(
                    player = Player(str(voice_channel_member.id))
                )
    