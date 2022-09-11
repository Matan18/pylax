from discord.user import User
class Player:
    __number_of_truths: int = 0
    __name: str = ''
    __response: str = ''
    __user: User = None

    def __init__(
        self, id: str
    ):
        self.__id: str = id

    @property
    def number_of_truths(self) -> str:
        return self.__number_of_truths

    @number_of_truths.setter
    def number_of_truths(self, value: int) -> None:
        self.__number_of_truths = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @property
    def response(self) -> str:
        return self.__response

    @response.setter
    def response(self, response: str) -> None:
        self.__response = response

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, user: str) -> None:
        self.__user = user