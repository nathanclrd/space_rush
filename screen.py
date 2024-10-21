import pygame

bg_image = pygame.image.load("./assets/map.png")
dimensions_fenetre = (800,600)

screen = pygame.display.set_mode(dimensions_fenetre,pygame.RESIZABLE)

def bg():
    resized = screen.get_size()
    scaled_image = pygame.transform.smoothscale(bg_image,resized)
    screen.blit(scaled_image,(0,0))

