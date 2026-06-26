import os
os.chdir("C:\\Users\\harshals\\Downloads\\dino")
import pygame
import random

# Initialize the game
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Platform Jumper")

# Load the player image
player_image = pygame.image.load("dino.png")
player_rect = player_image.get_rect()
player_rect.centerx = window_width // 2
player_rect.bottom = window_height - 10

# Load the platform image
platform_image = pygame.image.load("cactus.png")
platform_rect = platform_image.get_rect()
platform_rect.centerx = random.randint(0, window_width)
platform_rect.bottom = window_height

# Set up the game variables
score = 0
fall_speed = 5
jumping = False
jump_count = 10

running = False
start_game = False
while not running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game = True

    # Start the game when the start button is pressed
    if start_game:
        running = True
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True

    # Update the player position
    if jumping:
        player_rect.y -= jump_count
        jump_count -= 1
        if jump_count < 0:
            jumping = False
            jump_count = 10
    else:
        player_rect.y += fall_speed

    # Check if the player collides with the platform
    if player_rect.colliderect(platform_rect.rect):
        score += 20
        platform_rect.centerx = random.randint(0, window_width)
        platform_rect.bottom = window_height

    # Check if the player falls off the screen
    if player_rect.bottom > window_height:
        running = False

    # Draw the game elements
    window.fill((255, 255, 255))
    window.blit(player_image, player_rect)
    window.blit(platform_image, platform_rect)
    pygame.display.update()

# Game over
print("Game Over")
print("Score:", score)

# Quit the game
pygame.quit()
