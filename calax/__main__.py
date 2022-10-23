# --------------- PERSONAL PACKAGES ---------------
from model.instances.calax import calax
from model.service.calax.events import (
    on_ready
)
from model.service.calax import (
    commands
)

if __name__ == '__main__':
    calax.bot.run(token = calax.bot_token)