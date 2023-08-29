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
import sys
import backend.Constants
# ATTRIBUTES
"""
is_general: is the square a general?
is_fogged: is the square fogged?
is_swamp: is the square swamp?
is_city: is the square a city?
troop_number: the troop number on the square
troop_cost: the cost to capture this square (0 if captured/empty, -1 if not capturable (mountain)
"""


class Square:
    def __init__(self, creation_string, troop_number,
                 override_city: bool = False,
                 override_general: bool = False,
                 override_mountain: bool = False,
                 override_color_from_remebrance: str = "") -> None:
        """
        Initialize a new Square
        :param creation_string: the raw html creation storing
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
        self.remembered_color = False
        self.creation_string = creation_string
        self.color = ''
        self.troop_number = troop_number
        self._backup = -1
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
        if override_city:
            self.is_city = True
        if override_general:
            self.is_general = True
        if override_mountain:
            self.is_mountain = True
        if override_color_from_remebrance and self.color == "":
            self.remembered_color = True
            self.color = override_color_from_remebrance
        if self.is_mountain:
            self.square_type = 4
            return
        if self.is_general:
            self.square_type = 2
            return
        if self.is_city:
            self.square_type = 1
            return
        if 'obstacle' in self.args and self.is_fogged:
            self.square_type = 6
            return
        if self.is_fogged:
            self.square_type = 5
            return


        try:
            self.square_type
        except AttributeError:
            print(self.args, troop_number)
            sys.exit(1)

    def __str__(self) -> str:
        return f"square type: {self.square_type}" \
               f" is_swamp: {self.is_swamp}" \
               f" is_mountain: {self.is_mountain}" \
               f" is_general: {self.is_general}" \
               f" is_fogged: {self.is_fogged}" \
               f" is_city: {self.is_city}," \
               f" color_remembered: {self.remembered_color}" \
               f" color: {self.color}"

    def __eq__(self, other):
        return self.square_type == other.square_type\
            and self.is_swamp == other.is_swamp \
            and self.is_mountain == other.is_mountain\
            and self.is_general == other.is_general\
            and self.is_fogged == other.is_fogged\
            and self.is_city == other.is_city\
            and self.remembered_color == other.remembered_color\
            and self.color == other.color
