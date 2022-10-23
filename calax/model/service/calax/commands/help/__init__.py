# --------------- BUILT-IN PACKAGES ---------------
import json
from random import (
    choice
)

# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import (
    Player
)
from model.entities.room import (
    Room
)
from model.instances.calax import (
    calax
)
from util import ROOT_PATH
from util.room import (
    findRoomInCalaxByPlayerId
)

# Command to be used when asker doesn't know what to ask
@calax.bot.command()
async def help(context: Context):
    questions_path: str = f'{ROOT_PATH}/src/json/questoes.json'
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 3 and\
        room.game.asker.id == player.id:
            with open(
                file = questions_path,
                mode = 'r',
                encoding = 'utf-8'
            ) as questions_as_json:

                questions_as_dict: dict[str, list[str]] = json.load(questions_as_json)
                # It chooses a question
                chosen_question = choice(questions_as_dict[room.game.victim.response])
                await context.send(f'<@{room.game.victim.id}>, {chosen_question}')
                break
            

# --------------- ALIASES ---------------
def help_aliases() -> None:
    @calax.bot.command()
    async def ajuda(context: Context):
        await help(context)

    @calax.bot.command()
    async def ajd(context: Context):
        await help(context)