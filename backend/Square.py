# PIECE IDS:
"""
0: empty/normal
1 (with color/neutral) city
2 (with color/neutral) general
3 (with color/neutral) swamp
4 mountain
5 neutral square
6 fog
7 fog obstacle
8 fog swamp
"""

# ATTRIBUTES
"""
is_general: is the square a general?
is_fogged: is the square fogged?
is_swamp: is the square swamp?
is_city: is the square a city?
troop_number: the troop number on the square
is_our_color: is the square our color (false if neutral)
troop_cost: the cost to capture this square (0 if captured/empty, -1 if not capturable (mountain)
"""

import Constants
class Square:
    def __init__(self, creation_string, troop_number):
        self.args = creation_string.replace("attackable", "").replace("selectable", "").split(" ")
        self.is_general = False
        self.is_fogged = False
        self.is_swamp = False
        self.is_city = False
        self.is_mountain = False
        self.color = ''
        self.troop_number = troop_number
        if len(self.args) == 0:  # empty
            self.square_type = 0
        if len(self.args) == 1 and self.args[0] in Constants.colors:
            self.square_type = 1
        elif self.args[0] in Constants.colors:  # colored square
            self.color = self.args[1]
        if 'swamp' in self.args:  # is an available swamp
            self.is_swamp = True
        if 'fog' in self.args:
            self.is_fogged = True
        if 'mountain' in self.args:  # is mountain
            self.is_mountain = True
        if 'city' in self.args:
            self.is_city = True
        if 'general' in self.args:
            self.is_general = True
        if self.is_general:
            self.square_type = 2
        if self.is_city:
            self.square_type = 1
        if self.is_fogged:
            self.square_type = 6
        if self.is_swamp and self.is_fogged:
            self.square_type = 8
        if 'obstacle' in self.args and self.is_fogged:
            self.square_type = 7
