class Settings:
    """Settings for the PathFinding program"""

    def __init__(self):
        # Screen
        self.screen_w = 650
        self.screen_h = 650
        self.background = (128, 128, 128)
        self.title = 'A* Path Finding Program'
        self.number_rows = 30
        self.number_cols = 30
        # Square calculations
        self.sq_width = self.screen_w // self.number_cols
        self.sq_height = self.screen_h // self.number_rows
        # Colors
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.orange = (246, 190, 9)
        self.purple = (128, 0, 128)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
