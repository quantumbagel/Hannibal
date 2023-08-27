# DIRECTION
"""
0: up
1: right
2: down
3: left
"""
import backend.Square


class Move:
    def __init__(self, row: int = None, column: int = None, direction: int = None,
                 is_50_percent: int = None, start_square: backend.Square.Square = None,
                 end_square: backend.Square.Square = None, null: bool = False) -> None:
        """
        Initialize a new Move
        :param row: the row that we move from
        :param column: the column we move from
        :param direction: the direction (see top of file)
        :param is_50_percent: whether the move is 50 percent or not
        :param start_square: the starting Square
        :param end_square: the ending Square
        :param null: is the move null?
        """
        self.direction = direction
        self.is_50_percent = is_50_percent
        self.row = row
        self.column = column
        self.start_square = start_square
        self.end_square = end_square
        self.is_null = null
        if self.is_null:
            self.direction = None
            self.is_50_percent = None
            self.row = None
            self.column = None
            self.start_square = None
            self.end_square = None

    def __str__(self) -> str:
        if self.is_null:
            return "null"
        visualize = ['up', 'right', 'down', 'left']
        s = f'({self.column}, {self.row}) {visualize[self.direction]}'
        if self.is_50_percent:
            s += ' 50%'
        return s
