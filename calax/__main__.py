# --------------- PERSONAL PACKAGES ---------------
from model.instances.calax import calax
from model.service.calax import (
    events,
    commands
)

calax.bot.run(token = calax.bot_token)