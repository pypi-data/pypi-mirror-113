import os, random
from pynput import keyboard
from threading import Thread
from numpy import *
from processing_py import *

"""
HOW TO USE:
1.  Create a file that has a class with the name of your choosing.

2.  Inside that class add two functions setup() and draw().
    The code within the setup function runs only once at at the start of the program.
    The code within the draw function runs every frame until exited.

3.  in the setup function for example, you can add something like "app = App(400, 400)" 
    to create a canvas object which has the specified width and height dimensions.

4.  There are many functions and variables that can be called as part of the App class.
    For example, code such as "app.background(255)" which will set the background to white.
    (Have a look at https://processing.org/reference for more information about the functions and variables)

5. Finally after your app class call the function Run(x) with x being the name of your class.
"""

class ProcessingApp:
    """Inheritance Class for the processing App class"""
    app: App
    running: bool = True
    frameCount: int = 0

    def setup(self) -> None:
        self.app = App(800, 600)

    def draw(self) -> None:
        self.app.background(20)

    def keyPressed(self, key):
        pass

    def keyReleased(self, key):
        pass



def Exit(key) -> None:
    """Exit Function."""
    global sketch
    if key == keyboard.Key.esc:
        print("Program Ended")
        os._exit(1)


def Run(app):
    """Main function setting up the threads to run the program."""
    def Main_Thread() -> None:
        """Thread Contaning App Logic."""
        global sketch
        sketch = app()
        sketch.setup()
        while sketch.running:
            sketch.draw()
            sketch.app.redraw()
            sketch.frameCount += 1
        return

    def Input_Thread() -> None:
        """Thread Handling Input."""
        while sketch.running:
            with keyboard.Listener(on_press=sketch.keyPressed, on_release=sketch.keyReleased) as listener:
                listener.join()
        return

    def Exit_Thread() -> None:
        """Thread Handling Exit."""
        with keyboard.Listener(on_release=Exit) as ExitListener:
            ExitListener.join()
        
    """Adding the threads to the list 'threads'."""
    threads:list = []
    threads.extend([Thread(target=Main_Thread),
                    Thread(target=Input_Thread),
                    Thread(target=Exit_Thread)])

    """Iterating through each thread and Calling the .start() method."""
    for thread in threads:
        thread.start()

def Key(char:char) -> keyboard.KeyCode:
    """Takes a character like 'a' for example and return the keyboard.KeyCode value for it."""
    return keyboard.KeyCode.from_char(char)


class Vector2:
    """Vector2 class stores 2 Dimensional Vector with an x and a y value. Contains basic Vector maths functions."""

    x:float
    y:float

    def __init__(self, x:float=0, y:float=0):
        self.x = x ; self.y = y

    def __str__(self):
        """Prints the Vector class in the format "{x: 0, y: 0}"."""
        return f"{{x: {str(self.x)}, y: {str(self.y)}}}"

    def add(self, other):
        """Adding the Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x += other; self.y += other
        elif type(other) == Vector2:
            self.x += other.x; self.y += other.y
        else:
            print(f"Cant add {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def sub(self, other):
        """Subtracting the Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x -= other; self.y -= other
        elif type(other) == Vector2:
            self.x -= other.x; self.y -= other.y
        else:
            print(f"Cant subtract {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def mul(self, other):
        """Multiplying Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x *= other; self.y *= other
        elif type(other) == Vector2:
            self.x *= other.x; self.y *= other.y
        else:
            print(f"Cant multiply {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError
        return self   

    def div(self, other):
        """Dividing Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x /= other; self.y /= other
        elif type(other) == Vector2:
            self.x /= other.x; self.y /= other.y
        else:
            print(f"Cant divide {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self

    def random(self):
        """Returns a Vector with random x and y values between 0 and 1."""
        return Vector2(random.random(), random.random())

    def magnitude(self) -> float:
        """Returns the magnitude the Vector p.s thanks PYthagoras."""
        return float(sqrt(self.x**2 + self.y**2))

    def normalize(self, vector=0):
        """ Normalizes the Vector with the equation: u = v / |v|."""
        if vector != 0:
            return vector.div(vector.magnitude())
        else:
            temp_vector = Vector2(self.x, self.y)
            return temp_vector.div(temp_vector.magnitude())

class Vector3:
    """Vector3 class stores 3 Dimensional Vector with an x, y and a z value. Contains basic Vector maths functions."""
    x:float
    y:float
    z:float

    def __init__(self, x:float=0, y:float=0, z:float=0):
        self.x = x ; self.y = y ; self.z = z
        
    def __str__(self):
        return f"{{x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)}}}"

    def add(self, other):
        """Adding the Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x += other; self.y += other; self.z += other
        elif type(other) == Vector3:
            self.x += other.x; self.y += other.y; self.z += other.z
        else:
            print(f"Cant add {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def sub(self, other):
        """Subtracting the Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x -= other; self.y -= other; self.z -= other
        elif type(other) == Vector3:
            self.x -= other.x; self.y -= other.y; self.z -= other.z
        else:
            print(f"Cant subtract {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def mul(self, other):
        """Multiplying Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x *= other; self.y *= other; self.z *= other
        elif type(other) == Vector3:
            self.x *= other.x; self.y *= other.y; self.z *= other.z
        else:
            print(f"Cant multiply {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def div(self, other):
        """Dividing Vector with a number or other Vector."""
        if type(other) == int or type(other) == float:
            self.x /= other; self.y /= other; self.z /= other
        elif type(other) == Vector3:
            self.x /= other.x; self.y /= other.y; self.z /= other.z
        else:
            print(f"Cant divide {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def random(self):
        """Returns a Vector with random x, y and z values between 0 and 1."""
        return Vector3(random.random(), random.random(), random.random())

    def magnitude(self) -> float:
        """Returns the magnitude the Vector p.s thanks PYthagoras."""
        return float(sqrt(self.x**2 + self.y**2 + self.z**2))

    def normalize(self, vector=0):
        """ Normalizes the Vector with the equation: u = v / |v|."""
        if vector != 0:
            return vector.div(vector.magnitude())
        else:
            temp_vector = Vector2(self.x, self.y, self.z)
            return temp_vector.div(temp_vector.magnitude())
