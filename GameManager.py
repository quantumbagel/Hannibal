import importlib
import json
import sys
import time
import selenium.common
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from backend.Timer import Timer
from backend.Board import Board
import ruamel.yaml
from inspect import isclass
from backend.log import dprint

current_turn = 0
config = ruamel.yaml.YAML().load(open('backend/config.yaml'))
ai_import = config['ai'].split('.')
ai = importlib.import_module('.'.join(ai_import[:-1]))
class_name = [x for x in dir(ai) if isclass(getattr(ai, x))]
if ai_import[-1] not in class_name:
    dprint('GameManager', f'error: The referenced class does not exist!'
                          f' class name: {ai_import[-1]} module: {".".join(ai_import[:-1])}')
    sys.exit(1)


class GameManager:
    GIO_HOME = 'https:/generals.io'
    GIO_CUSTOM_GAME_PREFIX = 'https://generals.io/games/'
    GIO_HOME_PLAY_BUTTON_XPATH = "/html/body/div/div/div/center/div[1]/div[2]/button[1]"
    GIO_GAME_TURN_COUNTER_XPATH = "/html/body/div/div/div/div[4]"
    GIO_GAME_OVER_XPATH = "/html/body/div/div/div/div[3]/center"
    GIO_GAME_OVER_TEXT_XPATH = "/html/body/div/div/div/div[3]/center/p/span"
    GIO_GAME_TABLE_XPATH = "/html/body/div/div/div/div[2]/table/tbody"
    GIO_SEND_KEY_XPATH = "/html/body"
    GIO_HOME_1v1_BUTTON_XPATH = "/html/body/div/div/div/center/div[4]/div/center/button[2]"
    GIO_HOME_FFA_BUTTON_XPATH = "/html/body/div/div/div/center/div[4]/div/center/button[1]"
    VALID_BROWSER = ['edge', 'chrome', 'firefox', 'safari']
    GIO_CUSTOM_GAME_JOIN_BUTTON_XPATH = ""  # implement

    def __init__(self, configuration) -> None:
        """
        Initialize the GameManager.
        :param configuration: The json configuration from config.yaml
        """
        try:
            dprint("GameManager.init", 'creating webdriver...')
            driver_browser = configuration['driver'].lower()
            if driver_browser not in GameManager.VALID_BROWSER:
                dprint("GameManager.init", f"error: browser not valid (config.yaml). got: {driver_browser}"
                                           f" expected one of {GameManager.VALID_BROWSER}"
                                           f" note: if you use internet explorer"
                                           f", sucks to be you.")
                sys.exit(1)
            if driver_browser == 'edge':
                self.driver = webdriver.Edge()
            elif driver_browser == 'chrome':
                self.driver = webdriver.Chrome()
            elif driver_browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif driver_browser == 'safari':
                self.driver = webdriver.Safari()
        except selenium.common.NoSuchDriverException:
            dprint("GameManager.init", "error: could not create driver. this could be because of"
                                       " a non-existent internet connection"
                                       " or the driver package has not been installed."
                                       " if the latter is true, go to https://pypi.org/package/selenium and download"
                                       " the correct webdriver.")
            sys.exit(1)
        self.configuration = configuration
        self.cookies = json.load(open('session.json'))

    def enter_game(self) -> None:
        """
        Join the game according to self.configuration
        :return: None
        """
        if 'custom' not in self.configuration['auto_join']:  # not custom game, load homepage to enter 1v1/ffa queues
            dprint("GameManager.enter_game", f"Loading {GameManager.GIO_HOME}")
            self.driver.get(GameManager.GIO_HOME)
        else:  # custom game, load custom game page
            dprint("GameManager.enter_game", f"Loading {GameManager.GIO_CUSTOM_GAME_PREFIX}")
            self.driver.get(GameManager.GIO_CUSTOM_GAME_PREFIX + self.configuration['auto_join'].split('/')[1])
        for cookie in self.cookies:  # load cookies
            self.driver.add_cookie(cookie)
        self.driver.refresh()  # reload
        if not self.configuration['auto_join']:  # if we don't have a game mode, just stop here. run_game will wait
            return
        if self.configuration['auto_join'].lower() == '1v1':  # join 1v1 queue
            self.driver.find_element(By.XPATH, GameManager.GIO_HOME_PLAY_BUTTON_XPATH).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                self.driver.find_element(By.XPATH, GameManager.GIO_HOME_1v1_BUTTON_XPATH))).click()
        if self.configuration['auto_join'].lower() == 'ffa':  # join ffa queue
            self.driver.find_element(By.XPATH, GameManager.GIO_HOME_PLAY_BUTTON_XPATH).click()
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                self.driver.find_element(By.XPATH, GameManager.GIO_HOME_FFA_BUTTON_XPATH))).click()
        if 'custom' in self.configuration['auto_join']:
            self.driver.find_element(By.XPATH, GameManager.GIO_CUSTOM_GAME_PREFIX).click()
        #  if we made it here without triggering an if statement, then the auto_join parameter is invalid,
        #  and we will ask the user to start the game from the generals.io homepage

    def wait_for_next_turn(self) -> float:
        """
        Wait for the next turn by watching the turn counter in the top-left.
        Assumes game in progress and will crash otherwise.
        :return: the current turn
        """
        global current_turn
        turn_counter = self.driver.find_element(By.XPATH, GameManager.GIO_GAME_TURN_COUNTER_XPATH)
        while True:
            check_it = turn_counter.text.split(" ")[1]
            c_t = 0
            if check_it.endswith('.'):
                c_t = 0.5
            c_t += int(check_it.replace(".", ""))
            if c_t != current_turn:
                current_turn = c_t
                return current_turn

    def is_game_over(self) -> int:
        """
        A function to check if the game is over yet
        :return: 0 if game is ongoing, 1 if we won, 2 if we lost by capture, 3 if we lost by afk
        """
        elem = self.driver.find_elements(By.XPATH, GameManager.GIO_CUSTOM_GAME_PREFIX)
        if len(elem) == 0:
            return 0
        elem = elem[0]
        reason = elem.find_element(By.XPATH, GameManager.GIO_GAME_OVER_TEXT_XPATH).text
        if 'You went AFK.' in reason:
            return 3
        if reason == '':
            return 1
        if 'You were defeated by' in reason:
            return 2

    def run_game(self) -> int:
        """
        Run the game loop.
        :return: 1 if we won, 0 if we lost.
        """
        WebDriverWait(self.driver, 100000000).until(
            expected_conditions.visibility_of_element_located((By.XPATH, GameManager.GIO_GAME_TABLE_XPATH)))
        body = self.driver.find_element(By.XPATH, GameManager.GIO_SEND_KEY_XPATH)
        b = Board(self.driver, 'red')
        bot = getattr(ai, class_name[0])()
        for _ in range(5):  # zoom out so we can see (and click) on everything
            body.send_keys("9")
        while True:
            b.update()  # update squares and moves
            move = bot.get_move(b.moves, b.board, Timer(time.time(), 250))  # get move (250 ms)
            if not move.is_null:  # if we want to move, move
                dprint("GameManager.run_game", "Playing move: ", move)
                b.play_move(move)
            i = self.is_game_over()  # has the game ended?
            if i == 1:
                dprint("GameManager.run_game", "The bot has won!")
                return 1
            if i == 2:
                dprint("GameManager.run_game", "The bot was captured :(")
                return 0
            if i == 3:
                dprint("GameManager.run_game", "The bot went AFK xD")
                return 0
            self.wait_for_next_turn()


g = GameManager(config)
while True:
    g.enter_game()
    g.run_game()
