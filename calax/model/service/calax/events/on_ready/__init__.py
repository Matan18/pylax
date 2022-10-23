# --------------- BUILT-IN PACKAGES ---------------

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import Player
from model.instances.calax import calax

# --------------- DISCORD PACKAGES ---------------
from discord.channel import (
    TextChannel,
    VoiceChannel
)
from discord.member import (
    Member
)
from discord.message import (
    Message
)

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
            voice_channel: VoiceChannel = calax.bot.get_channel(int(room.id_voice_channel))
            voice_channel_members: list[Member] = voice_channel.members

            # Add player that is in game voice channel into its room
            ids_in_room: list[str] = [player.id for player in room.players]
            if len(voice_channel_members) > 0:
                for voice_channel_member in voice_channel_members:
                    # List all rooms to see if this player is in another one
                    if not str(voice_channel_member.id) in ids_in_room:
                        # Bug appears in the following line
                        room.addPlayer(
                            player = Player(str(voice_channel_member.id))
                        )
            else:
                room.players = []

    except Exception as exception:
        if exception.code == 10008:
            print('Auth-message not found')
    print('Calax tá on! 😎')