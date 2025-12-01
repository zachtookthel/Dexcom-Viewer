import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
from pydexcom import Dexcom
import datetime
import pygame
import time

# Initialize pygame and window
pygame.init()
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Glucose Monitor")

# Dexcom setup
user = input("Username: ")
passw = input("Password: ")
reg = input("Region (us for United States, jp for Japan, ous for everywhere else): ")
dexcom = Dexcom(username=user, password=passw, region=reg)

# Fonts
bigfont = pygame.font.SysFont('Arial', 160)
smallfont = pygame.font.SysFont('Arial', 50)

# Images
bg = pygame.image.load('img/bg.png')
appicon = pygame.image.load('img/icon.png')

# Window icon setup
pygame.display.set_icon(appicon)

def get_glucose():
    ### Fetch the latest glucose data.
    glucose_reading = dexcom.get_current_glucose_reading()
    mmol = str(glucose_reading.mmol_l)
    where = str(glucose_reading.trend_description)
    return mmol, where

def display(mmol, where):
    ### Draw the glucose level and direction.
    # Clear screen
    screen.blit(bg, (0, 0))
    
    # Render new text surfaces
    ### Big font keeps the big text consistent and non-pixelated
    level_surface = bigfont.render(mmol, True, (0, 0, 0))
    ### Same for small font, self explanatory
    direct_surface = smallfont.render(where, True, (0, 0, 0))
    
    # Draw them to screen
    screen.blit(level_surface, (0, 225))
    screen.blit(direct_surface, (0, 385))
    
    # Update display
    pygame.display.flip()

# Initial display
mmol, where = get_glucose()
display(mmol, where)

running = True
last_update = 0
update_interval = 30  # seconds

while running:
    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()

    # Fetch and display new data every 30 seconds
    if time.time() - last_update > update_interval:
        mmol, where = get_glucose()
        display(mmol, where)
        print(mmol, where)
        last_update = time.time()

    # Small delay so we don't use 100% CPU
    time.sleep(0.1)
