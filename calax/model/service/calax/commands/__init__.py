from model.instances.calax import calax
from model.entities.player import Player
from model.entities.room import Room

from discord.member import (
    Member
)

from discord.ext.commands.context import (
    Context
)
from discord.message import Message

from random import choice

from util.room import (
    findRoomInCalaxByPlayerId
)

async def showListOfPlayers(context: Context) -> None:
    """Show which people are in the game.

    Parameters
    ----------
    context : Context
        Context for the called command.
    """
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    bot_masters: list[str] = [room.game.bot_master.id for room in calax.rooms]
    if player.id in bot_masters:
        for room in calax.rooms:
            if room.id_txt_channel == str(context.channel.id):
                message: list[str] = [
                    'Pessoas participando da brincadeira:',
                    *[f' - <@{player.id}>' for player in room.players]
                ]
                await context.send('\n'.join(message))
                break

@calax.bot.command()
async def show_players(context: Context):
    """Show which people are in the game.

    Parameters
    ----------
    context : Context
        Context for the called command.
    """
    await showListOfPlayers(context = context)

# Starts the turn
@calax.bot.command()
async def iniciar(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    bot_masters: list[Player] = [room.game.bot_master for room in calax.rooms]
    if player.id in [bot_master.id for bot_master in bot_masters]:
        for room in calax.rooms:
            if str(context.channel.id) == room.id_txt_channel:
                room.game.master_context = context

                if room.game.fase_controller == 0 and len(room.game.players) > 1:
                    room.game.asker = room.game.players[room.game.players_pointer]
                    # Every new game goes to the next player;
                    # if the next player is the last one, it goes
                    # to the first one
                    if room.game.players_pointer < len(room.game.players) - 1:
                        room.game.players_pointer += 1
                    else:
                        room.game.players_pointer = 0

                    # Shows which people are in the game
                    await showListOfPlayers(context = context)
                    await context.send(f'\n<@{room.game.asker.id}> gire a garrafa.')
                    room.game.fase_controller = 1
                    break
                else:
                    await context.send(f'Não é possível inciar uma partida agora. Veja o número de jogadores ou em que fase estamos.')
                break

@calax.bot.command()
async def girar(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 1 and\
        room.game.asker.id == player.id:
            room.game.is_victim_a_asker = False
            # Raffles a different person to the arker to be
            # the victim
            while not room.game.is_victim_a_asker:
                room.game.victim = choice(room.game.players)
                if room.game.victim.id != room.game.asker.id:
                    room.game.is_victim_a_asker = True

            # Show the bottle spining
            message: Message = await context.send(
                content = f'Girando a garrafa: <@{choice(room.game.players).id}>'
            )
            for _ in range(10):
                await message.edit(
                    content = f'Girando a garrafa: <@{choice(room.game.players).id}>'
                )
            await message.edit(
                content = f'Girando a garrafa: <@{room.game.victim.id}>'
            )
            await message.delete()

            await context.send(
                content = f'<@{room.game.asker.id}> pergunta para <@{room.game.victim.id}>. Verdade ou consequência?'
            )
            room.game.fase_controller = 2
            break
        else:
            ...
            # await context.send(f'Não é possível girar a garrafa agora agora.')

# Command to choose if it's verdade or consequencia
@calax.bot.command()
async def op(
    context: Context,
    option: str = ''
):
    option = option.lower()
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 2 and\
        room.game.victim.id == player.id:
            if option == 'v':
                # It can choose truth
                if room.game.victim.number_of_truths <= 3:
                    room.game.victim.response = 'verdade'
                    await context.send(f'<@{room.game.asker.id}>, faça sua pergunta.')
                    room.game.victim.number_of_truths += 1
                    room.game.fase_controller = 3
                    break
                # It must choose challenge
                else:
                    option = 'c'
                    await context.send(
                        f'<@{room.game.victim.id}> você escolheu 3 vezes verdade. Agora será feito um desafio para você.'
                    )
                    room.game.victim.number_of_truths = 0
            if option == 'c':
                room.game.victim.response = 'consequencia'
                await context.send(f'<@{room.game.asker.id}>, faça seu desafio.')
                room.game.fase_controller = 3
                break
        else:
            ...
            # await context.send(f'Não é possível enviar uma resposta para o bot agora.')
