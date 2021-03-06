import arcade

import settings

from menu import MenuView
from rays_level import GameView
from alex_level import Alexlevel
from alans_level import AlansGame
from jeanluc_level import JeanlucView


class Director(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.view_index = 0
        self.views = [
            MenuView,
            GameView,
            #Alexlevel,
            JeanlucView,
            AlansGame
            
        ]
        self.next_view()

    def next_view(self):
        next_view = self.views[self.view_index]()
        next_view.director = self
        self.show_view(next_view)
        self.view_index = (self.view_index + 1) % len(self.views)


def main():
    window = Director(settings.WIDTH, settings.HEIGHT, "Game")
    arcade.run()


if __name__ == "__main__":
    main()
