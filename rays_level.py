import arcade
import math
import settings



#--------- currently updated to mark3---------
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

#------------------ Paste all classes here ----------------



class RayView(arcade.View):

#-------------- Paste all "my game code here" ----------------

 

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
