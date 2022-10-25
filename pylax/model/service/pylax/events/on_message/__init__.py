# --------------- BUILT-IN PACKAGES ---------------

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import Player
from model.entities.room import Room
from model.instances.pylax import pylax

# --------------- DISCORD PACKAGES ---------------
from discord.message import (
    Message
)

@pylax.bot.event
async def on_message(message: Message):
    player = Player(str(message.author.id))
    player.user = pylax.bot.get_user(int(player.id))

    id_voice_channel: str = None
    id_text_channel: str = None
    bot_master: Player = None
    game_players: list[Player] = []
    # Check if wasn't pylax who sent it
    if str(pylax.bot.user.id) != player.id:
        rooms: list[Room] = pylax.rooms
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
                if game_players != []:
                    break
            # Auth-player or bot_master of this room
            if player.id in [player.id for player in game_players] or\
                player.id == bot_master.id:
                await pylax.bot.process_commands(message)
            # Not auth-player
            else:
                await message.delete()
                await player.user.send(f'<@{player.id}>, você só pode mandar mensagem nesse chat se estiver jogando.')