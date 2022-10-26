# --------------- BUILT-IN PACKAGES ---------------
from dotenv import load_dotenv, find_dotenv, set_key
import os

# --------------- DISCORD PACKAGES ---------------
import discord
from discord.ext.commands.context import (
    Context
)
from discord import (
    TextChannel
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
from util import ROOT_PATH
from util.room import (
    findRoomInpylaxByPlayerId
)

@pylax.bot.command()
async def add_auth_message(
    context: Context
):
    await context.message.delete()
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    if player.id in [room.game.bot_master.id for room in pylax.rooms]:
        print('Enviando imagem...')
        load_dotenv()
        id_auth_message: str = os.getenv('id_auth_channel')
        auth_channel: TextChannel = pylax.bot.get_channel(int(id_auth_message))

        # Delete all messages in the channel
        await auth_channel.purge()

        image_path: str = f'{ROOT_PATH}/src/image/pylax_banner.png'
        with open(image_path, 'rb') as file:
            auth_image = discord.File(file)

        message = await auth_channel.send(file=auth_image)
        await message.add_reaction("👍")

        # Store the new message id
        pylax.id_auth_message = str(message.id)
        dotenv_file: str = find_dotenv()
        set_key(dotenv_file, 'id_auth_message', str(message.id))