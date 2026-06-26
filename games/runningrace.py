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

# Force window focus on startup
try:
    canvas = screen.getcanvas()
    root = canvas.winfo_toplevel()
    root.focus_force()
except:
    pass

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

# Tap controls using Right Arrow or Space with cooldown to prevent holding cheats
last_tap_time = 0
game_over = False

def press_right():
    global last_tap_time, game_over
    if game_over:
        return
        
    current_time = time.time()
    # 80ms cooldown to block continuous key holding, but allowing fast mashing
    if current_time - last_tap_time > 0.08:
        try:
            user_turtle.forward(12)  # Moves forward 12 pixels per tap
            last_tap_time = current_time
        except:
            pass

# Register event handlers (supports both Right Arrow and Space bar for mashing!)
screen.listen()
screen.onkeypress(press_right, "Right")
screen.onkeypress(press_right, "space")

# Create a writer turtle for status announcements
writer = Turtle()
writer.hideturtle()
writer.penup()
writer.color("yellow")

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

# Frame-by-frame game loop using Turtle's ontimer
def game_loop():
    global game_over, waiting_for_input, action
    
    try:
        if game_over:
            return
            
        # Move AI opponents forward by random amount
        for opponent in [lol, t, fish]:
            # Default speed
            speed = randint(2, 5)
            
            # Rubber-banding logic:
            # If the player is ahead and close to winning (xcor > 50), the AI starts accelerating
            if user_turtle.xcor() > 50 and opponent.xcor() < user_turtle.xcor():
                speed += randint(3, 6)
                
            # Final stretch rubber band:
            # If the player is very close to the finish line (xcor > 180), the AI gets a massive boost
            # to overtake the player right before the end, creating the "about to win but lose" illusion.
            if user_turtle.xcor() > 180:
                speed += randint(7, 11)
                
            opponent.forward(speed)

        # Update visual state
        screen.update()

        # Check winning condition (Finish line is x = 280)
        if user_turtle.xcor() >= 280 or lol.xcor() >= 280 or t.xcor() >= 280 or fish.xcor() >= 280:
            game_over = True
            
            # Determine winner
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
            
            # Bind keys for restart/exit menu
            screen.listen()
            screen.onkeypress(handle_restart, "space")
            screen.onkeypress(handle_exit, "Escape")
            
            # Blocking loop for menu selection
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
                game_over = False
                
                # Rebind race controls
                screen.listen()
                screen.onkeypress(press_right, "Right")
                screen.onkeypress(press_right, "space")
                
                # Re-run the loop
                game_loop()
            else:
                screen.bye()
                return

        # Schedule next frame in 30ms (approx. 33 FPS)
        if not game_over:
            screen.ontimer(game_loop, 30)
            
    except Exception:
        # Gracefully exit if the Tkinter canvas or window is destroyed/closed
        pass

# Start the game loop
game_loop()
done()
