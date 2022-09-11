from model.entities.player import Player
from model.entities.room import Room
from model.entities.calax import Calax
from model.instances.calax import calax

from model.service.calax.events import(
  on_ready
)

from discord.ext.commands import Context

from util import ROOT_PATH


if __name__ == '__main__':
    calax.bot.run(token = calax.bot_token)