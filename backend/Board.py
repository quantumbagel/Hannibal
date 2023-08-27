import sys
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
import backend.Move
from backend.Square import Square
from backend.Move import Move
from backend.log import dprint


class Board:
    def __init__(self, webdriver_board: webdriver.Chrome, our_color) -> None:
        self.board_driver = webdriver_board.find_element(By.XPATH, "/html/body/div/div/div/div[2]/table/tbody")
        self.our_color = our_color
        self.moves = []
        self.rows = self.board_driver.find_elements(By.TAG_NAME, "tr")
        self.board = []
        self.update()
        self.height = len(self.board)
        self.width = len(self.board[0])

    def update(self) -> None:
        """
        Update the board and moves
        :return: None
        """
        arrows = ['\u2190', '\u2191', '\u2192', '\u2193']
        board_html = self.board_driver.\
            get_attribute('outerHTML').\
            replace('<tr>', "").\
            replace("</tr>", "[end]").\
            replace('"', "")
        board_html = [i.replace('></td>', "").replace(' class="', "").replace("</tbody>", "") for i in
                      board_html.split("<td class=")][1:]
        # the above jank is a html parser that's ~35 times faster than using native selenium
        new_board = []
        temp_board = []
        for item in board_html:
            square_count = -1
            is_end_row = '[end]' in item  # flag for row ending
            if ">" in item:  # this means that the item has army
                next_loop = False  # more html parsing to ensure that the arrows don't screw with the table
                for i in item:  # we technically don't need this
                    if i in arrows:  # it's just for lag
                        next_loop = True
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
                    print("VALUE ERROR", item)
                    print(e)
                    sys.exit(1)
                item = item.split('>')[0]
            temp_board.append(Square(item.replace('[end]', ''), square_count))
            if is_end_row:
                new_board.append(temp_board)
                temp_board = []
        self.board = new_board
        self._update_moves()

    def _update_moves(self) -> list[backend.Move.Move]:
        """
        update self.moves based on self.board
        :return: the new moves.
        """
        self.moves = []
        transform = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        for y, column in enumerate(self.board):
            for x, square in enumerate(column):
                if square.color == self.our_color:
                    for fifty_percent in range(2):
                        exit_early = False
                        for direction in range(4):
                            new_position = [x + transform[direction][0], y + transform[direction][1]]
                            if new_position[0] >= self.width\
                                    or new_position[0] < 0\
                                    or new_position[1] >= self.height\
                                    or new_position[1] < 0:
                                continue
                            print(new_position, self.board[new_position[1]])
                            if self.board[new_position[1]][new_position[0]].is_mountain:  # mountain
                                continue
                            if self.board[y][x].troop_number < 2:  # not enough troops
                                exit_early = True
                                break
                            self.moves.append(Move(y, x, direction, fifty_percent))
                        if exit_early:
                            break
        return self.moves

    def click(self, column, row):
        """
        Click on the square at (row, column)
        :param column: the column the square is in
        :param row: the row the square is in
        :return: 1 if successfully clicked, 0 if not
        """
        elem = self.board_driver. \
            find_element("xpath", f"/html/body/div/div/div/div[2]/table/tbody/tr[{str(row + 1)}]/td[{str(column + 1)}]")
        try:
            elem.click()
            return 1
        except selenium.common.ElementClickInterceptedException:
            dprint("Board.click", "Board click interception! Game over? this could also be an alert/popup")
            return 0

    def play_move(self, move):
        """
        Play the Move object. TODO: ignore arrows, implement 50%
        :param move:
        :return:
        """
        transform = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        if not self.click(move.column, move.row):
            return
        self.click(move.column + transform[move.direction][0], move.row + transform[move.direction][1])
