# Personal packages
from model.entities.calax import Calax

# External packges
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: str = os.getenv('TOKEN')
id_auth_message: str = os.getenv('id_auth_message')
id_auth_channel: str = os.getenv('id_auth_channel')

# Matan's solutions for the problem with not seeing
# the members in the channel
intents = discord.Intents().all()

bot = commands.Bot(
    command_prefix = '??',
    case_insensitive = True,
    intents = intents,
    help_command = None
)

calax = Calax(
    id_auth_message = id_auth_message,
    id_auth_channel = id_auth_channel,
    bot_token = TOKEN,
    bot = bot
)