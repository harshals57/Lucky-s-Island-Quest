import pygame
import os
import mazeoni
import e
import arrowjumper

os.chdir("F:\\d_CLASS")
pygame.init()

yellow = (255, 255, 0)
brown = (165, 42, 42)

g = pygame.image.load("stars.jpg")
gg = pygame.transform.scale(g, (800, 800))
l = pygame.image.load("g.png")
imp = pygame.transform.scale(l, (250, 250))

# Set the dimensions of the window
width = 800
height = 600
window_size = (width, height)

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Create the window
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Homepage")

font = pygame.font.Font("w.ttf", 20)
font2 = pygame.font.Font("w.ttf", 16)

# Create the text
text = font.render("Choose your game!", True, black)

# Create the buttons
button_width = 600
button_height = 70
button_spacing = 20

button1_rect = pygame.Rect((width - button_width) // 2, 200, button_width, button_height)
button2_rect = pygame.Rect((width - button_width) // 2, 200 + button_height + button_spacing, button_width, button_height)
button3_rect = pygame.Rect((width - button_width) // 2, 200 + 2 * (button_height + button_spacing), button_width, button_height)
button4_rect = pygame.Rect((width - button_width) // 2, 200 + 3 * (button_height + button_spacing), button_width, button_height)

# Function to draw the homepage UI
def draw_homepage():
    window.fill(black)
    window.blit(gg, (0, 0))
    pygame.draw.rect(window, brown, button1_rect)
    pygame.draw.rect(window, yellow, button2_rect)
    pygame.draw.rect(window, brown, button3_rect)
    pygame.draw.rect(window, yellow, button4_rect)
    window.blit(text, (220, 167))
    window.blit(imp, (250, 10))

    button1_text = font2.render("An Arching Jump!- Obstacle Runner", True, yellow)
    button2_text = font2.render("Peek-a-boo! with Onis - Maze Runner", True, brown)
    button3_text = font2.render("Eat it all you can! - Slither Runner", True, yellow)
    button4_text = font2.render("Aqua-mania sprint - Running Game", True, brown)

    window.blit(button1_text, (button1_rect.x + 10, button1_rect.y + 10))
    window.blit(button2_text, (button2_rect.x + 10, button2_rect.y + 10))
    window.blit(button3_text, (button3_rect.x + 10, button3_rect.y + 10))
    window.blit(button4_text, (button4_rect.x + 10, button4_rect.y + 10))

    pygame.display.update()

# Main function to handle the homepage and game logic
def main():
    running = True
    while running:
        draw_homepage()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if button1_rect.collidepoint(mouse_pos):
                        arrowjumper.arrow()  # Run the first game
                    elif button2_rect.collidepoint(mouse_pos):
                        mazeoni.oni()  # Run the second game
                    elif button3_rect.collidepoint(mouse_pos):
                        e.snake()  # Run the third game
                    elif button4_rect.collidepoint(mouse_pos):
                        print("Aqua-mania sprint - Running Game selected!")
        
        # Refresh the homepage display after the game ends
        pygame.display.update()

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
