import importlib
import random
import sys
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from backend.Timer import Timer
from backend.Board import Board
import ruamel.yaml
from inspect import isclass

print("GameManager.py")
print("note: go to backend/config.yaml to configure GameManager.")
current_turn = 0
config = ruamel.yaml.YAML().load(open('backend/config.yaml'))
ai = importlib.import_module(config["ai"])
class_name = [x for x in dir(ai) if isclass(getattr(ai, x)) and x not in ['AI', 'Move', 'Square', 'Timer']]
if len(class_name) > 1:
    print('ERROR: inconclusive classes')
    print(class_name)
    sys.exit(1)
link = "https://generals.io/games/hannibaltest"
driver = webdriver.Chrome()
driver.get(link)
def join_custom_room(id):
    global driver

    pass

def wait_for_next_turn():
    global current_turn
    turn_counter = driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]")
    while True:
        check_it = turn_counter.text.split(" ")[1]
        c_t = 0
        if check_it.endswith('.'):
            c_t = 0.5
        c_t += int(check_it.replace(".", ""))
        if c_t != current_turn:
            current_turn = c_t
            return current_turn


def is_game_over():
    """
    A function to check if the game is over yet
    :return: 0 if game is ongoing, 1 if we won, 2 if we lost by capture, 3 if we lost by afk
    """
    elem = driver.find_elements(By.XPATH, "/html/body/div/div/div/div[3]/center")
    if len(elem) == 0:
        return 0
    elem = elem[0]
    reason = elem.find_element(By.XPATH, "/html/body/div/div/div/div[3]/center/p/span").text
    if 'You went AFK.' in reason:
        return 3
    if reason == '':
        return 1
    if 'You were defeated by' in reason:
        return 2






def run_game():
    WebDriverWait(driver, 100).until(
        expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/table/tbody")))
    body = driver.find_element(By.XPATH, "/html/body")
    b = Board(driver, 'red')
    bot = getattr(ai, class_name[0])()
    for _ in range(5):
        body.send_keys("9")
    while True:
        b.update()
        b.update_moves()
        move = bot.get_move(b.moves, b.board, Timer(time.time(), 250))
        print(move)
        if not move.is_null:
            b.play_move(move)
        i = is_game_over()
        if i == 1:
            print("Bot has won!")
            return 1
        if i == 2:
            print("Bot was captured :(")
            return 0
        if i == 3:
            print("Bot went AFK xD")
            return 0
        wait_for_next_turn()


run_game()