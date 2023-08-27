import random
from backend.Move import Move
from backend.Timer import Timer
from backend.Square import Square
from backend.AI import AI


class HannibalBot(AI):
    def __init__(self) -> None:
        """
        Hannibal: the bot
        ToBeImplemented I guess
        """
        super(HannibalBot, self).__init__("Hannibal", "Hannibal is a bot.", "@quantumbagel, @p1xelz22",
                                          "https://github.com/quantumbagel/Hannibal")

    def get_move(self, moves: list[Move], board: list[list[Square]], timer: Timer) -> Move:
        """
        Get the move. There really isn't anything else to say here xD.
        :param moves: you know
        :param board: you should know this
        :param timer: cmon
        :return: the move, you genius
        """
        if len(moves) == 0:
            return Move(null=True)
        return moves[random.randint(0, len(moves) - 1)]
