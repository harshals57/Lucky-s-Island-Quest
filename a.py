import cv2
import pygame
import os

os.chdir("E://")

# Initialize Pygame for audio playback
pygame.init()
pygame.mixer.init()

# Create a VideoCapture object and read from the input file
cap = cv2.VideoCapture('S.mp4')

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Get the video's frames per second (fps) and width and height
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

# Read until the video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Write the frame to the output video
        out.write(frame)

        # Play audio using Pygame
        pygame.mixer.music.load('S.mp4')  # Assuming audio is embedded in the video file
        pygame.mixer.music.play()

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Release the video capture and video writer objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
