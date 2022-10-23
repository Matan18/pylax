# --------------- BUILT-IN PACKAGES ---------------

# --------------- PERSONAL PACKAGES ---------------
from model.instances.calax import calax

# --------------- DISCORD PACKAGES ---------------
from discord.channel import (
    TextChannel
)
from discord.message import (
    Message
)

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
        # if exception.code == 10008:
            # print('Auth-message not found')
        print(exception)