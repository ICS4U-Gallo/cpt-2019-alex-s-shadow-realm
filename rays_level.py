import arcade
import math
import settings
import json



#--------- currently updated to mark3---------
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
background = arcade.load_texture("images/back.jpg")

#------------------ Paste all classes here ----------------

def count_score(num_list):
    if len(num_list) == 0:
        return 0
    elif num_list[0].time_collected is not None:
        return (num_list[0].time_collected*num_list[0].collection_bonus
                + count_score(num_list[1:]))
    else:
        return 0 + count_score(num_list[1:])


def check_name(name):
    with open("scores.json", "r") as f:
        score_dictionary = json.load(f)

    name_list = []
    for key in score_dictionary.keys():
        name_list.append(key)

    if name not in name_list:
        return True
    else:
        return False


def binary_search(lista, target):
    start = 0
    end = len(lista) - 1
    while start <= end:
        mid = math.ceil((start + end) // 2)
        if lista[mid] == target:
            return mid
        elif lista[mid] > target:
            end = mid - 1
        elif lista[mid] < target:
            start = mid + 1
    return -1


def merge_sort(numbers):
    if len(numbers) == 1:
        return numbers
    midpoint = len(numbers)//2
    left_side = merge_sort(numbers[:midpoint])
    right_side = merge_sort(numbers[midpoint:])
    sorted_list = []
    left_marker = 0
    right_marker = 0
    while left_marker < len(left_side) and right_marker < len(right_side):

        if left_side[left_marker] < right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1

        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1

    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1

    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1

    return sorted_list


def save_score(name=None, score=None):
    with open("scores.json", "r") as f:
        score_dictionary = json.load(f)

    name_list = []
    for key in score_dictionary.keys():
        name_list.append(key)

    score_dictionary[name] = score

    with open("scores.json", "w") as f:
        json.dump(score_dictionary, f)

    score_list = []
    for value in score_dictionary.values():
        score_list.append(value)
    score_list = merge_sort(score_list)

    return [len(score_list)-(binary_search(score_list, score)), score, name]


def find_highscores():
    with open("scores.json", "r") as f:
        dictionary = json.load(f)
        data = []
    for i in range(3):
        high_value = 0
        high_key = None
        for key, value in dictionary.items():
            if value >= high_value:
                high_value = value
                high_key = key
        data.append(high_key)
        data.append(high_value)
        del dictionary[high_key]
    return data


# classes

class Player(arcade.Sprite):

    def __init__(self, image):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale=0.25)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0
        self.move_speed = 7.5
        self.turn_speed = 5
        self.center_x = 35
        self.center_y = 575
        self.angle = 270

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        # keep player in screen
        if self.center_x < self.width/2:
            self.center_x = self.width/2
        if self.center_x > WIDTH - self.width/2:
            self.center_x = WIDTH - self.width/2
        if self.center_y < self.width/2:
            self.center_y = self.width/2
        if self.center_y > HEIGHT - 100 - self.width/2:
            self.center_y = HEIGHT - 100 - self.width/2


class Turret(arcade.Sprite):
    '''Turret class
    Attributes:
        image (image file): the name of the food
        center_x (int): x pos of turret
        center_y (int): y pos of turret
        angle (int): angle of turret
        '''

    def __init__(self, image, center_x, center_y, angle):
        """Create a Turret object.
        Args:
            image: file path of image
            center_x: x pos of turret
            center_y: y pos of turret
            angle: angle of turret
        """
        # Call the parent init
        super().__init__(image, scale=0.4)
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.activated = False


class SpinnyTurret(Turret):
    def __init__(self, image, center_x, center_y, angle):
        super().__init__(image, center_x, center_y, angle)
        self.turn_speed = 1


class SmartTurret(Turret):
    def __init__(self, image, center_x, center_y, angle):
        super().__init__(image, center_x, center_y, angle)
        self.angle = 90

    def update(self, target_x, target_y):
        # Convert angle in degrees to radians.
        self.angle = (-90 + math.degrees(math.atan2(target_y - self.center_y,
                      target_x - self.center_x)))


class Laser(arcade.Sprite):

    def __init__(self, turret):

        super().__init__()
        self.center_x = turret.center_x
        self.center_y = turret.center_y
        self.angle = turret.angle
        self.speed = 5
        self.change_x = math.cos(math.radians(self.angle + 90)) * self.speed
        self.change_y = math.sin(math.radians(self.angle + 90)) * self.speed
        self.texture = arcade.make_soft_square_texture(30,
                                                       arcade.color.ORANGE,
                                                       outer_alpha=255)
        self.width = 5


class Barrier(arcade.Sprite):
    def __init__(self, center_x, center_y, angle):
        super().__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.texture = arcade.make_soft_square_texture(310, arcade.color.RED,
                                                       outer_alpha=255)
        self.width = 10


class Heart(arcade.Sprite):

    def __init__(self, image, heart_num):

        super().__init__(image)
        self.scale = .75
        self.top = HEIGHT - 20
        self.left = heart_num*75 - 50


class Coin(arcade.Sprite):

    def __init__(self, image, center_x, center_y):
        super().__init__(image, scale=0.05)
        self.center_x = center_x
        self.center_y = center_y
        self.collection_bonus = 50
        self.time_collected = None


class Diamond(Coin):
    def __init__(self, image, center_x, center_y):
        super().__init__(image, center_x, center_y)
        self.scale = 0.25
        self.collection_bonus = 500
        self.time_collected = None





#-------------- Paste all "my game code here" ----------------

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        self.player = Player("images/rokit_ship.png")
        self.barrier_on = True
        self.frame_count = 0
        self.score = 0
        self.turret_list = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.long_lasers = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.barrier_turrets = arcade.SpriteList()
        self.barriers = arcade.SpriteList()
        self.recur_list = []
        self.reset_message = False
        self.show_time = 0

        # set up turrets

        turret = Turret("images/turret.png",  1200, 600, 180)
        self.turret_list.append(turret)
        turret = Turret("images/turret.png",  450, 100, 0)
        self.turret_list.append(turret)
        turret = Turret("images/turret.png",  1100, 125, 90)
        self.turret_list.append(turret)
        turret = Turret("images/turret.png",  1300, 250, 90)
        self.turret_list.append(turret)
        turret = Turret("images/turret.png",  900, 35, 0)
        self.turret_list.append(turret)
        turret = SpinnyTurret("images/turret.png",  800, 450, 90)
        self.turret_list.append(turret)
        turret = SpinnyTurret("images/turret.png",  1000, 600, 269)
        self.turret_list.append(turret)
        turret = SpinnyTurret("images/turret.png",  600, 600, 91)
        self.turret_list.append(turret)

        self.smart_turret = SmartTurret("images/turret.png",  25, 25, 300)

        barrier_turret = Turret("images/turret.png",  39, 300, 270)
        self.barrier_turrets.append(barrier_turret)
        barrier_turret = Turret("images/turret.png",  300, 39, 0)
        self.barrier_turrets.append(barrier_turret)

        # set up hearts

        heart = Heart("images/heart.jpg", 1)
        self.heart_list.append(heart)
        heart = Heart("images/heart.jpg", 2)
        self.heart_list.append(heart)
        heart = Heart("images/heart.jpg", 3)
        self.heart_list.append(heart)
        heart = Heart("images/heart.jpg", 4)
        self.heart_list.append(heart)
        heart = Heart("images/heart.jpg", 5)
        self.heart_list.append(heart)

        # set up coins

        coin = Coin("images/coin.png", 800, 550)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("images/coin.png", 380, 50)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("images/coin.png", 950, 50)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("images/coin.png", 1250, 500)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("images/coin.png", 650, 350)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Diamond("images/dimond.png", 100, 100)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        # set up barrier

        barrier = Barrier(300, 150, 0)
        self.barriers.append(barrier)
        barrier = Barrier(150, 300, 270)
        self.barriers.append(barrier)

        # activate initial turrets

        self.turret_list[0].activated = True
        self.turret_list[1].activated = True
        self.turret_list[2].activated = True
        self.turret_list[3].activated = True
        self.turret_list[4].activated = True

    # class functions

    def countdown(self):
        if self.frame_count < 90:
            return str(math.ceil((90-self.frame_count)/30))
        else:
            return "GO"

    # the draw

    def on_draw(self):
        arcade.start_render()  # keep as first line
        arcade.draw_texture_rectangle(WIDTH//2, HEIGHT//2, WIDTH, HEIGHT,
                                      background)
        arcade.draw_xywh_rectangle_textured(1280, 0, 70, 50,
                                            arcade.load_texture
                                            ("images/finish box.jpg"))
        self.barriers.draw()
        self.lasers.draw()
        self.barrier_turrets.draw()
        self.turret_list.draw()
        self.smart_turret.draw()
        self.player.draw()
        self.heart_list.draw()
        self.coin_list.draw()

        arcade.draw_text(f"SCORE: {self.score}", 1050, 650, arcade.color.WHITE,
                         30)

        if self.frame_count < 120:
            arcade.draw_text(self.countdown(), WIDTH//2, HEIGHT//2,
                             arcade.color.WHITE, 500,
                             align="center", anchor_x="center",
                             anchor_y="center")

        if self.reset_message is True:
            arcade.draw_text("SCORE BOARD HAS\nBEEN RESET", WIDTH//2, 500,
                             arcade.color.RED, 100, align="center",
                             anchor_x="center", anchor_y="center")

    # the update

    def update(self, delta_time):

        self.frame_count += 1

        self.player.update()
        self.turret_list.update()
        self.lasers.update()
        self.coin_list.update()
        self.smart_turret.update(self.player.center_x, self.player.center_y)

        # spinny turret

        if self.frame_count % 3 == 0:
            for turret in self.turret_list[5:8]:
                turret.angle -= turret.turn_speed
                if turret.angle == 270 or turret.angle == 90:
                    turret.turn_speed = -turret.turn_speed

        # shoot lasers

        if self.frame_count % 120 == 0:
            for turret in self.turret_list:
                if turret.activated is True:
                    laser = Laser(turret)
                    self.lasers.append(laser)

        if self.frame_count % 40 == 0:
            if self.smart_turret.activated is True:
                laser = Laser(self.smart_turret)
                self.lasers.append(laser)

        if self.frame_count % 20 == 0:
            if len(self.coin_list) == 0:
                laser = Laser(self.smart_turret)
                self.lasers.append(laser)

        # check if laser hit

        for laser in self.lasers:
            hit = arcade.check_for_collision(laser, self.player)
            if hit is True:
                laser.remove_from_sprite_lists()

                self.player.center_x = 35
                self.player.center_y = 575
                self.player.angle = 270
                self.heart_list[-1].remove_from_sprite_lists()
                print(len(self.heart_list))

        if (self.player.collides_with_list(self.turret_list)
                or self.player.collides_with_list(self.barrier_turrets)
                or self.player.collides_with_list(self.barriers)):

            self.player.center_x = 35
            self.player.center_y = 575
            self.player.angle = 270
            self.heart_list[-1].remove_from_sprite_lists()
            print(len(self.heart_list))

        # kill laser when it leaves screen to save memory

        for laser in self.lasers:
            if laser.top < 0:
                laser.remove_from_sprite_lists()
            elif laser.bottom > HEIGHT:
                laser.remove_from_sprite_lists()
            if laser.right < 0:
                laser.remove_from_sprite_lists()
            elif laser.left > WIDTH:
                laser.remove_from_sprite_lists()

        # collect coins

        for coin in self.coin_list:
            hit = arcade.check_for_collision(coin, self.player)
            if hit is True:
                coin.remove_from_sprite_lists()
                coin.time_collected = 300-self.frame_count//60

        self.score = count_score(self.recur_list)

        if self.score > 9999999:
            self.score = 9999999

        # increase difficulty

        if len(self.coin_list) < 6:
            pass

        if len(self.coin_list) < 5:
            self.turret_list[5].activated = True

        if len(self.coin_list) < 3:
            self.turret_list[6].activated = True
            self.turret_list[7].activated = True

        # off barrier

        if len(self.coin_list) == 1:
            for barrier in self.barriers:
                barrier.remove_from_sprite_lists()
            self.smart_turret.activated = True

        # finish game

        if self.player.center_x > 1300 and self.player.center_y < 50:
            finish_view = FinishView()
            self.score += 100*(300-self.frame_count//60)
            finish_view.score = self.score
            finish_view.win = True
            finish_view.director = self.director
            self.window.show_view(finish_view)

        # die

        if len(self.heart_list) == 0:
            finish_view = FinishView()
            finish_view.score = self.score
            finish_view.win = False
            finish_view.director = self.director
            self.window.show_view(finish_view)

        if self.reset_message is True:
            self.show_time += 1
        if self.show_time > 60:
            self.reset_message = False
            self.show_time = 0

    # key functions

    def on_key_press(self, key, modifiers):

        # moving
        if key == arcade.key.UP and self.frame_count > 120:
            self.player.speed = self.player.move_speed
        elif key == arcade.key.DOWN and self.frame_count > 120:
            self.player.speed = -self.player.move_speed

        # turning
        elif key == arcade.key.LEFT:
            self.player.change_angle = self.player.turn_speed
        elif key == arcade.key.RIGHT:
            self.player.change_angle = -self.player.turn_speed

        # cheat codes in case you suck

        elif key == arcade.key.KEY_1:
            finish_view = FinishView()
            self.score = 9999999
            finish_view.score = self.score
            finish_view.win = True
            finish_view.director = self.director
            self.window.show_view(finish_view)

        elif key == arcade.key.KEY_2:
            self.coin_list[0].remove_from_sprite_lists()
            self.coin_list[0].time_collected = 300-self.frame_count//60

        elif key == arcade.key.KEY_3:
            with open("scores.json", "r") as f:
                score_dictionary = json.load(f)
            score_dictionary = {" ": 0, "  ": 0, "   ": 0}
            with open("scores.json", "w") as f:
                json.dump(score_dictionary, f)
            self.reset_message = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_angle = 0


class FinishView(arcade.View):

    def on_draw(self):
        arcade.start_render()

        # print win/lose screen
        if self.win is False:
            arcade.set_background_color(arcade.color.RED)
            arcade.draw_text("YOU LOSE", WIDTH//2, 550, arcade.color.BLACK,
                             100, align="center", anchor_x="center",
                             anchor_y="center")
        elif self.win is True:
            arcade.set_background_color(arcade.color.GREEN)
            arcade.draw_text("YOU WIN", WIDTH//2, 550, arcade.color.BLACK, 100,
                             align="center", anchor_x="center",
                             anchor_y="center")

        # buttons

        arcade.draw_text(f"YOUR SCORE WAS: {self.score}", WIDTH//2, 450,
                         arcade.color.BLACK, 50, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_rectangle_filled(WIDTH//2, 300, 300, 100,
                                     arcade.color.BLACK)
        arcade.draw_rectangle_filled(WIDTH//2, 100, 300, 100,
                                     arcade.color.BLACK)
        arcade.draw_text("CLICK TO TRY  \n AGAIN", WIDTH//2, 300,
                         arcade.color.WHITE, 25, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("CLICK TO SUBMIT  \n SCORE", WIDTH//2, 100,
                         arcade.color.WHITE, 25, align="center",
                         anchor_x="center", anchor_y="center")

    # click buttons

    def on_mouse_press(self, _x, _y, _button, _modifiers):

        if WIDTH//2 - 150 < _x < WIDTH//2 + 150 and 250 < _y < 350:
            game_view = GameView()
            self.window.show_view(game_view)

        elif WIDTH//2 - 150 < _x < WIDTH//2 + 150 and 50 < _y < 150:
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
        arcade.draw_texture_rectangle(WIDTH//2, HEIGHT//2, WIDTH, HEIGHT,
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
    my_view = GameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
