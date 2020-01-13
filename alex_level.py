import arcade

import settings
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

class Alexlevel(arcade.View):
    def __init__(self,):
        self.wall_list = None
        self.player_list = None
        self.coin_list = None

        self.player_sprite = None
        
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Alex Level", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
                         
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        self.director.next_view()

    def setup():

        self.player_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = "/Users/alexpassarelli/Downloads/cpt/cloud.jpg"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Alexlevel()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
