import pygame
import random
pygame.init()


bg_image = pygame.image.load("./assets/map.png")
dimensions_fenetre = (800,600)
LARGEUR_FENETRE,HAUTEUR_FENETRE= dimensions_fenetre[0],dimensions_fenetre[1]

screen = pygame.display.set_mode(dimensions_fenetre)

police = pygame.font.SysFont('monospace', HAUTEUR_FENETRE//20, True)
JAUNE= (255,255,0)

limit_sound = pygame.mixer.Sound("./assets/limit.mp3")


BOTTOM_OFFSET = 40

gameIcon = pygame.image.load("./assets/icon.png")

pygame.display.set_caption("Space Invaders")
 
# set icon
pygame.display.set_icon(gameIcon)


def bg():
    resized = screen.get_size()
    scaled_image = pygame.transform.smoothscale(bg_image,resized)
    screen.blit(scaled_image,(0,0))
    
    
joueur = {
    "image" : pygame.transform.smoothscale(pygame.image.load("./assets/SpaceShip.png").convert_alpha(),(85,85)),
    "position" : [0,0],
    "vitesse" : [0,0],
    "acceleration": [0,0],
    "vie" : 100,
}
joueur["size"] = joueur["image"].get_size()
joueur["position_init"] = [LARGEUR_FENETRE//2-joueur['size'][0]//2,HAUTEUR_FENETRE-joueur['size'][1]-BOTTOM_OFFSET]

message = police.render("Vous avez atteint la limite du monde", True,JAUNE)
message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
message_position = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)

show_text = True
blink_interval = 0.5
last_blink_time = pygame.time.get_ticks()/1000

def newEnnemy():
    return {
    "position" : [0,0],
    "vitesse" : [0,0],
    "acceleration": [0,0],
    "vie" : 100,
}


def inputs():
    global running,joueur
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #controls
        if event.type == pygame.KEYDOWN:      
            if event.key == pygame.K_RIGHT:
                joueur['position'][0] += 12
            if event.key == pygame.K_LEFT:
                joueur['position'][0] -= 12
            if event.key == pygame.K_UP:
                joueur['position'][1] -=12
            if event.key == pygame.K_DOWN:
                joueur['position'][1] +=12

joueur['position'] = joueur['position_init']
def displayPlayer():
    screen.blit(joueur['image'],(joueur['position']))

def collision():
    global HAUTEUR_FENETRE,LARGEUR_FENETRE
    if joueur['position'][0]+joueur['size'][0] >= LARGEUR_FENETRE:
        joueur['position'][0] = LARGEUR_FENETRE - joueur['size'][0]
    if joueur['position'][0]<= 0:
        joueur['position'][0] = 0
    if joueur['position'][1]+joueur['size'][1]>= HAUTEUR_FENETRE:
        joueur['position'][1] = HAUTEUR_FENETRE - joueur['size'][1]
    if joueur['position'][1]<= -200:
        joueur['position'][1] = -200
        flicker_text(message,message_position)
        
        
        ## Commencer a perdre la barre de vie si on reste

def flicker_text(message,position):
    global last_blink_time, blink_interval, show_text
    if pygame.time.get_ticks()/1000 - last_blink_time > blink_interval:
        show_text = not show_text  # Alterner l'affichage du texte
        last_blink_time = pygame.time.get_ticks()/1000  # Réinitialiser le temps
    if show_text :
        screen.blit(message,position)
        pygame.mixer.Sound.play(limit_sound)

def projectile():
    return


pygame.key.set_repeat(40, 20)
running = True
while running:
    bg()
    inputs()
    collision()
    displayPlayer()
    pygame.display.flip()
            
            
pygame.quit()