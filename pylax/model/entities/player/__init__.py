from discord.user import User
class Player:

    def __init__(
        self, id: str
    ):
        self.faults: int = 0
        self.id: str = id
        self.number_of_truths: int = 0
        self.name: str = ''
        self.response: str = ''
        self.stars: int = 0
        self.user: User = None