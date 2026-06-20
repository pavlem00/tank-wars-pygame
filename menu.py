class Menu:
    def __init__(self):
        self.options = ["Singleplayer",
                        "Multiplayer",
                        "Tutorial",
                        "Quit"]
        self.selected = 0

    def move_up(self):
        self.selected = (self.selected-1) % len(self.options)
    
    def move_down(self):
        self.selected = (self.selected+1) % len(self.options)

    def get_selected(self):
        return self.options[self.selected]