# DIRECTION
"""
0: up
1: right
2: down
3: left
"""


class Move:
    def __init__(self, row, column, direction, is_50_percent):
        self.direction = direction
        self.is_50_percent = is_50_percent
        self.row = row
        self.column = column
    def __str__(self):
        visualize = ['up', 'right', 'down', 'left']
        s = f'moving from ({self.column}, {self.row}) {visualize[self.direction]}.'
        if self.is_50_percent:
            s += ' 50% move'
        return s
