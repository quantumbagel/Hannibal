import random
from backend.Move import Move
from backend.Timer import Timer
from backend.AI import AI
from backend.Board import Board


class HannibalBot(AI):
    def __init__(self) -> None:
        """
        Hannibal: the bot
        ToBeImplemented I guess
        """
        super(HannibalBot, self).__init__("Hannibal", "Hannibal is a bot.", "@quantumbagel, @p1xelz22",
                                          "https://github.com/quantumbagel/Hannibal")

    def get_move(self, board: Board, timer: Timer) -> Move:
        """
        Get the move. There really isn't anything else to say here xD.
        :param board: you should know this
        :param timer: cmon
        :return: the move, you genius
        xD why did I write this
        """
        # if we can't move, don't. The reason this goes to the bot is that they can assess that they made a mistake
        # and log it
        if len(board.moves) == 0:
            return Move(null=True)
        for move in board.moves:
            if move.end_square.square_type == 0:
                print(move, move.end_square.color, move.start_square.color)
            if move.end_square.square_type == 0 and move.end_square.color == "":
                # if the move moves to an empty square, capture it
                return move
            if move.end_square.square_type == 1\
                    and move.end_square.color == ""\
                    and move.start_square.troop_number > move.end_square.troop_number+1:  # a city we can capture
                return move
            if move.end_square.square_type == 0\
                    and move.end_square.troop_number+1 < move.start_square.troop_number\
                    and move.end_square.color\
                    not in [board.our_color, ""]:
                return move
        return Move(null=True)
