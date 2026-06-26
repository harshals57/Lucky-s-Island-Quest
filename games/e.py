import turtle
import time
import random
import os

# Set working directory to this script's directory (games/)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def snake():
    delay = 0.1
    score = 0
    high_score = 0

    # Creating a window screen
    wn = turtle.Screen()
    wn.title("Slither Runner - Eat it all you can!")
    wn.bgcolor("green")
    wn.setup(width=600, height=600)
    wn.tracer(0)

    # Register "lucky.gif" shape from ../images/
    wn.addshape("../images/lucky.gif")

    # Head of the snake
    head = turtle.Turtle()
    head.shape("../images/lucky.gif")  # Use the registered shape
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "Stop"

    # Food in the game
    food = turtle.Turtle()
    colors = random.choice(['red'])
    shapes = random.choice(['triangle'])
    food.speed(0)
    food.shape(shapes)
    food.color(colors)
    food.penup()
    food.goto(0, 100)

    # Score pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 250)
    pen.write("Score : 0 High Score : 0", align="center", font=("candara", 24, "bold"))

    # Assigning key directions
    def group():
        if head.direction != "down":
            head.direction = "up"

    def godown():
        if head.direction != "up":
            head.direction = "down"

    def goleft():
        if head.direction != "right":
            head.direction = "left"

    def goright():
        if head.direction != "left":
            head.direction = "right"

    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)
        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)
        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)
        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)

    wn.listen()
    wn.onkeypress(group, "Up")
    wn.onkeypress(godown, "Down")
    wn.onkeypress(goleft, "Left")
    wn.onkeypress(goright, "Right")

    segments = []
    im = True
    
    # Main Gameplay Loop
    while im:
        wn.update()
        
        # Check collision with borders
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            pen.goto(0, 0)
            pen.color("red")
            pen.write("GAME OVER!", align="center", font=("candara", 30, "bold"))
            wn.update()
            
            time.sleep(1.5)
            
            head.goto(0, 0)
            head.direction = "Stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            
            score = 0
            delay = 0.1
            
            pen.clear()
            pen.goto(0, 250)
            pen.color("white")
            pen.write("Score : {} High Score : {} ".format(score, high_score), align="center", font=("candara", 24, "bold"))
            
        # Check collision with food
        if head.distance(food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)

            # Adding segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("../images/lucky.gif")  # Use the registered shape
            new_segment.penup()
            segments.append(new_segment)
            
            delay = max(0.02, delay - 0.005)
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write("Score : {} High Score : {} ".format(score, high_score), align="center", font=("candara", 24, "bold"))
            
        # Move body segments in reverse order
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)
            
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)
            
        move()
        
        # Check collision with own body
        for segment in segments:
            if segment.distance(head) < 20:
                pen.goto(0, 0)
                pen.color("red")
                pen.write("GAME OVER!", align="center", font=("candara", 30, "bold"))
                wn.update()
                
                time.sleep(1.5)
                
                head.goto(0, 0)
                head.direction = "Stop"
                for s in segments:
                    s.goto(1000, 1000)
                segments.clear()

                score = 0
                delay = 0.1
                
                pen.clear()
                pen.goto(0, 250)
                pen.color("white")
                pen.write("Score : {} High Score : {} ".format(score, high_score), align="center", font=("candara", 24, "bold"))
                
        time.sleep(delay)

    wn.mainloop()

if __name__ == "__main__":
    snake()
