# --------------- BUILT-IN PACKAGES ---------------


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

@pylax.bot.command()
async def status(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    for room in pylax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            # Build the status message
            message_list: list[str] = []
            message_list.append(
                '**ROOM**'
            )
            message_list.append(
                f'**Bot master**: <@{room.game.bot_master.id}>'
            )
            message_list.append(
                f'**Channels**:'
            )
            message_list.append(
                f'`{"Id":<25}`  `{"Name":<20}`'
            )
            message_list.append(
                f'`{"<" + room.id_voice_channel + ">":<25}`  <#{room.id_voice_channel}>'
            )
            message_list.append(
                f'`{"<" + room.id_txt_channel + ">":<25}`  <#{room.id_txt_channel}>'
            )
            message_list.append(
                f'\n**Asker**: {"<@" + room.game.asker.id + ">" if room.game.asker != None else None} | **Victim**: {"<@" + room.game.victim.id + ">" if room.game.victim != None else None}'
            )
            message_list.append(
                f'**Players**: {" | ".join([f"<@{player.id}>" for player in room.players])}'
            )
            message_list.append(
                '\n**GAME**'
            )
            message_list.append(
                f'`{"N° of truths":<14}`  `{"Id":<20}`  `{"Stars ⭐":<9}`  `{"Punishment":<12}`  `{"Name":<20}`'
            )
            for game_player in room.game.players:
                message_list.append(
                    f'`{game_player.number_of_truths:<14}`  `{game_player.id:<20}`  `{"[" + str(game_player.stars) + "]":<10}`   `[{game_player.faults}] {"✅" if game_player.id in [player.id for player in room.game.punished_players] else "🟥":<7}` <@{game_player.id}>'
                )
            await context.send('\n'.join(message_list))
            break