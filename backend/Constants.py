colors = ["red",
          "lightblue",
          "green",
          "teal",
          "orange",
          "pink",
          "purple",
          "maroon",
          "yellow",
          "brown",
          "blue",
          "purpleblue"]
abbrev_colors = ['RR', 'LB', 'GG', 'TT', "OO", "PN", "PP", "MM", "YY", "BR", "BB", "PB"]
piece_visualize = {0: "_", 1: "$", 2: "G", 3: "~", 4: "^", 5: "F", 6: "?", 7: "~"}
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
GIO_GAME_LEADERBOARD_XPATH = "/html/body/div/div/div/table"
GIO_GAME_CHAT_XPATH = "/html/body/div/div/div/div[3]/div/div"
GIO_GAME_CHAT_ENTER_TEXT_XPATH = "/html/body/div/div/div/div[3]/div/input"
# PIECE IDS:
"""
0: empty/normal
1 (with color/neutral) city
2 (with color/neutral) general
3 (with color/neutral) swamp
4 mountain
5 fog
6 fog obstacle
"""
# DIRECTION
"""
0: up
1: right
2: down
3: left
"""