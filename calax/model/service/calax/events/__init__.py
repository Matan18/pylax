from model.instances.calax import calax

@calax.bot.event
async def on_ready():
    # Adicionar todas as pessoas nas salas de voz no objeto sala
    id_auth_message = calax.id_auth_message
    id_auth_channel = calax.id_auth_channel
    print(f'id_auth_message: {id_auth_message}')
    print(f'id_auth_channel: {id_auth_channel}')
    channel = calax.bot.get_channel(int(id_auth_channel))
    message = await channel.fetch_message(int(id_auth_message))
    await message.clear_reaction("👍")
    await message.add_reaction("👍")
    