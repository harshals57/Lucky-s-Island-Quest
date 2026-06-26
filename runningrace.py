import time
from turtle import *
from random import randint
import os

# Set working directory to script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the turtle screen
screen = Screen()
screen.bgpic("we.gif")
screen.title("Aqua-mania Sprint - Running Game")
screen.setup(width=800, height=600)

# Add shapes
screen.addshape("swim.gif")
screen.addshape("lol.gif")
screen.addshape("t.gif")
screen.addshape("fish.gif")

# Draw the finish line
tur = Turtle()
tur.hideturtle()
tur.width(10)
tur.shape("arrow")
tur.color("red")
tur.penup()
tur.goto(280, 400)
tur.pendown()
tur.goto(280, -400)

# Create the swimmers/runners
ada = Turtle()
ada.shape("swim.gif")
ada.penup()
ada.goto(-240, 200)

lol = Turtle()
lol.shape("lol.gif")
lol.penup()
lol.goto(-240, 50)

t = Turtle()
t.shape("t.gif")
t.penup()
t.goto(-240, -100)

fish = Turtle()
fish.shape("fish.gif")
fish.penup()
fish.goto(-240, -200)

user_turtle = ada

# Tracking key states and last tapped key
keys_held = {"Right": False, "Left": False}
last_key_pressed = None

def press_right():
    global last_key_pressed
    # Only register on initial press (ignores OS auto-repeat)
    if not keys_held["Right"]:
        keys_held["Right"] = True
        # Enforce alternate tapping (must tap Left before tapping Right again)
        if last_key_pressed != "Right":
            user_turtle.forward(randint(5, 9))
            last_key_pressed = "Right"

def release_right():
    keys_held["Right"] = False

def press_left():
    global last_key_pressed
    # Only register on initial press (ignores OS auto-repeat)
    if not keys_held["Left"]:
        keys_held["Left"] = True
        # Enforce alternate tapping (must tap Right before tapping Left again)
        if last_key_pressed != "Left":
            user_turtle.forward(randint(5, 9))
            last_key_pressed = "Left"

def release_left():
    keys_held["Left"] = False

# Register event handlers
screen.listen()
screen.onkeypress(press_right, "Right")
screen.onkeyrelease(release_right, "Right")
screen.onkeypress(press_left, "Left")
screen.onkeyrelease(release_left, "Left")

# Create a writer turtle for status announcements
writer = Turtle()
writer.hideturtle()
writer.penup()
writer.color("yellow")

game_over = False

# Turn off tracer for manual updating (prevents lag/flicker)
screen.tracer(0)

# Game loop
while not game_over:
    # Move AI opponents forward by random amount (significantly boosted speed!)
    lol.forward(randint(3, 6))
    t.forward(randint(3, 6))
    fish.forward(randint(3, 6))

    # Update visual state
    screen.update()

    # Check winning condition (Finish line is x = 280)
    if user_turtle.xcor() >= 280:
        writer.goto(0, 0)
        writer.write("YOU WON!", align="center", font=("Arial", 36, "bold"))
        screen.update()
        game_over = True
        time.sleep(2)
    elif lol.xcor() >= 280 or t.xcor() >= 280 or fish.xcor() >= 280:
        writer.goto(0, 0)
        writer.write("PC WON!", align="center", font=("Arial", 36, "bold"))
        screen.update()
        game_over = True
        time.sleep(2)

    # Frame delay to reduce CPU consumption and keep responsiveness
    time.sleep(0.03)

# Safely close turtle screen
screen.bye()
