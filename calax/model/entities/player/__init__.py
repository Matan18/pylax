class Player:
    __number_of_truths: int = 0

    def __init__(
        self, id: str, name: str, response: str
    ):
        self.__id: str = id
        self.__name: str = name
        self.__response: str = response

    @property
    def number_of_truths(self):
        return self.__number_of_truths

    @number_of_truths.setter
    def number_of_truths(self, value: int):
        self.__number_of_truths = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, response: str):
        self.__response = response