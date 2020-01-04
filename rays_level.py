import arcade
import math
import settings



#--------- currently updated to mark3---------
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

#------------------ Paste all classes here ----------------

#turret class

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
        super().__init__(image)
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.scale = 0.5
        self.activated = False 

#laser class
    
class Laser(arcade.Sprite):

    def __init__(self, image, turret):

        super().__init__(image)
        self.center_x = turret.center_x
        self.center_y = turret.center_y 
        self.angle = turret.angle 
        self.change_x = math.cos(math.radians(self.angle +90)) *5
        self.change_y = math.sin(math.radians(self.angle +90)) *5
        self.texture = arcade.make_soft_square_texture(30, arcade.color.ORANGE, outer_alpha=255)
        self.width = 5

class Heart(arcade.Sprite):

    def __init__(self, image, heart_num):

        super().__init__(image)
        self.scale = 1
        self.top = HEIGHT - 20
        self.left = heart_num*100 - 50

class Coin(arcade.Sprite):

    def __init__(self, image, center_x, center_y, collection_bonus):
        super().__init__(image)
        self.scale = .1
        self.center_x = center_x
        self.center_y = center_y
        self.collection_bonus = collection_bonus
        self.time_collected = None





        
#player class

class Player(arcade.Sprite):

    def __init__(self, image):
        """ Set up the player """

        # Call the parent init
        super().__init__(image)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

        self.move_speed = 10
        self.turn_speed = 5
        self.scale = .25

        self.center_x = 100
        self.center_y = 900

        self.hearts = 5



    
    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        #keep player in screen

        if self.center_x < self.width/2:
            self.center_x = self.width/2
        if self.center_x > WIDTH - self.width/2:
            self.center_x = WIDTH - self.width/2
        if self.center_y < self.width/2:
            self.center_y = self.width/2
        if self.center_y > HEIGHT - 100 - self.width/2:
            self.center_y = HEIGHT - 100 - self.width/2

class RayView(arcade.View):

#-------------- Paste all "my game code here" ----------------

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.player = Player("rokit_ship.png")

        #set up turrets

        self.turret_list = arcade.SpriteList()
        turret1 = Turret("turret.png",  700, 900, 180)
        turret2 = Turret("turret.png",  200, 800, 270)
        turret3 = Turret("turret.png",  500, 600, 180)
        turret4 = Turret("turret.png",  1800, 100, 0)
        turret5 = Turret("turret.png",  1600, 500, 90)
        turret6 = Turret("turret.png",  200, 100, 0)
        turret7 = Turret("turret.png",  1300, 800, 180)
        turret8 = Turret("turret.png",  800, 400, 270)
        self.turret_list.append(turret1)
        self.turret_list.append(turret2)
        self.turret_list.append(turret3)
        self.turret_list.append(turret4)
        self.turret_list.append(turret5)
        self.turret_list.append(turret6)
        self.turret_list.append(turret7)
        self.turret_list.append(turret8)

        #activate initial turrets

        self.turret_list[0].activated = True
        self.turret_list[1].activated = True
        self.turret_list[2].activated = True
        self.turret_list[3].activated = True
        self.turret_list[4].activated = True
        self.turret_list[5].activated = True
        self.turret_list[6].activated = True
        self.turret_list[7].activated = True
        



        self.lasers = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.recur_list = []

        heart1 = Heart("heart.jpg", 1)
        heart2 = Heart("heart.jpg", 2)
        heart3 = Heart("heart.jpg", 3)
        heart4 = Heart("heart.jpg", 4)
        heart5 = Heart("heart.jpg", 5)
        
        self.heart_list.append(heart1)
        self.heart_list.append(heart2)
        self.heart_list.append(heart3)
        self.heart_list.append(heart4)
        self.heart_list.append(heart5)

        
        coin = Coin("coin.png", 900, 300, 45)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("coin.png", 450, 200, 10)
        self.coin_list.append(coin)
        self.recur_list.append(coin)
        
        coin = Coin("coin.png", 200, 700, 60)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("coin.png", 1300, 500, 75)
        self.coin_list.append(coin)
        self.recur_list.append(coin)

        coin = Coin("coin.png", 1600, 700, 55)
        self.coin_list.append(coin)
        self.recur_list.append(coin)
        

        self.frame_count = 0
        self.score = 0
        self.time = 300
        
    def count_score(self,n):
        if len(n) == 0:
            return 0
        elif n[0].time_collected != None:
            return n[0].time_collected*n[0].collection_bonus + self.count_score(n[1:])
        else:
            return 0 + self.count_score(n[1:])
        

        

    
    #the draw

    def on_draw(self):
        arcade.start_render()  # keep as first line

        # Draw everything below here.
        self.player.draw()
        self.lasers.draw()
        self.turret_list.draw()
        self.heart_list.draw()
        self.coin_list.draw()


        output = f"Score: {self.score}"
        arcade.draw_text(output, 1500, 1000, arcade.color.WHITE, 50)
        
        
    #the update 

    def update(self, delta_time):

       
        
        self.frame_count += 1
        

        if self.score > 9999999:
            self.score = 9999999
        self.player.update()
        self.turret_list.update()
        self.lasers.update()
        self.coin_list.update()
        self.score = self.count_score(self.recur_list)
        

        

        #shoot laser every this many frames


        if self.frame_count %90 == 0:
            for turret in self.turret_list:
                if turret.activated == True:
                    laser = Laser("rokit_ship.png", turret)
                    self.lasers.append(laser)

        #spinny turret

        if self.frame_count %3 == 0:
            self.turret_list[7].angle += 1
                

        #kill laser when it leaves screen to save memory

        for laser in self.lasers:
            if laser.top < 0:
                laser.remove_from_sprite_lists()
            elif laser.bottom > HEIGHT:
                laser.remove_from_sprite_lists()
            if laser.right < 0:
                laser.remove_from_sprite_lists()
            elif laser.left > WIDTH:
                laser.remove_from_sprite_lists()


        # check if hit laser or turret

        for laser in self.lasers:
            hit = arcade.check_for_collision(laser, self.player)
            if hit == True:
                laser.remove_from_sprite_lists()
                print("oof")
                self.player.center_x = 0
                self.player.center_y = 900
                self.player.hearts -= 1
                self.heart_list.pop()
                print(self.player.hearts)

        if self.player.collides_with_list(self.turret_list):
            self.player.center_x = 0
            self.player.center_y = 900
            self.player.hearts -= 1
            self.heart_list.pop()
            print(self.player.hearts)

        for coin in self.coin_list:
            hit = arcade.check_for_collision(coin, self.player)
            if hit == True:
                coin.remove_from_sprite_lists()
                coin.time_collected = 300-self.frame_count//60

        if self.player.hearts == 0:
           self.director.next_view() 



        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        #moving
        if key == arcade.key.UP:
            self.player.speed = self.player.move_speed
        elif key == arcade.key.DOWN:
            self.player.speed = -self.player.move_speed

        #turning
        elif key == arcade.key.LEFT:
            self.player.change_angle = self.player.turn_speed
        elif key == arcade.key.RIGHT:
            self.player.change_angle = -self.player.turn_speed

        elif key == arcade.key.KEY_0:
           self.director.next_view()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_angle = 0
  


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
    my_view = RayView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
