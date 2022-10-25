# --------------- PERSONAL PACKAGES ---------------
from model.instances.pylax import pylax
from model.service.pylax import (
    events,
    commands
)

pylax.bot.run(token = pylax.bot_token)