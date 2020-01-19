import arcade

import settings
CHARACTER_SCALING = 1.5
TILE_SCALING = 0.5
# COIN_SCALING = 0.5
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
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

GRID_PIXEL_SIZE = (TILE_SCALING)

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
        
        self._score = 0
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

      
        self.end_of_map = 0
        # self.background = arcade.load_texture("images/Alex Images/glacial_mountains_preview_lightened.png")
        

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

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)
                                                            

        # end game here


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

        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            self._score += 1
                

        if self.player_sprite.center_x >= 500:
            self.win = True
            finish_view = FinishView()
            self._score += 100*(self._score)
            finish_view.score = self._score
            finish_view.win = True
            finish_view.director = self.director
            self.window.show_view(finish_view)
            print(f"Your Score: {self._score}")
class FinishView(arcade.View):

    def on_draw(self):
        arcade.start_render()

        # print win/lose screen
        if self.win is False:
            arcade.set_background_color(arcade.color.RED)
            arcade.draw_text("YOU LOSE", settings.WIDTH//2, 550, arcade.color.BLACK,
                             100, align="center", anchor_x="center",
                             anchor_y="center")
        elif self.win is True:
            arcade.set_background_color(arcade.color.GREEN)
            arcade.draw_text("YOU WIN", settings.WIDTH//2, 550, arcade.color.BLACK, 100,
                             align="center", anchor_x="center",
                             anchor_y="center")

        # buttons

        arcade.draw_text(f"YOUR SCORE WAS: {self.score}", settings.WIDTH//2, 450,
                         arcade.color.BLACK, 50, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_rectangle_filled(settings.WIDTH//2, 300, 300, 100,
                                     arcade.color.BLACK)
        arcade.draw_rectangle_filled(settings.WIDTH//2, 100, 300, 100,
                                     arcade.color.BLACK)
        arcade.draw_text("CLICK TO TRY  \n AGAIN", settings.WIDTH//2, 300,
                         arcade.color.WHITE, 25, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("CLICK TO SUBMIT  \n SCORE", WIDTH//2, 100,
                         arcade.color.WHITE, 25, align="center",
                         anchor_x="center", anchor_y="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):

        if settings.WIDTH//2 - 150 < _x < settings.WIDTH//2 + 150 and 250 < _y < 350:
            game_view = GameView()
            self.window.show_view(game_view)

        elif settings.WIDTH//2 - 150 < _x < settings.WIDTH//2 + 150 and 50 < _y < 150:
            score_view = ScoreView()
            score_view.score = self.score
            score_view.director = self.director
            self.window.show_view(score_view)
class ScoreView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.name = " "
        self.submit = False
        self.name_taken = False
        self.show_time = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(settings.WIDTH//2, settings.HEIGHT//2, settings.WIDTH, settings.HEIGHT,
                                      background)
        # typing name
        if self.submit is False:
            arcade.draw_text("ENTER NAME:", 100, 310, arcade.color.WHITE, 80,)

            arcade.draw_text(self.name, 750, 310, arcade.color.WHITE, 80)

        # highscore
        else:
            arcade.draw_text("HIGHSCORES", WIDTH//2, 600,
                             arcade.color.AQUA, 120,
                             align="center", anchor_x="center",
                             anchor_y="center")
            arcade.draw_text("RANK", WIDTH//3 - 100, 475,
                             arcade.color.NEON_GREEN, 70,
                             align="center", anchor_x="center",
                             anchor_y="center")
            arcade.draw_text("SCORE", WIDTH//2, 475,
                             arcade.color.NEON_GREEN, 70,
                             align="center", anchor_x="center",
                             anchor_y="center")
            arcade.draw_text("NAME", WIDTH - WIDTH//3 + 100, 475,
                             arcade.color.NEON_GREEN, 70,
                             align="center", anchor_x="center",
                             anchor_y="center")

            leaderboard = (find_highscores())

            for i in range(6):
                if leaderboard[i] == 0:
                    leaderboard[i] = " "
            leaderboard.insert(2, arcade.color.GOLD)
            leaderboard.insert(5, arcade.color.SILVER)
            leaderboard.insert(8, arcade.color.BRONZE)

            top = 350
            index = 0
            suffix = ["ST", "ND", "RD", "TH"]
            for i in range(3):
                arcade.draw_text(leaderboard[index], 875, top,
                                 leaderboard[index + 2], 50)
                arcade.draw_text(str(leaderboard[index + 1]), 560, top,
                                 leaderboard[index + 2], 50)
                arcade.draw_text(str(index//3 + 1) + suffix[index//3], 250,
                                 top, leaderboard[index + 2], 50)

                top -= 75
                index += 3
            if self.stats[0] > 3:
                top -= 25
                arcade.draw_text(str(self.stats[2]), 875, top,
                                 arcade.color.AFRICAN_VIOLET, 50)
                arcade.draw_text(str(self.stats[1]), 560, top,
                                 arcade.color.AFRICAN_VIOLET, 50)
                arcade.draw_text(str(self.stats[0]) + suffix[3], 250, top,
                                 arcade.color.AFRICAN_VIOLET, 50)
            else:
                arcade.draw_text("NICE JOB YOU MADE THE BOARD!", WIDTH//2, top,
                                 arcade.color.NEON_GREEN, 50, align="center",
                                 anchor_x="center", anchor_y="center")
            arcade.draw_text("PRESS ENTER TO CONTINUE  ->", 1100, 50,
                             arcade.color.RED, 25, align="center",
                             anchor_x="center", anchor_y="center")

        # name taken
        if self.name_taken is True:
            arcade.draw_text("NAME ALREADY TAKEN", WIDTH//2, 500,
                             arcade.color.RED, 80, align="center",
                             anchor_x="center", anchor_y="center")

    # flash message if name taken

    def update(self, delta_time):

        if self.name_taken is True:
            self.show_time += 1

        if self.show_time > 60:
            self.name_taken = False
            self.show_time = 0

    # type name

    def on_key_press(self, key, modifiers):
        if (key == arcade.key.BACKSPACE
           and len(self.name) > 1
           and self.submit is False):
            self.name = self.name[:-1]

        elif (key != arcade.key.BACKSPACE
                and key != arcade.key.ENTER
                and len(self.name) < 8
                and self.submit is False):
            self.name += (chr(key)).upper()

        elif (key == arcade.key.ENTER) and self.submit is True:
            self.director.next_view()

    # enter and check name/score
    def on_key_release(self, key, modifiers):
        if (key == arcade.key.ENTER
           and self.name is not " "
           and self.submit is False):

            if check_name(self.name) is True:
                self.submit = True
                self.stats = save_score(self.name, self.score)

            else:
                self.name_taken = True

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
