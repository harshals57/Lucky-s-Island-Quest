import pygame
import random
import os
import sys

# Set working directory to the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

pygame.init()

# Set up the game window
win_width = 1000
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Obstacle Runner - An Arching Jump!")

# Set up the dino
dino_width = 100
dino_height = 100
dino_x = 100
dino_y = 350  # Stands at y=350, bottom is y=450
dino_vel = 15
dino_jump_vel = 22
dino_jump = False
dino_img = pygame.image.load('lucky.jpg')
o = pygame.transform.scale(dino_img, (dino_width, dino_height))

# Set up the cactus
cactus_width = 32
cactus_height = 64
cactus_x = win_width + cactus_width
cactus_y = win_height - cactus_height - 50  # bottom is y=450
cactus_vel = 15  # starts fast
cactus_img = pygame.image.load('cactus.png')

# Set up the score
score = 0
font = pygame.font.SysFont('Lucida Console', 40, True)
background_image = pygame.image.load('bg.png')
w = pygame.transform.scale(background_image, (1000, 500))

# Set up the game loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(30)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and not dino_jump:
                dino_jump = True
            if event.key == pygame.K_LEFT:
                dino_x -= dino_vel
            if event.key == pygame.K_RIGHT:
                dino_x += dino_vel

    # Constrain dino to screen bounds
    if dino_x < 0:
        dino_x = 0
    elif dino_x > win_width - dino_width:
        dino_x = win_width - dino_width

    # Move the dino (jump physics)
    if dino_jump:
        dino_y -= dino_jump_vel
        dino_jump_vel -= 1
        if dino_jump_vel < -22:
            dino_jump = False
            dino_jump_vel = 22
            dino_y = 350  # Reset back to ground level
    else:
        dino_y = 350  # Clamp to ground

    # Move the cactus with wild, unpredictable velocity fluctuations
    cactus_x -= cactus_vel
    
    # Fluctuate speed randomly on every single frame to create a jerky, unpredictable motion
    cactus_vel += random.randint(-3, 3)
    # Clamp speed between 12 (somewhat normal) and 45 (extremely fast!)
    cactus_vel = max(12, min(cactus_vel, 45))

    if cactus_x < -cactus_width:
        cactus_x = win_width + cactus_width
        score += 1
        # Set a brand new, highly unpredictable random base speed for the next obstacle
        cactus_vel = random.randint(15, 42)

    # Check for collision (using padded rects for fairer gameplay)
    dino_rect = pygame.Rect(dino_x + 15, dino_y + 10, dino_width - 30, dino_height - 15)
    cactus_rect = pygame.Rect(cactus_x + 5, cactus_y + 5, cactus_width - 10, cactus_height - 5)
    
    if dino_rect.colliderect(cactus_rect):
        # Game over screen
        game_over = True
        while game_over:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((win_width, win_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            win.blit(overlay, (0, 0))
            
            go_font = pygame.font.SysFont('Lucida Console', 48, True)
            sub_font = pygame.font.SysFont('Lucida Console', 24, True)
            
            go_text = go_font.render("GAME OVER", True, (255, 50, 50))
            score_text = sub_font.render(f"Score: {score}", True, (255, 255, 255))
            restart_text = sub_font.render("Press SPACE to Restart or ESC to Exit", True, (255, 255, 255))
            
            win.blit(go_text, (win_width // 2 - go_text.get_width() // 2, win_height // 2 - 80))
            win.blit(score_text, (win_width // 2 - score_text.get_width() // 2, win_height // 2 - 10))
            win.blit(restart_text, (win_width // 2 - restart_text.get_width() // 2, win_height // 2 + 40))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart game parameters
                        dino_x = 100
                        dino_y = 350
                        dino_jump = False
                        dino_jump_vel = 22
                        cactus_x = win_width + cactus_width
                        cactus_vel = 15
                        score = 0
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        game_over = False

    # Draw the game
    win.fill((255, 255, 255))
    win.blit(w, (0, 0))
    win.blit(o, (dino_x, dino_y))
    win.blit(cactus_img, (cactus_x, cactus_y))
    
    # Draw Score
    score_text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(score_text, (win_width - score_text.get_width() - 20, 20))
    
    pygame.display.update()

pygame.quit()
sys.exit()
