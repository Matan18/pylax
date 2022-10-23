import json
from time import sleep

from model.instances.calax import calax
from model.entities.player import Player
from model.entities.room import Room

from util import ROOT_PATH

from discord.member import (
    Member
)

from discord.channel import (
    TextChannel
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
                punished_player_ids: list[str] =\
                        [punished_playes.id for punished_playes in room.game.punished_players]
                message: list[str] = [
                    'Pessoas participando da brincadeira:',
                    *[f' - {"🚩" * player.faults} | ~~{player.user.name}~~'
                      if player.id in punished_player_ids
                      else f' - <@{player.id}>'
                      for player in room.game.players]
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
                punished_player_ids: list[str] =\
                    [punished_playes.id for punished_playes in room.game.punished_players]
                if room.game.fase_controller == 0\
                    and len([player for player in room.game.players if player.id not in punished_player_ids]) > 1:
                    # [REFACTOR IT]
                    while room.game.players[room.game.players_pointer].id in punished_player_ids:
                        if room.game.players_pointer < len(room.game.players) - 1:
                            room.game.players_pointer += 1
                        else:
                            room.game.players_pointer = 0
                    room.game.asker = room.game.players[room.game.players_pointer]
                    # Every new game goes to the next player;
                    # if the next player is the last one, it goes
                    # to the first one
                    if room.game.players_pointer < len(room.game.players) - 1:
                        room.game.players_pointer += 1
                    else:
                        room.game.players_pointer = 0
                    # Check if the next arker will not be a punished player
                        

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
            punished_player_ids: list[str] =\
                        [punished_playes.id for punished_playes in room.game.punished_players]
            while not room.game.is_victim_a_asker:
                room.game.victim = choice(room.game.players)
                if room.game.victim.id != room.game.asker.id\
                    and room.game.victim.id not in punished_player_ids:
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

# Command to be used when asker doesn't know what to ask
@calax.bot.command()
async def ajuda(context: Context):
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

# Command to be used when the challenge or the answer is done
@calax.bot.command()
async def feito(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 3 and\
        room.game.victim.id == player.id:

            # Clear last votes
            room.game.votes = []

            # Starts the vote to see if people believe in the victim
            message = await context.send("Vocês acreditam nessa pessoa?")
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            room.game.id_voting_message = str(message.id)

            # Wait 10 seconds to finish the vote
            number_emojis: list[str] = [
                "🔟", "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣", "0️⃣"
            ]
            for number_emoji in number_emojis:
                await message.add_reaction(number_emoji)
                # if all the players already voted, stop votes 
                if len(room.game.votes) == len(room.game.players) - 1:
                    try:
                        await message.clear_reaction(number_emoji)
                        break
                    except:
                        await message.clear_reaction(number_emoji)
                        break
                sleep(1)
                await message.clear_reaction(number_emoji)

            updated_message: Message = await context.channel.fetch_message(message.id)

            positive: int = 0
            negative: int = 0 
            # Counts the votes
            for reaction in updated_message.reactions:
                if str(reaction) == "👍":
                    positive = reaction.count
                elif str(reaction) == "👎":
                    negative = reaction.count

            # Verifies results
            if positive > negative:
                room.game.victim.stars += 1
                await context.send(
                    f'<@{room.game.victim.id}>, as pessoas acreditaram em você.\nMuito bem! Ganhou uma estrelinha.⭐'
                )
            elif negative > positive:
                room.game.victim.faults += 1
                await context.send(
                    f'<@{room.game.victim.id}>, as pessoas não acreditaram em você.\nVocê vai pagar por isso!😈'
                )
                
                if room.game.victim.faults >= 2:
                    room.game.addPunishedPlayer(
                        player = room.game.victim
                    )
            else:
                await context.send(
                    f'<@{room.game.victim.id}>, as pessoas ficaram na Dúvida.\nVocê falhou.'
                )
            room.game.fase_controller = 0
            
            # Remove one fault of each player if it is not a victim
            for punished_player in room.game.punished_players:
                if punished_player.id != room.game.victim.id:
                    punished_player.faults -= 1
                    if punished_player.faults <= 0:
                        room.game.removePunishedPlayer(
                            id_player = punished_player.id
                        )         

            # Starts a new round after 1s
            sleep(1)
            await iniciar(room.game.master_context)
            break
        else:
            ...
            # await context.send(f'<@{player.id}>, você não pode responder agora.')

# Restart the game
@calax.bot.command()
async def restart(context: Context):
    await context.message.delete()
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
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

# Go to the next round
@calax.bot.command()
async def proximo(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            await context.send('⏩ | Pulando para o próximo participante...')
            room.game.fase_controller = 0
            await iniciar(context)
            break

@calax.bot.command()
async def status(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
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
                f'`{"N° of truths":<14}`  `{"Id":<20}`  `{"Punishment":<12}`  `{"Name":<20}`'
            )
            for game_player in room.game.players:
                message_list.append(
                    f'`{game_player.number_of_truths:<14}`  `{game_player.id:<20}`  `[{game_player.faults}] {"✅" if game_player.id in [player.id for player in room.game.punished_players] else "🟥":<7}` <@{game_player.id}>'
                )
            await context.send('\n'.join(message_list))
            break


# Kick player
@calax.bot.command()
async def kick(
    context: Context,
    id_kick_player: str = '',
    option: str = '2'
):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    async def fromGame(room: Room):
        room.game.removePlayer(id_kick_player)

    async def fromRoom(room: Room):
        room.removePlayer(id_kick_player)
        id_auth_message: str = calax.id_auth_message
        auth_channel: TextChannel = calax.bot.get_channel(int(calax.id_auth_channel))
        auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
        await auth_message.remove_reaction("👍", calax.bot.get_user(int(id_kick_player)))

    async def fromEverywhere(room: Room):
        await fromGame(room)
        await fromRoom(room)

    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.bot_master.id == player.id:
            places = [fromGame, fromRoom, fromEverywhere]
            try:
                await places[int(option)](room)
            except Exception as exception:
                print(exception)
            break

# Rules
@calax.bot.command()
async def regras(
    context: Context,
):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel\
        and player.id in [player.id for player in room.game.players]:

            # Build the status message
            message_list: list[str] = []
            message_list.append(
                'Olá! Vamos brincar de uma brincadeira bem divertida? 😈'
            )
            message_list.append(
                'Prefixo: ??'
            )
            message_list.append(
                'Comandos:\n'
            )
            message_list.append(
                f'{"iniciar | comeca | começa | play ":>35} - Inicia uma nova partida. Não é possível iniciar enquanto uma outra estiver acontecendo.'
            )
            message_list.append(
                f'{"girar | gira | rodar | roda ":>35} - Sorteia quem irá desafiar quem.'
            )
            message_list.append(
                f'{"op | opcao | opção | option ":>35} - Escolhe qual das opções a vítima quer. Use `v` ou `c` para escolher.'
            )
            message_list.append(
                f'{"ajuda | ajd | help ":>35} - Não sabe o que perguntar? Use esse comando que Calux vai te ajudar.'
            )
            message_list.append(
                f'{"feito | done ":>35} - A vítima deve usar esse comando quando tiver respondido ou cumprido seu desafio.'
            )
            message_list.append(
                f'{"regras | regra | rule | rules ":>35} - Mostra os como jogar e os comandos do bot.\n'
            )
            message_list.append(
                'Lembrando que os desafios podem ser provados com uma fotinha, um vídeo curto ou mostrando na call. As pessoas decidirão se acreditam ou não.\n'
            )
            message_list.append(
                'Vamos começar! 😈'
            )

            await context.send('```' + '\n'.join(message_list) + '```')