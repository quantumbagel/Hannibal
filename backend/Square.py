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
import sys
import backend.Constants
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


class Square:
    def __init__(self, creation_string, troop_number) -> None:
        """
        Initialize a new Square
        :param creation_string: the raw html creation string
        :param troop_number: the troops in that square
        """
        self.args = creation_string \
            .replace("attackable", "") \
            .replace("selectable", "") \
            .replace('selected', "") \
            .replace('neutral', "") \
            .split(" ")
        self.args = [i for i in self.args if i != ""]
        self.is_general = False
        self.is_fogged = False
        self.is_swamp = False
        self.is_city = False
        self.is_mountain = False
        self.creation_string = creation_string
        self.color = ''
        self.troop_number = troop_number
        if len(self.args) == 0:  # empty
            self.square_type = 0
        elif len(self.args) == 1 and self.args[0] in backend.Constants.colors:
            self.square_type = 1
            self.color = self.args[0].replace(" ", "")
        elif self.args[0] in backend.Constants.colors:  # colored square
            self.color = self.args[0].replace(" ", "")
        # there are so many if statements that I almost died
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
        if self.color == '' and troop_number > 0:
            self.square_type = 5
            return
        if self.is_mountain:
            self.square_type = 4
            return
        if self.is_general:
            self.square_type = 2
            return
        if self.is_city:
            self.square_type = 1
            return
        if self.is_fogged:
            self.square_type = 6
            return
        if self.is_swamp and self.is_fogged:
            self.square_type = 8
            return
        if 'obstacle' in self.args and self.is_fogged:
            self.square_type = 7
            return
        try:
            self.square_type
        except AttributeError:
            print(self.args, troop_number)
            sys.exit(1)

    def __str__(self) -> str:
        return f"square type: {self.square_type} is_swamp: {self.is_swamp} is_mountain: {self.is_mountain} is_general: {self.is_general} is_fogged: {self.is_fogged} is_city: {self.is_city}"
