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

    def get_move(self, board: Board, timer: Timer) -> (Move, str):
        """
        Get the move. There really isn't anything else to say here xD.
        :param board: you should know this
        :param timer: cmon
        :return: the move and the message to send. return "" for no message
        xD why did I write this
        """
        # if we can't move, don't. The reason this goes to the bot is that they can assess that they made a mistake
        # and log it
        if len(board.moves) == 0:
            return Move(null=True)
        for move in board.moves:
            if move.end_square.square_type == 0 and move.end_square.color == "":
                # if the move moves to an empty square, capture it
                return move, "i PLAYED THIS BECAUSE THE SQUARE WAS EMPTY"
            if move.end_square.square_type == 1\
                    and move.end_square.color == ""\
                    and move.start_square.troop_number > move.end_square.troop_number+1:  # a city we can capture
                return move, "I played this move because it was a city that I could capture :D"
            if move.end_square.square_type == 0\
                    and move.end_square.troop_number+1 < move.start_square.troop_number\
                    and move.end_square.color\
                    not in [board.our_color, ""]:
                return move, "I played this move because I could capture your square :D"
        return Move(null=True), 'I chose not to play a move because yYYyYyou....set Me UP'
