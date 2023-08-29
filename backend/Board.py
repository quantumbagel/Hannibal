import sys
import backend.Move
from backend.Square import Square
from backend.Move import Move
from backend.log import dprint
from Constants import colors, abbrev_colors
from copy import deepcopy
class Board:
    def __init__(self, our_color) -> None:
        self.our_color = our_color
        self.moves = []
        self.board = []
        self.height = 0
        self.width = 0
        self._board_initalized = False
        self.queued_moves = []
        self._previous_board_positions = []
        # note: you have to run Board.update before any value is ready
    def update(self, moves_2d_squares: list[list[backend.Square.Square]] = None, moves_html: str = None) -> None:
        """
        Update the board and moves to a list of
        :param moves_2d_squares: a 2d list of Squares (from GameManager) to send to the Board
        :param moves_html: the HTML from the table to parse.
        :return: None
        """
        if moves_2d_squares is None and moves_html is None:
            dprint("Board.update", "Error! You must supply one of moves_2d_squares or moves_html to Board.update.")
        if moves_2d_squares is not None:
            if len(moves_2d_squares) != self.height:
                dprint("Board.update", f"Error! Height mismatch from moves_2d_squares. got: {len(moves_2d_squares)}"
                                       f" expected: {self.height}")
                sys.exit(1)
            if len(moves_2d_squares[0]) != self.width:
                dprint("Board.update", f"Error! Width mismatch from moves_2d_squares. got: {len(moves_2d_squares[0])}"
                                       f" expected: {self.width}")
                sys.exit(1)
            self.board = moves_2d_squares
            return

        arrows = ['\u2190', '\u2191', '\u2192', '\u2193']
        board_html = moves_html. \
            replace('<tr>', ""). \
            replace("</tr>", "[end]"). \
            replace('"', "")
        board_html = [i.replace('></td>', "").replace(' class="', "").replace("</tbody>", "") for i in
                      board_html.split("<td class=")][1:]
        # the above jank is a html parser that's ~35 times faster than using native selenium
        new_board = []
        temp_board = []
        current_column = 0
        current_row = -1
        for item in board_html:
            square_count = 0
            current_row += 1
            is_end_row = '[end]' in item  # flag for row ending
            if ">" in item:  # this means that the item has army
                next_loop = False  # more html parsing to ensure that the arrows don't screw with the table
                for i in item:  # we technically don't need this
                    if i in arrows:  # it's just for lag
                        next_loop = True  # because you never know
                        break
                if next_loop:
                    continue
                try:
                    square_count = int(item.replace("</td", "").split('>')[1].replace("[end]", "")  # yay
                                       .replace("<div class=center-horizontal style=bottom: 0px;", "")  # more html
                                       .replace("<div class=center-horizontal style=top: 0px;", "")  # parser
                                       .replace("<div class=center-vertical style=left: 0px;", "")  # argh
                                       .replace("<div class=center-vertical style=right: 0px;", ""))  # this is evil
                except ValueError as e:
                    dprint("Board.update", "value error: ", item, e)
                    sys.exit(1)
                item = item.split('>')[0]
            if not self._board_initalized:
                temp_board.append(Square(item.replace('[end]', ''), square_count))
            else:
                if self.board[current_column][current_row].is_general:
                    temp_board.append(Square(item.replace('[end]', ''), square_count, override_general=True))
                elif self.board[current_column][current_row].is_city:
                    temp_board.append(Square(item.replace('[end]', ''), square_count, override_city=True))
                elif self.board[current_column][current_row].is_mountain:
                    temp_board.append(Square(item.replace('[end]', ''), square_count, override_mountain=True))
                if self.board[current_column][current_row].color:
                    temp_board.append(Square(item.replace('[end]', ''), square_count, override_color_from_remebrance=self.board[current_column][
                            current_row].color))

            if is_end_row:
                current_row = -1
                current_column += 1
                new_board.append(temp_board)
                temp_board = []
        self.board = new_board
        self.height = len(self.board)
        self.width = len(self.board[0])
        self._update_moves()

    def _update_moves(self) -> list[backend.Move.Move]:
        """
        update self.moves based on self.board
        :return: the new moves.
        """
        self.moves = []
        transform = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        for y, column in enumerate(self.board):
            if len(column) != self.width:
                dprint("Board._update_moves", f"things are very sus. expected {self.width} got {len(column)}.")
            for x, square in enumerate(column):
                if square.color == self.our_color:
                    for fifty_percent in range(2):
                        exit_early = False
                        for direction in range(4):
                            new_position = [x + transform[direction][0], y + transform[direction][1]]
                            if new_position[0] >= self.width \
                                    or new_position[0] < 0 \
                                    or new_position[1] >= self.height \
                                    or new_position[1] < 0:
                                continue
                            if self.board[new_position[1]][new_position[0]].is_mountain:  # mountain
                                continue
                            if self.board[y][x].troop_number < 2:  # not enough troops
                                exit_early = True
                                break
                            self.moves.append(Move(y, x, direction, fifty_percent, start_square=self.board[y][x],
                                                   end_square=self.board[new_position[1]][new_position[0]]))
                        if exit_early:
                            break
        return self.moves

    def play_move(self, move: backend.Move.Move):
        """
        Simulate playing a move. This assumes the move is valid. This updates the Board state as well.
        :param move: the move to play
        :return: None
        """
        self._previous_board_positions.append(deepcopy(self.board))
        start = move.start_square
        is_50 = move.is_50_percent
        column = move.column
        row = move.row
        direction = move.direction
        transform = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        new_position = [row + transform[direction][0], column + transform[direction][1]]
        # calculate troops to move
        if is_50:
            if start.troop_number % 2:
                troops_to_move = start.troop_number // 2
            else:
                troops_to_move = (start.troop_number - 1) // 2
        else:
            troops_to_move = start.troop_number - 1
        # transfer troops
        # if we own the square, nobody does, or an opponent does, but with 0 army, we can add directly
        colo = self.board[new_position[1]][new_position[0]].color
        troop_end = self.board[new_position[1]][new_position[0]].troop_number
        if colo == self.our_color or (colo != self.our_color and troop_end == 0):
            self.board[new_position[1]][new_position[0]].troop_number += troops_to_move
            self.board[column][row].troop_number -= troops_to_move
            self.board[new_position[1]][new_position[0]].color = self.our_color

        # unfog squares
        for x, row in enumerate(self.board):
            for y, square in enumerate(row):
                if square.color == self.our_color:  # if the square is our color
                    for trans in transform:
                        new_pos = [x+trans[1], y+trans[0]]
                        ref = self.board[new_pos[0]][new_pos[1]]
                        try:
                            ref.is_fogged = False
                            if ref.square_type == 6:
                                ref.square_type = 4  # assume fog obstacles are mountains
                            if ref.square_type == 5:
                                ref.square_type = 0

                        except IndexError:
                            continue
        # add to queued moves
        self.queued_moves.append(move)
        return True

    def undo_move(self, move: backend.Move.Move):
        if self.queued_moves[-1] != move:  # can't undo the move
            return False
        self.board = deepcopy(self._previous_board_positions[-1])
        self.queued_moves.pop(-1)
        self._previous_board_positions.pop(-1)
        return True

    def __str__(self):
        out = ''
        piece_visualize = {0: "_", 1: "$", 2: "G", 3: "~", 4: "^", 5: "F", 6: "?", 7: "~"}

        for row in b.board:
            for ind, square in enumerate(row):
                our_color_index = colors.index(self.our_color)
                if square.color:
                    out += abbrev_colors[our_color_index][0]\
                           + str(piece_visualize[square.square_type])\
                           + abbrev_colors[our_color_index][1]

                else:
                    out += "_" + str(piece_visualize[square.square_type]) + "_"
                if ind+1 < len(row):
                    out += ' '
            out += '\n'
        return out
