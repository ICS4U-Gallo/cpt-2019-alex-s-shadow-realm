import arcade

import settings
CHARACTER_SCALING = 1.5
TILE_SCALING = 0.5
# COIN_SCALING = 0.5

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

MOVEMENT_SPEED = 4
UPDATES_PER_FRAME = 7
GRAVITY = 0.65
PLAYER_JUMP_SPEED = 13

IMAGE_WIDTH = 1350
SCROLL_SPEED = 5

LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 250


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename, scale=CHARACTER_SCALING),
        arcade.load_texture(filename, scale=CHARACTER_SCALING, mirrored=True)
    ]


class Alexlevel(arcade.View):


    def __init__(self):


        super().__init__()


        arcade.set_background_color(arcade.color.WHITE)

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Physics Engine
        self.physics_engine = None

        # Set up the player
        image_source = "images/Alex Images/Owlet_Monster.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)


        # Name of map file to load
        map_name = "images\Alex Images\map\map.tmx"
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(arcade.color.ICEBERG)


 
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        # self.background = arcade.load_texture("images/Alex Images/glacial_mountains_preview_lightened.png")
        
        # Create the ground

        # for x in range(-settings.WIDTH, settings.WIDTH, 64):
        #     wall = arcade.Sprite("images/Alex Images/128x128/GrassJoinHillLeft&Right.png", TILE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.wall_list.append(wall)

        # coordinate_list = [[500, 200],
        #                    [564, 200],
        #                    [768, 96]]

        # for coordinate in coordinate_list:
        #     # Add a crate on the ground
        #     wall = arcade.Sprite("images/Alex Images/128x128/GrassCliffMid.png", TILE_SCALING)
        #     wall.position = coordinate
        #     self.wall_list.append(wall)
        # # Adding Coins



        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)


     
    def on_draw(self):
        arcade.start_render()


                                      

        self.wall_list.draw()
        self.coin_list.draw()

        self.player_list.draw()





    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        # Move the player with the physics engine

        self.physics_engine.update()


        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + settings.WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True



        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                settings.WIDTH + self.view_left,
                                self.view_bottom,
                                settings.HEIGHT + self.view_bottom)

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
