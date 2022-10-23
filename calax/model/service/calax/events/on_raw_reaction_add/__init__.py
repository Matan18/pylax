# --------------- BUILT-IN PACKAGES ---------------

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import Player
from model.entities.room import Room
from model.instances.calax import calax
from util.room import (
    findRoomInCalaxByPlayerId
)

# --------------- DISCORD PACKAGES ---------------
from discord.channel import (
    TextChannel,
    VoiceChannel
)
from discord.member import (
    Member
)
from discord.message import (
    Message
)
from discord.raw_models import RawReactionActionEvent

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