import pygame

pygame.init()

image_fond = pygame.image.load("./assets/map.png")
dimensions_fenetre = (800, 600)
LARGEUR_FENETRE, HAUTEUR_FENETRE = dimensions_fenetre[0], dimensions_fenetre[1]

ecran = pygame.display.set_mode(dimensions_fenetre)

police = pygame.font.SysFont('monospace', HAUTEUR_FENETRE // 20, True)
ROUGE = (255, 0, 0)

son_limite = pygame.mixer.Sound("./assets/beep.mp3")
projectile_tire = False

horloge = pygame.time.Clock()

OFFSET_BAS = 40

icone_jeu = pygame.image.load("./assets/icon.png")
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icone_jeu)

def afficher_fond():
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.smoothscale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))

joueur = {
    "image": pygame.transform.smoothscale(pygame.image.load("./assets/SpaceShip.png").convert_alpha(), (85, 85)),
    "position": [0, 0],
    "vitesse": [0, 0],
    "acceleration": [0, 0],
    "vie": 100,
}
joueur["taille"] = joueur["image"].get_size()
joueur["position_initiale"] = [LARGEUR_FENETRE // 2 - joueur['taille'][0] // 2, HAUTEUR_FENETRE - joueur['taille'][1] - OFFSET_BAS]

projectile = {
    "image": pygame.transform.smoothscale(pygame.image.load("./assets/Projectile.png").convert_alpha(), (20, 30)),
    "position": [0, 0],
    "vitesse": [0, 8],
    "acceleration": [0, 0],
}
projectile["taille"] = projectile["image"].get_size()
projectile["position_initiale"] = [LARGEUR_FENETRE // 2 - projectile['taille'][0] // 2, HAUTEUR_FENETRE - projectile['taille'][1] - OFFSET_BAS]

message = police.render("Vous avez atteint la limite du monde", True, ROUGE)
message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
position_message = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)

afficher_texte = True
intervalle_clignotement = 0.5
dernier_temps_clignotement = pygame.time.get_ticks() / 1000
temps_actuel = pygame.time.get_ticks() / 1000
dernier_temps = 0

def nouvel_ennemi(id):
    return {
        "id": id,
        "position": [0, 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        "vie": 100,
    }

liste_ennemis = [nouvel_ennemi(x) for x in range(10)]
print(liste_ennemis)

dt = temps_actuel - dernier_temps

def gerer_entrees():
    global en_cours, joueur, projectile, projectile_tire, dernier_temps, dt
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    touches = pygame.key.get_pressed()
    if touches[pygame.K_RIGHT]:
        joueur['position'][0] += 12
    if touches[pygame.K_LEFT]:
        joueur['position'][0] -= 12
    if touches[pygame.K_UP]:
        joueur['position'][1] -= 12
    if touches[pygame.K_DOWN]:
        joueur['position'][1] += 12
    if touches[pygame.K_SPACE] and not projectile_tire:
        projectile['position'][1] = joueur['position'][1]
        projectile['position'][0] = joueur['position'][0] + (joueur['taille'][0] // 2) - (projectile['taille'][0] // 2)
        projectile_tire = True

joueur['position'] = joueur['position_initiale']

def afficher_joueur():
    ecran.blit(joueur['image'], (joueur['position']))

def detecter_collisions():
    if joueur['position'][0] + joueur['taille'][0] >= LARGEUR_FENETRE:
        joueur['position'][0] = LARGEUR_FENETRE - joueur['taille'][0]
    if joueur['position'][0] <= 0:
        joueur['position'][0] = 0
    if joueur['position'][1] + joueur['taille'][1] >= HAUTEUR_FENETRE:
        joueur['position'][1] = HAUTEUR_FENETRE - joueur['taille'][1]
    if joueur['position'][1] <= -200:
        joueur['position'][1] = -200
        clignoter_texte(message, position_message)

def clignoter_texte(texte, position):
    global dernier_temps_clignotement, intervalle_clignotement, afficher_texte
    if pygame.time.get_ticks() / 1000 - dernier_temps_clignotement > intervalle_clignotement:
        afficher_texte = not afficher_texte
        dernier_temps_clignotement = pygame.time.get_ticks() / 1000
    if afficher_texte:
        ecran.blit(texte, position)
        pygame.mixer.Sound.play(son_limite)

projectile['position'] = projectile['position_initiale']

def tirer_projectile():
    global projectile, projectile_tire
    if projectile_tire:
        projectile['position'][1] -= projectile['vitesse'][1]
        ecran.blit(projectile['image'], (projectile['position']))
    if projectile['position'][1] < 0:
        projectile_tire = False

pygame.key.set_repeat(40, 20)
en_cours = True
while en_cours:
    temps_actuel = pygame.time.get_ticks() / 1000
    dt = temps_actuel - dernier_temps
    afficher_fond()
    gerer_entrees()
    detecter_collisions()
    afficher_joueur()
    tirer_projectile()
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()