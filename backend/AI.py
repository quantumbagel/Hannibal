import backend


class AI:
    def __init__(self, name, description, author, url):
        """
        Initalize a generic AI
        :param name: The bot's name
        :param description: the bot's description
        :param author: the bot's maker
        """
        self.name = name
        self.description = description
        self.author = author
        self.url = url

    def get_move(self, moves: list[backend.Move.Move], board: list[list[backend.Square.Square]], timer: backend.Timer.Timer) -> backend.Move.Move:
        raise NotImplementedError("You have to implement AI.get_move!")


    def get_info(self):
        return {'name': self.name, 'description': self.description, 'author': self.author, 'url': self.url}
