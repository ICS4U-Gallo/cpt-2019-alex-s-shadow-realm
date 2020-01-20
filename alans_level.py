import arcade


class GameProperties:
    '''Game Properties class: Static for Game properties --
    similar as static method but cleaner code
    Attributes:
        SCREEN_WIDTH: screen width
        SCREEN_HEIGHT: screen height
        SCREEN_TITLE: displays title at the top of the screen
        CHARACTER_SCALING: character scaling relative to other objects
        TILE_SCALING: tile scaling
        JERRY_SCALING: jerry the mouse scaling
        TOM_MOVEMENT_SPEED: tom the cat movement speed
        GAME_RUNNING: ensures that the game is running
        GAME_OVER: condition for the end of the game
        '''
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 650
    SCREEN_TITLE = "Alan's Tom & Jerry Game"
    CHARACTER_SCALING = 1
    TILE_SCALING = 0.5
    JERRY_SCALING = 0.5
    TOM_MOVEMENT_SPEED = 5
    GAME_RUNNING = 1
    GAME_OVER = 2


class AlansGame(arcade.Window):
    '''Game class
        Attributes:
            jerry_list: list of jerry
            wall_list: list of walls
            tom_list: list of tom
            tom_sprite = None
            score: score of the game
            endgame: end game status
            current_state: current game status
            eat_jerry_sound: tom's eating sound
            jump_sound: finished game sound
            arcade.set_background_color:background color
    '''
    def __init__(self):
        # Using the parent class (inherent class) init class and set up the game view
        super().__init__(GameProperties.SCREEN_WIDTH, GameProperties.SCREEN_HEIGHT, GameProperties.SCREEN_TITLE)
        self.jerry_list = None
        self.wall_list = None
        self.tom_list = None

        self.tom_sprite = None

        self.score = 0
        self.endgame = 0
        self.current_state = GameProperties.GAME_RUNNING

        self.eat_jerry_sound = arcade.load_sound("images/alans_images/eat.wav")
        self.jump_sound = arcade.load_sound("images/alans_images/over.wav")

        arcade.set_background_color(arcade.csscolor.PALE_GOLDENROD)

    def setup(self):
        self.score = 0
        self.tom_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.jerry_list = arcade.SpriteList()

        # Create Tom
        image_source = "images/alans_images/tom_c.png"
        self.tom_sprite = arcade.Sprite(image_source, GameProperties.CHARACTER_SCALING)
        self.tom_sprite.center_x = 64
        self.tom_sprite.center_y = 128
        self.tom_list.append(self.tom_sprite)

        # Create Game env
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/alans_images/grass.png", GameProperties.TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/alans_images/box.png", GameProperties.TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create Jerries for Tom to catch
        for x in range(128, 1250, 256):
            jerry = arcade.Sprite("images/alans_images/jerry_c.png", GameProperties.JERRY_SCALING)
            jerry.center_x = x
            jerry.center_y = 96
            self.jerry_list.append(jerry)

        # Create arcade engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.tom_sprite, self.wall_list)

    @classmethod
    def gameOver(cls):
        '''Creates a classmethod for "Game over" Screen
        '''
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.BLACK_BEAN, 54)
        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.BLACK_BEAN, 24)

    def draw_game_over(self):
        AlansGame.gameOver()

    def draw_game(self):
        self.wall_list.draw()
        self.jerry_list.draw()
        self.tom_list.draw()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10,
                         arcade.csscolor.RED, 18)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == GameProperties.GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == GameProperties.GAME_OVER:
            self.setup()
            self.current_state = GameProperties.GAME_RUNNING

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.tom_sprite.change_y = GameProperties.TOM_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.tom_sprite.change_y = -GameProperties.TOM_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.tom_sprite.change_x = -GameProperties.TOM_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.tom_sprite.change_x = GameProperties.TOM_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.tom_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.tom_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.tom_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.tom_sprite.change_x = 0

    def on_update(self, delta_time):
        """Updates and checks to see if Tom catches any Jerries. Updates score
        """
        if self.current_state == GameProperties.GAME_RUNNING:
            self.physics_engine.update()
            # See if Tom catches any Jerries
            jerry_hit_list = arcade.check_for_collision_with_list(self.tom_sprite, self.jerry_list)
            for jerry in jerry_hit_list:
                jerry.remove_from_sprite_lists()
                arcade.play_sound(self.eat_jerry_sound)
                self.score += 1
                if self.score >= 4:
                    arcade.play_sound(self.jump_sound)
                    self.current_state = GameProperties.GAME_OVER


def main():
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    # Create AlansGame
    window = AlansGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
