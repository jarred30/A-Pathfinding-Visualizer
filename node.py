class Node:
    def __init__(self, x=None, y=None, f_cost=None, g_cost=None, h_cost=None, old_x=None, old_y=None):
        """This class represents one node in the path"""
        self.old_x = old_x
        self.old_y = old_y
        self.f_cost = f_cost
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.x = x
        self.y = y
