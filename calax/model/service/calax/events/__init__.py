from model.instances.calax import calax
from model.entities.player import Player
from model.entities.room import Room

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
            # BUG: even if there is no player in the voice channel,
            # it appends player from other room into players
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
async def on_message(message):
    player = Player(str(message.author.id))
    player.user = calax.bot.get_user(int(player.id))

    id_voice_channel: str = None
    id_text_channel: str = None
    id_bot_master: str = None
    auth_players: list[Player] = []
    # Check if was't Calax who sent it
    if str(calax.bot.user.id) != player.id:
        rooms: list[Room] = calax.rooms
        # Check if the message was sent in a game text channel
        if str(message.channel.id) in [room.id_txt_channel for room in rooms]:
            # Search in each room
            for room in rooms:
                # for the player who sent the mesage
                for player_in_room in room.players:
                    # If it's a player in a room, it stores its id_voice_channel and id_bot_master
                    if player_in_room == player.id:
                        id_voice_channel = room.id_voice_channel
                        id_text_channel = room.id_txt_channel
                        id_bot_master = room.game.bot_master
                        auth_players = room.game.players
                        break
                break
            # Auth-player or bot_master of this room
            if player.id in auth_players or player.id == room.game.bot_master.id:
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
            # IMPLEMENTS
            ...
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

                await player.user.send(f'<@{player.id}>, você precisa estar em uma fala para participar do jogo.')
            except Exception as exception:
                print(exception)
        # print('Player is not in room!')

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
            id_auth_message = calax.id_auth_message
            auth_channel = calax.bot.get_channel(int(calax.id_auth_channel))
            auth_message = await auth_channel.fetch_message(int(id_auth_message))
            await auth_message.remove_reaction("👍", player.user)
            for room in calax.rooms:
                if str(before.channel.id) == room.id_voice_channel:
                    room.removePlayer(
                        id_player = str(context.id)
                    )
                    break
            # [TO-DO] REMOVE ITS REACTION FROM AUTH MESSAGE
            # [CHECK] IT WAS IN A GAME
                # [TO-DO] TAKE OUT FROM A GAME
                # [CHECK] IT WAS A VICTIM
                    # [TO-DO] RESTART THE ROUND
                # [CHECK] IT WAS A ASKER
                    # [TO-DO] GO TO NEXT ROUND
                
            ...
    # Changed its voice channel
    elif before.channel != None and after.channel != None:
        # Check if it's from a game channel to a game channel
        if str(before.channel.id) in game_voice_channels and\
            str(after.channel.id) in game_voice_channels:
            # [TO-DO] TAKE OUT FROM ITS ROOM
            # [TO-DO] REMOVE ITS REACTION FROM AUTH MESSAGE
            # [CHECK] IT WAS IN A GAME
                # [TO-DO] TAKE OUT FROM A GAME
            # [TO-DO] PUT IT INTO ITS ROOM
            ...

        # Check if it's not from a game channel to a game channel
        elif str(before.channel.id) not in game_voice_channels and\
            str(after.channel.id) in game_voice_channels:
            # [TO-DO] PUT IT INTO ITS ROOM
            ...
            
        # Check if it's from a game channel to a not game channel
        elif str(before.channel.id)  in game_voice_channels and\
            str(after.channel.id) not in game_voice_channels:
            # [TO-DO] TAKE OUT FROM ITS ROOM
            # [TO-DO] REMOVE ITS REACTION FROM AUTH MESSAGE
            # [CHECK] IT WAS IN A GAME
                # [TO-DO] TAKE OUT FROM A GAME
                # [CHECK] IT WAS A VICTIM
                    # [TO-DO] RESTART THE ROUND
                # [CHECK] IT WAS A ASKER
                    # [TO-DO] GO TO NEXT ROUND
            ...
        # Check if it's not from a game channel
        ...
#     if before.channel != None:
#       b_current_channel_id = before.channel.id

#     if after.channel != None:
#       a_current_channel_id = after.channel.id


#     user = ctx.id
#     b = str(before.channel)
#     a = str(after.channel)
#     # Get inside
#     # print(f'Before:{before}', f'\nAfter:{after}')
#     if ((b == 'None' and a != 'None') or (b != 'None' and a != 'None')) and (a != b) and after.channel.id in channels_ids.keys():

#         if user not in channels_ids[after.channel.id]['mem_vc_id']:
#           channels_ids[after.channel.id]['mem_vc_id'].append(user)

#         if before.channel and after.channel is not None and before.channel.id != after.channel.id:
#           auth_msg_id = channels_ids[before.channel.id]['auth_msg_id']
#           txt_channel_id = channels_ids[before.channel.id]['txt_channel_id']
#           txt_channel   = client.get_channel(txt_channel_id)
#           # Remove reaction from auth message and user from the list
#           if user in channels_ids[before.channel.id]['mem_vc_id']:
#             channels_ids[before.channel.id]['mem_vc_id'].remove(user)
#             channel = client.get_channel(channels_ids[before.channel.id]['auth_channel_id'])
#             message = await channel.fetch_message(auth_msg_id)
#             user_g  = client.get_user(user)
#             await message.remove_reaction("👍", user_g)

#           # If this user is in the players list, it takes
#           # it off
#           if user in channels_ids[before.channel.id]['mem_play_id']:
#             channels_ids[before.channel.id]['mem_play_id'].remove(user)
#             await ctx.send(f'<@{user}>, você não pode sair do jogo. Vai pagar por isso!😈')

#             # If person who left is the victim, it
#             # restart round
#             try:
#               victim = channels_ids[before.channel.id]['victim']
#               asker = channels_ids[before.channel.id]['asker']
#               if user == victim:
#                 await txt_channel.send(f'Nossa vítima <@{user}> saiu da sala. Vamos reiniciar a rodada.')
#                 channels_ids[before.channel.id]['ctrl']   = 0
#                 channels_ids[before.channel.id]['turn']  -= 1
#                 channels_ids[before.channel.id]['victim'] = None
#                 await iniciar(channels_ids[before.channel.id]['master_ctx'])
                  
#               elif user == asker:
#                 await txt_channel.send(f'A pessoa que pergunta saiu da sala. Vamos reiniciar a rodada.')
#                 channels_ids[before.channel.id]['ctrl']   = 0
#                 channels_ids[before.channel.id]['asker'] = None
#                 await iniciar(channels_ids[before.channel.id]['master_ctx'])
#             except:
#               pass