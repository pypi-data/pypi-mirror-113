import os, random
from pynput import keyboard
from threading import Thread
from numpy import *
from processing_py import *


class ProcessingApp:
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
    global sketch
    if key == keyboard.Key.esc:
        print("Program Ended")
        os._exit(1)


def Run(app):
    def Main_Thread() -> None:
        """Thread Contaning App Logic"""
        global sketch
        sketch = app()
        sketch.setup()
        while sketch.running:
            sketch.draw()
            sketch.app.redraw()
            sketch.frameCount += 1
        return

    def Input_Thread() -> None:
        """Thread Handling Input"""
        while sketch.running:
            with keyboard.Listener(on_press=sketch.keyPressed, on_release=sketch.keyReleased) as listener:
                listener.join()
        return

    def Exit_Thread() -> None:
        with keyboard.Listener(on_release=Exit) as ExitListener:
            ExitListener.join()
        
    threads:list = []
    threads.extend([Thread(target=Main_Thread),
                    Thread(target=Input_Thread),
                    Thread(target=Exit_Thread)])

    for thread in threads:
        thread.start()

def Key(char:char) -> keyboard.KeyCode:
    return keyboard.KeyCode.from_char(char)


class Vector2:
    x:float
    y:float

    def __init__(self, x:float=0, y:float=0):
        self.x = x ; self.y = y

    def __str__(self):
        return f"{{x: {str(self.x)}, y: {str(self.y)}}}"

    def add(self, other):
        """Adding the Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x += other; self.y += other
        elif type(other) == Vector2:
            self.x += other.x; self.y += other.y
        else:
            print(f"Cant add {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def sub(self, other):
        """Subtracting the Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x -= other; self.y -= other
        elif type(other) == Vector2:
            self.x -= other.x; self.y -= other.y
        else:
            print(f"Cant subtract {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def mul(self, other):
        """Multiplying Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x *= other; self.y *= other
        elif type(other) == Vector2:
            self.x *= other.x; self.y *= other.y
        else:
            print(f"Cant multiply {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError
        return self   

    def div(self, other):
        """Dividing Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x /= other; self.y /= other
        elif type(other) == Vector2:
            self.x /= other.x; self.y /= other.y
        else:
            print(f"Cant divide {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self

    def random(self):
        return Vector2(random.random(), random.random())

    def magnitude(self) -> float:
        return float(sqrt(self.x**2 + self.y**2))

    def normalize(self, vector=0):
        """u = v / |v|"""
        if vector != 0:
            return vector.div(vector.magnitude())
        else:
            return self.div(self.magnitude())

class Vector3:
    x:float
    y:float
    z:float

    def __init__(self, x:float=0, y:float=0, z:float=0):
        self.x = x ; self.y = y ; self.z = z
        
    def __str__(self):
        return f"{{x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)}}}"

    def add(self, other):
        """Adding the Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x += other; self.y += other; self.z += other
        elif type(other) == Vector3:
            self.x += other.x; self.y += other.y; self.z += other.z
        else:
            print(f"Cant add {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def sub(self, other):
        """Subtracting the Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x -= other; self.y -= other; self.z -= other
        elif type(other) == Vector3:
            self.x -= other.x; self.y -= other.y; self.z -= other.z
        else:
            print(f"Cant subtract {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def mul(self, other):
        """Multiplying Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x *= other; self.y *= other; self.z *= other
        elif type(other) == Vector3:
            self.x *= other.x; self.y *= other.y; self.z *= other.z
        else:
            print(f"Cant multiply {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def div(self, other):
        """Dividing Vector with a number or other Vector"""
        if type(other) == int or type(other) == float:
            self.x /= other; self.y /= other; self.z /= other
        elif type(other) == Vector3:
            self.x /= other.x; self.y /= other.y; self.z /= other.z
        else:
            print(f"Cant divide {self} of type {type(self)} and {other} of type {type(other)}")
            raise TypeError   
        return self   

    def random(self):
        return Vector3(random.random(), random.random(), random.random())

    def magnitude(self) -> float:
        return float(sqrt(self.x**2 + self.y**2 + self.z**2))

    def normalize(self, vector=0):
        """u = v / |v|"""
        if vector != 0:
            return vector.div(vector.magnitude())
        else:
            return self.div(self.magnitude())
