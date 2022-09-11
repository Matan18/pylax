# Personal packages
from model.entities.calax import Calax
from model.entities.game import Game
from model.entities.room import Room
from model.entities.player import Player

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

rooms = [
    {
        'bot_master': '546840612972789782',
        'id_text_channel': '1018594639021875271',
        'id_voice_channel': '910507210906431498'
    },
    {
        'bot_master': '772066124052693013',
        'id_text_channel': '1018594664259006504',
        'id_voice_channel': '910518654926475274'
    }
]

# Add all games to calax
for room in rooms:
    calax.addRoom(
        Room(
            id_txt_channel = room['id_text_channel'],
            id_voice_channel = room['id_voice_channel'],
            game = Game(
                bot_master = Player(
                    room['bot_master']
                )
            )            
        )
    )