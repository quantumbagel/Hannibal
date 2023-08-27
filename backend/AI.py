import backend


class AI:
    def __init__(self, name, description, author, url) -> None:
        """
        Initialize a generic AI
        :param name: The name of the bot
        :param description: the description of the bot
        :param author: the maker of the bot
        :param url: the website of the source code/website of the bot
        """
        self.name = name
        self.description = description
        self.author = author
        self.url = url

    def get_move(self, moves: list[backend.Move.Move],
                 board: list[list[backend.Square.Square]],
                 timer: backend.Timer.Timer) -> backend.Move.Move:
        """
        Get the move to play.
        :param moves: the Move list
        :param board: the Board
        :param timer: the time to decide
        :return: the Move to play
        """
        raise NotImplementedError("You have to implement AI.get_move!")

    def get_info(self) -> dict:
        """
        Return the bot's information.
        :return: the bot's name, description, author, and url
        """
        return {'name': self.name, 'description': self.description, 'author': self.author, 'url': self.url}
