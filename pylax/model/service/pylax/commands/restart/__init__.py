# --------------- BUILT-IN PACKAGES ---------------
from time import (
    sleep
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
from model.instances.pylax import (
    pylax
)
from util.room import (
    findRoomInpylaxByPlayerId
)

# Restart the game
@pylax.bot.command()
async def restart(context: Context):
    await context.message.delete()
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    for room in pylax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            room.game.fase_controller = 0
            room.game.players_pointer = 0
            room.game.asker = None
            room.game.victim = None
            room.game.punished_players = []
            for player in room.game.players: player.faults = 0
            
            message = await context.send("Reloading")
            clock_emojis: list[str] = [
                "🕛", "🕜", "🕑"
            ]
            for index, clock_emoji in enumerate(clock_emojis):
                await message.edit(
                    content = f'{clock_emoji} | Reloading' + '. ' * (index + 1)
                )
                sleep(.2)
            await message.edit(content="✅ | Done!")
            sleep(.2)
            await message.delete()
            break