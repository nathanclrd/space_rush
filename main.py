import pygame
import screen
import player
pygame.init()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.bg()
    pygame.display.flip()
            
            
pygame.quit()