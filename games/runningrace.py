import time
from turtle import *
from random import randint
import os

# Set working directory to this script's directory (games/)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the turtle screen
screen = Screen()
screen.bgpic("../images/we.gif")
screen.title("Aqua-mania Sprint - Running Game")
screen.setup(width=800, height=600)

# Add shapes from ../images/
screen.addshape("../images/swim.gif")
screen.addshape("../images/lol.gif")
screen.addshape("../images/t.gif")
screen.addshape("../images/fish.gif")

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
ada.shape("../images/swim.gif")
ada.penup()
ada.goto(-240, 200)

lol = Turtle()
lol.shape("../images/lol.gif")
lol.penup()
lol.goto(-240, 50)

t = Turtle()
t.shape("../images/t.gif")
t.penup()
t.goto(-240, -100)

fish = Turtle()
fish.shape("../images/fish.gif")
fish.penup()
fish.goto(-240, -200)

user_turtle = ada

# Tracking last tapped key
last_key_pressed = None

def press_right():
    global last_key_pressed
    # Enforce alternate tapping (must press Left before pressing Right again)
    if last_key_pressed != "Right":
        user_turtle.forward(randint(6, 10))
        last_key_pressed = "Right"

def press_left():
    global last_key_pressed
    # Enforce alternate tapping (must press Right before pressing Left again)
    if last_key_pressed != "Left":
        user_turtle.forward(randint(6, 10))
        last_key_pressed = "Left"

# Register event handlers
screen.listen()
screen.onkeypress(press_right, "Right")
screen.onkeypress(press_left, "Left")

# Create a writer turtle for status announcements
writer = Turtle()
writer.hideturtle()
writer.penup()
writer.color("yellow")

game_over = False

# Define globals for menu interaction
waiting_for_input = True
action = None

def handle_restart():
    global waiting_for_input, action
    action = "restart"
    waiting_for_input = False
    
def handle_exit():
    global waiting_for_input, action
    action = "exit"
    waiting_for_input = False

# Turn off tracer for manual updating (prevents lag/flicker)
screen.tracer(0)

# Game loop
while not game_over:
    # Move AI opponents forward by random amount
    lol.forward(randint(3, 6))
    t.forward(randint(3, 6))
    fish.forward(randint(3, 6))

    # Update visual state
    screen.update()

    # Check winning condition (Finish line is x = 280)
    if user_turtle.xcor() >= 280 or lol.xcor() >= 280 or t.xcor() >= 280 or fish.xcor() >= 280:
        if user_turtle.xcor() >= 280:
            winner_text = "YOU WON!"
        else:
            winner_text = "PC WON!"
            
        # Draw winner banners and prompts
        writer.goto(0, 0)
        writer.write(winner_text, align="center", font=("Arial", 36, "bold"))
        writer.goto(0, -50)
        writer.write("Press SPACE to Restart or ESC to Exit", align="center", font=("Arial", 18, "bold"))
        screen.update()
        
        # Reset input loop states
        waiting_for_input = True
        action = None
        
        screen.listen()
        screen.onkeypress(handle_restart, "space")
        screen.onkeypress(handle_exit, "Escape")
        
        while waiting_for_input:
            screen.update()
            time.sleep(0.05)
            
        if action == "restart":
            # Reset swimmer coordinates
            ada.goto(-240, 200)
            lol.goto(-240, 50)
            t.goto(-240, -100)
            fish.goto(-240, -200)
            
            # Reset tracking variables
            writer.clear()
            last_key_pressed = None
            
            # Rebind keys
            screen.listen()
            screen.onkeypress(press_right, "Right")
            screen.onkeypress(press_left, "Left")
        else:
            screen.bye()
            break

    # Frame delay to reduce CPU consumption and keep responsiveness
    time.sleep(0.03)

# Safely close turtle screen
try:
    screen.bye()
except:
    pass
