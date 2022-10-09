from model.instances.calax import calax
from model.entities.player import Player
from model.entities.room import Room
from model.service.calax.commands import (
    iniciar
)

from util.room import (
    findRoomInCalaxByPlayerId
)

from discord.channel import (
    TextChannel,
    VoiceChannel
)
from discord.message import Message
from discord.member import (
    Member,
    VoiceState
)
from discord.raw_models import RawReactionActionEvent

@calax.bot.event
async def on_ready():
    id_auth_message: str = calax.id_auth_message
    id_auth_channel: str = calax.id_auth_channel
    try:
        channel: TextChannel = calax.bot.get_channel(int(id_auth_channel))
        message: Message = await channel.fetch_message(int(id_auth_message))
        # Clear all reaction in auth message
        await message.clear_reaction("👍")
        # Add first reaction in auth message
        await message.add_reaction("👍")
        for room in calax.rooms:
            voice_channel: VoiceChannel = calax.bot.get_channel(int(room.id_voice_channel))
            voice_channel_members: list[Member] = voice_channel.members

            # Add player that is in game voice channel into its room
            ids_in_room: list[str] = [player.id for player in room.players]
            if len(voice_channel_members) > 0:
                for voice_channel_member in voice_channel_members:
                    # List all rooms to see if this player is in another one
                    if not str(voice_channel_member.id) in ids_in_room:
                        # Bug appears in the following line
                        room.addPlayer(
                            player = Player(str(voice_channel_member.id))
                        )
            else:
                room.players = []

    except Exception as exception:
        if exception.code == 10008:
            print('Auth-message not found')
    print('Calax tá on! 😎')

@calax.bot.event
async def close():
    id_auth_message: str = calax.id_auth_message
    id_auth_channel: str = calax.id_auth_channel
    try:
        channel: TextChannel = calax.bot.get_channel(int(id_auth_channel))
        message: Message = await channel.fetch_message(int(id_auth_message))
        # Clear all reaction in auth message
        await message.clear_reaction("👍")
        # Add first reaction in auth message
        await message.add_reaction("👍")
    except Exception as exception:
        if exception.code == 10008:
            print('Auth-message not found')

@calax.bot.event
async def on_message(message: Message):
    player = Player(str(message.author.id))
    player.user = calax.bot.get_user(int(player.id))

    id_voice_channel: str = None
    id_text_channel: str = None
    bot_master: Player = None
    game_players: list[Player] = []
    # Check if wasn't Calax who sent it
    if str(calax.bot.user.id) != player.id:
        rooms: list[Room] = calax.rooms
        # Check if the message was sent in a game text channel
        if str(message.channel.id) in [room.id_txt_channel for room in rooms]:
            # Search in each room
            for room in rooms:
                # for the player who sent the mesage
                for player_in_room in room.players:
                    # If it's a player in a room, it stores its id_voice_channel and id_bot_master
                    if player_in_room.id == player.id:
                        id_voice_channel = room.id_voice_channel
                        id_text_channel = room.id_txt_channel
                        bot_master = room.game.bot_master
                        game_players = room.game.players
                        break
                break
            # Auth-player or bot_master of this room
            if player.id in [player.id for player in game_players] or\
                player.id == room.game.bot_master.id:
                await calax.bot.process_commands(message)
            # Not auth-player
            else:
                await message.delete()
                await player.user.send(f'<@{player.id}>, você só pode mandar mensagem nesse chat se estiver jogando.')

@calax.bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    player = Player(str(payload.user_id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    # Check if reaction was in a game text channel
    if player_room:
        id_voice_channel: str = player_room.id_voice_channel
        id_text_channel: str = player_room.id_txt_channel

        voice_channel: VoiceChannel = calax.bot.get_channel(int(id_voice_channel))
        reacted_text_channel: TextChannel = calax.bot.get_channel(payload.channel_id)

        voice_channel_members: list[Member] = voice_channel.members
        reacted_message: Message = await reacted_text_channel.fetch_message(payload.message_id)

        # ------------ AUTH MESSAGE ------------
        if str(reacted_message.id) == calax.id_auth_message:
            # Check if this player is not in a game already
            # And if player is not Calax
            if player.id not in [player.id for player in player_room.game.players]\
            and player.id != str(calax.bot.user.id):
                player_room.game.addPlayer(player)
                await player.user.send(f'<@{player.id}>, agora você está no jogo.')

        # ------------ VOTING MESSAGE ------------
        elif str(reacted_message.id) == player_room.game.id_voting_message\
        and player.id != str(calax.bot.user.id):
            # If the user is in the game, it haven't voted yet, it is not
            # the victim and it's a vote reaction
            if player.id in [player.id for players in player_room.game.players]\
            and player.id not in [player.id for players in player_room.game.votes]\
            and player.id != player_room.game.victim.id\
            and payload.emoji.name in ["👍", "👎"]:

                player_room.game.addVote(player)

            else:
                try:
                    await reacted_message.remove_reaction(payload.emoji.name, player.user)
                except:
                    await reacted_message.remove_reaction(payload.emoji.name, player.user)

        # ------------ REACTION OUTTA THE GAME ------------
        else:
            # IMPLEMENTS
            ...
    # Player not in a room
    else:
        # ------------ AUTH MESSAGE ------------
        if str(payload.message_id) == calax.id_auth_message\
            and player.id != str(calax.bot.user.id):
            try:
                reacted_text_channel: TextChannel = calax.bot.get_channel(payload.channel_id)
                reacted_message: Message = await reacted_text_channel.fetch_message(payload.message_id)
                await reacted_message.remove_reaction(payload.emoji.name, player.user)

                await player.user.send(f'<@{player.id}>, você precisa estar em um canal de voz do jogo para participar.')
            except Exception as exception:
                print(exception)
        # print('Player is not in room!')

@calax.bot.event
async def on_raw_reaction_remove(payload: RawReactionActionEvent):
    player = Player(str(payload.user_id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    # Check if reaction was in a game text channel
    if player_room:
        id_voice_channel: str = player_room.id_voice_channel
        id_text_channel: str = player_room.id_txt_channel

        voice_channel: VoiceChannel = calax.bot.get_channel(int(id_voice_channel))
        reacted_text_channel: TextChannel = calax.bot.get_channel(payload.channel_id)

        voice_channel_members: list[Member] = voice_channel.members
        reacted_message: Message = await reacted_text_channel.fetch_message(payload.message_id)

        # ------------ AUTH MESSAGE ------------
        if str(reacted_message.id) == calax.id_auth_message:
            # Check if this player is in a game
            # And if player is not Calax
            if player.id in [player.id for player in player_room.game.players]\
            and player.id != str(calax.bot.user.id):
                player_room.game.removePlayer(player.id)
                await player.user.send(f'<@{player.id}>, você não pode sair do jogo. Vai pagar por isso!😈')
                # If was the victim
                if player.id == player_room.game.victim.id:
                    player_room.game.fase_controller = 0
                    if player_room.game.players_pointer > 0:
                        player_room.game.players_pointer -= 1
                    await iniciar(player_room.game.master_context)
                # If was the asker
                elif player.id == player_room.game.asker.id:
                    player_room.game.fase_controller = 0
                    await iniciar(player_room.game.master_context)

        # ------------ VOTING MESSAGE ------------
        elif str(reacted_message.id) == player_room.game.id_voting_message\
        and player.id != str(calax.bot.user.id):
            # IMPLEMENTS
            # If the user is in the game, it have already voted, it is not
            # the victim and it's a vote reaction
            if player.id in [player.id for players in player_room.game.players]\
            and player.id in [player.id for players in player_room.game.votes]\
            and player.id != player_room.game.victim.id\
            and payload.emoji.name in ["👍", "👎"]:

                await reacted_message.remove_reaction(payload.emoji.name, player.user)

        # ------------ REACTION OUTTA THE GAME ------------
        else:
            # IMPLEMENTS
            ...


@calax.bot.event
async def on_voice_state_update(
    context: Member,
    before: VoiceState,
    after: VoiceState
):

    player = Player(str(context.id))
    player.user = calax.bot.get_user(int(player.id))
    game_voice_channels: str = [room.id_voice_channel for room in calax.rooms]

    # Got into a voice channel
    if before.channel == None:
        # Check if it's a game channel
        if str(after.channel.id) in game_voice_channels:
            # ADD IT INTO ITS ROOM
            for room in calax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break

    # Got out from a voice channel just
    elif before.channel != None and after.channel == None:
        # Check if it's from a game channel
        if str(before.channel.id) in game_voice_channels:

            # REMOVE IT FROM ITS ROOM
            id_auth_message: str = calax.id_auth_message
            auth_channel: TextChannel = calax.bot.get_channel(int(calax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in calax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break

    # Changed its voice channel
    elif before.channel != None and after.channel != None:
        # Check if it was from a game channel to another game channel
        if str(before.channel.id) in game_voice_channels and\
            str(after.channel.id) in game_voice_channels and\
            before.channel.id != after.channel.id:

            # REMOVE IT FROM ITS ROOM
            id_auth_message: str = calax.id_auth_message
            auth_channel: TextChannel = calax.bot.get_channel(int(calax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in calax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break

            # ADD IT INTO ITS ROOM
            for room in calax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break

        # Check if it was not from a game channel to a game channel
        elif str(before.channel.id) not in game_voice_channels and\
            str(after.channel.id) in game_voice_channels:

            # ADD IT INTO ITS ROOM
            for room in calax.rooms:
                if str(after.channel.id) == room.id_voice_channel:
                    room.addPlayer(
                        player = player
                    )
                    break
            
        # Check if it was from a game channel to a not game channel
        elif str(before.channel.id) in game_voice_channels and\
            str(after.channel.id) not in game_voice_channels:
             # REMOVE IT FROM ITS ROOM
            id_auth_message: str = calax.id_auth_message
            auth_channel: TextChannel = calax.bot.get_channel(int(calax.id_auth_channel))
            auth_message: Message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)

            # REMOVE IT FROM ITS ROOM
            for room in calax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break
