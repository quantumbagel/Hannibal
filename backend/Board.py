import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class Board:
    def __init__(self, height, width, webdriver_board: webdriver.Chrome):
        self.board_driver = webdriver_board.find_element(By.XPATH, "/html/body/div/div/div/div[2]/table/tbody")
        self.height = height
        self.width = width
        self.rows = self.board_driver.find_elements(By.TAG_NAME, "tr")
        self.board_elem = []
        for row in self.rows:
            self.board_elem.append(row.find_elements(By.TAG_NAME, "td"))

    def get(self):
        board_html = self.board_driver.get_attribute('outerHTML').replace('<tr>', "").replace("</tr>", "[endrow]").replace('"', "")
        board_html = [i.replace('</td>', "").replace(' class="', "").replace("</tbody>", "") for i in board_html.split("<td class=")][1:]
        s_list = []
        t = []
        for item in board_html:
            square_count = -1
            is_endrow = '[endrow]' in item
            if ">" in item:  # this means that the item has army
                square_count = item.split('>')[1].replace("[endrow]", "")
                item = item.split('>')[0]
            t.append([item.replace('[endrow]', ''), square_count])
            if is_endrow:
                s_list.append(t)
                t = []

        return s_list

