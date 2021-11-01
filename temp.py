import turtle
import time
from pygame import mixer


mixer.init()
mixer.music.load('back.wav')
mixer.music.play()

while True:
    turtle.Screen().bgcolor("red")
    time.sleep(0.3)
    turtle.Screen().bgcolor("blue")
    time.sleep(0.3)
    turtle.Screen().bgcolor("green")
    time.sleep(0.3)
