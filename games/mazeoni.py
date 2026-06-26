import os
from random import choice
from turtle import *
from freegames import floor, vector

# Set working directory to this script's directory (games/)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def oni():
    setup(420, 420, 370, 0)
    title("Maze Runner - Peek-a-boo! with Onis")
    hideturtle()
    tracer(False)
    
    # Register shapes from ../images/
    register_shape("../images/lucky.gif")
    register_shape("../images/oni.gif")

    state = {'score': 0, 'game_over': False}
    path = Turtle(visible=False)
    writer = Turtle(visible=False)
    aim = vector(5, 0)
    pacman = vector(-40, -80)
    ghosts = [
        [vector(-180, 160), vector(5, 0)],
        [vector(-180, -160), vector(0, 5)],
        [vector(100, 160), vector(0, -5)],
        [vector(100, -160), vector(-5, 0)],
    ]
    # fmt: off
    initial_tiles = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    # fmt: on
    tiles = list(initial_tiles)

    def square(x, y):
        """Draw square using path at (x, y)."""
        path.up()
        path.goto(x, y)
        path.down()
        path.begin_fill()

        for count in range(4):
            path.forward(20)
            path.left(90)

        path.end_fill()

    def offset(point):
        """Return offset of point in tiles."""
        x = (floor(point.x, 20) + 200) / 20
        y = (180 - floor(point.y, 20)) / 20
        index = int(x + y * 20)
        return index

    def valid(point):
        """Return True if point is valid in tiles."""
        index = offset(point)

        if tiles[index] == 0:
            return False

        index = offset(point + 19)

        if tiles[index] == 0:
            return False

        return point.x % 20 == 0 or point.y % 20 == 0

    def world():
        """Draw world using path."""
        bgcolor('black')
        path.color('green')

        for index in range(len(tiles)):
            tile = tiles[index]

            if tile > 0:
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                square(x, y)

                if tile == 1:
                    path.up()
                    path.goto(x + 10, y + 10)
                    path.dot(2, 'white')

    def move():
        """Move pacman and all ghosts."""
        if state['game_over']:
            return
            
        writer.undo()
        writer.write(state['score'])

        clear()

        if valid(pacman + aim):
            pacman.move(aim)

        index = offset(pacman)

        if tiles[index] == 1:
            tiles[index] = 2
            state['score'] += 1
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            
            # Check victory condition
            if state['score'] >= 100:
                state['game_over'] = True
                show_game_over_menu("YOU WIN!")
                return

        # Draw pacman with "lucky.gif" shape
        up()
        goto(pacman.x + 10, pacman.y + 10)
        shape("../images/lucky.gif")
        stamp()

        for point, course in ghosts:
            if valid(point + course):
                point.move(course)
            else:
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y

            up()
            goto(point.x + 10, point.y + 10)
            shape("../images/oni.gif")
            stamp()

        update()

        # Check collision with ghosts
        for point, course in ghosts:
            if abs(pacman - point) < 20:
                state['game_over'] = True
                show_game_over_menu("GAME OVER")
                return

        ontimer(move, 100)

    def show_game_over_menu(msg):
        writer.goto(0, 0)
        if msg == "YOU WIN!":
            writer.color('yellow')
        else:
            writer.color('red')
        writer.write(msg, align="center", font=("Arial", 30, "bold"))
        
        writer.goto(0, -40)
        writer.color('white')
        writer.write("Press SPACE to Restart or ESC to Exit", align="center", font=("Arial", 16, "bold"))
        update()
        
        # Listen for restart keys
        listen()
        onkey(restart_game, "space")
        onkey(bye, "Escape")

    def restart_game():
        # Reset tiles
        for i in range(len(tiles)):
            tiles[i] = initial_tiles[i]
            
        # Reset state variables
        state['score'] = 0
        state['game_over'] = False
        
        # Reset pacman and ghosts
        pacman.x = -40
        pacman.y = -80
        aim.x = 5
        aim.y = 0
        
        ghosts[0][0].x, ghosts[0][0].y = -180, 160
        ghosts[0][1].x, ghosts[0][1].y = 5, 0
        
        ghosts[1][0].x, ghosts[1][0].y = -180, -160
        ghosts[1][1].x, ghosts[1][1].y = 0, 5
        
        ghosts[2][0].x, ghosts[2][0].y = 100, 160
        ghosts[2][1].x, ghosts[2][1].y = 0, -5
        
        ghosts[3][0].x, ghosts[3][0].y = 100, -160
        ghosts[3][1].x, ghosts[3][1].y = -5, 0
        
        # Redraw the world
        path.clear()
        world()
        
        # Rebind movement keys
        listen()
        onkey(lambda: change(5, 0), 'Right')
        onkey(lambda: change(-5, 0), 'Left')
        onkey(lambda: change(0, 5), 'Up')
        onkey(lambda: change(0, -5), 'Down')
        
        # Re-run the move loop
        move()

    def change(x, y):
        """Change pacman aim if valid."""
        if valid(pacman + vector(x, y)):
            aim.x = x
            aim.y = y

    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])
    listen()
    onkey(lambda: change(5, 0), 'Right')
    onkey(lambda: change(-5, 0), 'Left')
    onkey(lambda: change(0, 5), 'Up')
    onkey(lambda: change(0, -5), 'Down')
    world()
    move()
    done()

if __name__ == "__main__":
    oni()
