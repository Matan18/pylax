# --------------- BUILT-IN PACKAGES ---------------


# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)
from discord.message import Message

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
from util import ROOT_PATH
from util.room import (
    findRoomInpylaxByPlayerId
)

# Rules
@pylax.bot.command()
async def rules(
    context: Context,
):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    for room in pylax.rooms:
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
                f'{"iniciar | comecar | começar | start ":>35} - Inicia uma nova partida. Não é possível iniciar enquanto uma outra estiver acontecendo.'
            )
            message_list.append(
                f'{"girar | gira | rodar | roda | spin ":>35} - Sorteia quem irá desafiar quem.'
            )
            message_list.append(
                f'{"op | opcao | opção | option | choice ":>35} - Escolhe qual das opções a vítima quer. Use `v` ou `c` para escolher.'
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


# --------------- ALIASES ---------------
def rules_aliases() -> None:
    @pylax.bot.command()
    async def regras(context: Context):
        await rules(context)

    @pylax.bot.command()
    async def regra(context: Context):
        await rules(context)

    @pylax.bot.command()
    async def rule(context: Context):
        await rules(context)