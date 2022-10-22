from discord.user import User
class Player:

    def __init__(
        self, id: str
    ):
        self.id: str = id
        self.number_of_truths: int = 0
        self.name: str = ''
        self.response: str = ''
        self.user: User = None