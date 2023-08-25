import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from backend.Square import Square
from backend.Move import Move


class Board:
    def __init__(self, webdriver_board: webdriver.Chrome, our_color):
        self.board_driver = webdriver_board.find_element(By.XPATH, "/html/body/div/div/div/div[2]/table/tbody")
        self.our_color = our_color
        self.moves = []
        self.rows = self.board_driver.find_elements(By.TAG_NAME, "tr")
        self.board = []
        self.update()
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.update_moves()


    def update(self):
        arrows = ['\u2190', '\u2191', '\u2192', '\u2193']
        board_html = self.board_driver.get_attribute('outerHTML').replace('<tr>', "").replace("</tr>",
                                                                                              "[endrow]").replace('"',
                                                                                                                  "")
        board_html = [i.replace('></td>', "").replace(' class="', "").replace("</tbody>", "") for i in
                      board_html.split("<td class=")][1:]
        board_strings = []
        new_board = []
        temp_string = []
        temp_board = []
        for item in board_html:
            square_count = -1
            is_endrow = '[endrow]' in item
            if ">" in item:  # this means that the item has army
                next_loop = False
                for i in item:
                    if i in arrows:
                        print("arrow, ignoring")
                        next_loop = True
                        break
                if next_loop:
                    continue
                try:
                    square_count = int(item.replace("</td", "").split('>')[1].replace("[endrow]", "")
                                       .replace("<div class=center-horizontal style=bottom: 0px;", "")
                                       .replace("<div class=center-horizontal style=top: 0px;", "")
                                       .replace("<div class=center-vertical style=left: 0px;", "")
                                       .replace("<div class=center-vertical style=right: 0px;", ""))
                except ValueError as e:
                    print("VALUE ERROR", item)
                    print(e)
                    sys.exit(1)
                item = item.split('>')[0]
            temp_string.append([item.replace('[endrow]', ''), square_count])
            temp_board.append(Square(item.replace('[endrow]', ''), square_count))
            if is_endrow:
                board_strings.append(temp_string)
                temp_string = []
                new_board.append(temp_board)
                temp_board = []
        self.board = new_board
        return board_strings

    def update_moves(self):
        self.moves = []
        transform = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        for y, column in enumerate(self.board):
            for x, square in enumerate(column):
                if square.color == self.our_color:
                    for fifty_percent in range(2):
                        exit_early = False
                        for direction in range(4):
                            new_position = [x + transform[direction][0], y + transform[direction][1]]
                            if new_position[0] >= self.width or new_position[0] < 0 or new_position[1] >= self.height or \
                                    new_position[1] < 0:
                                continue
                            if self.board[new_position[1]][new_position[0]].is_mountain:  # mountain
                                continue
                            if self.board[y][x].troop_number < 2:  # not enough troops
                                exit_early = True
                                break
                            self.moves.append(Move(y, x, direction, fifty_percent))
                        if exit_early:
                            break
        return self.moves
