# DIRECTION
"""
0: up
1: right
2: down
3: left
"""
from typing import overload


class Move:
    def __init__(self, row: int = None, column: int = None, direction: int = None, is_50_percent: bool = None):
        self.direction = direction
        self.is_50_percent = is_50_percent
        self.row = row
        self.column = column
        self.is_null = self.direction is None \
                       and self.is_50_percent is None \
                       and self.row is None \
                       and self.column is None
        if (self.direction is None
            or self.is_50_percent is None
            or self.row is None
            or self.column is None) \
                       and not self.is_null:
            raise Exception("you must define all or none of the Move class methods!")

    def __str__(self):
        if self.is_null:
            return "null"
        visualize = ['up', 'right', 'down', 'left']
        s = f'moving from ({self.column}, {self.row}) {visualize[self.direction]}.'
        if self.is_50_percent:
            s += ' 50% move'
        return s
