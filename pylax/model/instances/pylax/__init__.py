# --------------- BUILT-IN PACKAGES ---------------
from dotenv import load_dotenv
import json
import os


# --------------- DISCORD PACKAGES ---------------
import discord
from discord.ext import (
    commands
)

# --------------- PERSONAL PACKAGES ---------------
from model.entities.pylax import Pylax
from model.entities.game import Game
from model.entities.room import Room
from model.entities.player import Player
from util import ROOT_PATH

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

pylax = Pylax(
    id_auth_message = id_auth_message,
    id_auth_channel = id_auth_channel,
    bot_token = TOKEN,
    bot = bot
)

# Load rooms informations
rooms_path: str = f'{ROOT_PATH}/src/json/rooms.json'
with open(
        file = rooms_path,
        mode = 'r'
    ) as rooms_as_json:
    rooms: list[dict[str, str]] = json.load(rooms_as_json)

# Add all games to pylax
for room in rooms:
    pylax.addRoom(
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