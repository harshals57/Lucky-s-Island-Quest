import pygame
import os
import sys
import time
import subprocess
import vlc
from pytubefix import YouTube

# Get dynamic base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Initialize Pygame
pygame.init()
pygame.mixer.init()

yellow = (255, 255, 0)
brown = (165, 42, 42)

# Load images from the images/ folder
g = pygame.image.load("images/stars.jpg")
gg = pygame.transform.scale(g, (800, 800))
l = pygame.image.load("images/g.png")
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

# Video helper function
def download_and_play(url, local_filename):
    filepath = os.path.join(BASE_DIR, local_filename)
    if not os.path.exists(filepath):
        print(f"Downloading {local_filename} from YouTube...")
        try:
            yt = YouTube(url)
            # Find progressive mp4 stream (contains both audio and video)
            stream = yt.streams.filter(file_extension="mp4", progressive=True).first()
            if not stream:
                stream = yt.streams.filter(file_extension="mp4").first()
            if stream:
                stream.download(output_path=BASE_DIR, filename=local_filename)
                print(f"Downloaded {local_filename} successfully.")
        except Exception as e:
            print(f"Error downloading video: {e}")
            
    if os.path.exists(filepath):
        print(f"Playing video {local_filename}...")
        try:
            # Create VLC player instance
            instance = vlc.Instance()
            media = instance.media_player_new()
            media.set_media(instance.media_new(filepath))
            
            # Embed VLC inside the Pygame window using HWND
            hwnd = pygame.display.get_wm_info()['window']
            media.set_hwnd(hwnd)
            
            media.play()
            
            # Sleep briefly to let it start
            time.sleep(0.5)
            
            # Wait for it to finish, allowing user to skip using Space, Escape, X key, or clicking the X close window button
            running_video = True
            play_game = True
            while running_video:
                state = media.get_state()
                if state in [vlc.State.Ended, vlc.State.Error, vlc.State.Stopped]:
                    break
                
                # Check for Pygame events to skip
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # Clicking window close button skips the video AND cancels launching the game
                        media.stop()
                        running_video = False
                        play_game = False
                        # Put the QUIT event back in the event queue so the main loop handles it and exits
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_x]:
                            media.stop()
                            running_video = False
                            break
                time.sleep(0.05)
            media.release()
            
            # Clear Pygame screen after video finishes so video frames don't linger
            window.fill(black)
            pygame.display.update()
            
            return play_game
        except Exception as e:
            print(f"Error playing video: {e}")
    return True

# Play startup video (if user closes this, play_game is False, we will exit)
if not download_and_play("https://youtu.be/MKQ4bX141zM", "intro.mp4"):
    pygame.quit()
    sys.exit()

# Start background music
pygame.mixer.music.load("[Official] Doodle Champion Island Games - Overworld.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def run_game_process(script_name, music_file):
    # Stop any running music
    pygame.mixer.music.stop()
    
    # Hide/Iconify launcher window
    pygame.display.iconify()
    
    # Load and play game specific music
    if music_file:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    
    # Launch sub-process
    print(f"Running game: {script_name}...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        
    # Re-focus and restore window
    pygame.display.set_mode(window_size)
    pygame.display.set_caption("Homepage")
    
    # Stop game music
    pygame.mixer.music.stop()
    
    # Resume launcher background music
    pygame.mixer.music.load("[Official] Doodle Champion Island Games - Overworld.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if button1_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Stop overworld music!
                    if download_and_play("https://youtu.be/1exYBdNZrhg", "swimming_intro.mp4"):
                        run_game_process("games/arrowjumper.py", "[Official] Doodle Champion Island Games - Artistic Swimming Song 1 (Rock).mp3")

                elif button2_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Stop overworld music!
                    if download_and_play("https://youtu.be/qsqWftxM3iU", "rugby_intro.mp4"):
                        run_game_process("games/mazeoni.py", "[Official] Doodle Champion Island Games - Rugby Theme.mp3")

                elif button3_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Stop overworld music!
                    if download_and_play("https://youtu.be/fgJy3Q0vzMw", "marathon_intro.mp4"):
                        run_game_process("games/e.py", "[Official] Doodle Champion Island Games - Marathon Theme.mp3")

                elif button4_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Stop overworld music!
                    if download_and_play("https://youtu.be/aeIySOUIQ2g", "skateboarding_intro.mp4"):
                        run_game_process("games/runningrace.py", "[Official] Doodle Champion Island Games - Skateboarding Theme.mp3")

    # Fill the window with background
    window.fill(black)
    window.blit(gg, (0, 0))
    
    # Draw buttons
    pygame.draw.rect(window, brown, button1_rect)
    pygame.draw.rect(window, yellow, button2_rect)
    pygame.draw.rect(window, brown, button3_rect)
    pygame.draw.rect(window, yellow, button4_rect)
    
    # Draw title text and image
    window.blit(text, (220, 167))
    window.blit(imp, (250, 10))

    # Add text to the buttons
    button1_text = font2.render("An Arching Jump!- Obstacle Runner", True, yellow)
    button2_text = font2.render("Peek-a-boo! with Onis - Maze Runner", True, brown)
    button3_text = font2.render("Eat it all you can! - Slither Runner", True, yellow)
    button4_text = font2.render("Aqua-mania sprint - Running Game", True, brown)

    window.blit(button1_text, (button1_rect.x + 10, button1_rect.y + 10))
    window.blit(button2_text, (button2_rect.x + 10, button2_rect.y + 10))
    window.blit(button3_text, (button3_rect.x + 10, button3_rect.y + 10))
    window.blit(button4_text, (button4_rect.x + 10, button4_rect.y + 10))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
