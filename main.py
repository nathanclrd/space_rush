import random
import pygame

pygame.init()

# Données de base et fond d ecran
image_fond = pygame.image.load("./assets/map.png")
dimensions_fenetre = (800, 600)
LARGEUR_FENETRE, HAUTEUR_FENETRE = dimensions_fenetre[0], dimensions_fenetre[1]

# definition de la fenêtre
ecran = pygame.display.set_mode(dimensions_fenetre)

# Police message avertissement si on dépasse la limite du jeu.
police = pygame.font.SysFont('monospace', HAUTEUR_FENETRE // 20, True)
ROUGE = (255, 0, 0)

# Son alerte
son_limite = pygame.mixer.Sound("./assets/beep.mp3")
projectile_tire = False

# Gestion du temps
horloge = pygame.time.Clock()

OFFSET_BAS = 40

# Icône et titre de la fenêtre
icone_jeu = pygame.image.load("./assets/icon.png")
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icone_jeu)

def afficher_fond():
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.smoothscale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))

# Configuration du joueur
joueur_image = pygame.transform.smoothscale(pygame.image.load("./assets/SpaceShip.png").convert_alpha(), (85, 85))
joueur_taille = joueur_image.get_size()
joueur = {
    "image": joueur_image,
    "position": [LARGEUR_FENETRE // 2, HAUTEUR_FENETRE-80],
    "vitesse": [0, 0],
    "vie": 100,
}
# joueur["position_initiale"] = [LARGEUR_FENETRE // 2 - joueur['taille'][0] // 2, HAUTEUR_FENETRE - joueur['taille'][1] - OFFSET_BAS]

# Configuration du projectile
projectile = {
    "image": pygame.transform.smoothscale(pygame.image.load("./assets/Projectile.png").convert_alpha(), (20, 30)),
    "position": [0, 0],
    "vitesse": [0, 8],
    "acceleration": [0, 0],
}

projectile["taille"] = projectile["image"].get_size()
projectile["position_initiale"] = [LARGEUR_FENETRE // 2 - projectile['taille'][0] // 2, HAUTEUR_FENETRE - projectile['taille'][1] - OFFSET_BAS]
# Message d'avertissement
message = police.render("Vous avez atteint la limite du monde", True, ROUGE)
message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
position_message = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)

afficher_texte = True
intervalle_clignotement = 0.5
dernier_temps_clignotement = pygame.time.get_ticks() / 1000
temps_actuel = pygame.time.get_ticks() / 1000
dernier_temps = 0

liste_projectiles = []
for projectile in liste_projectiles[:]:
    projectile["rect"].y += projectile["vitesse"]
    if projectile["rect"].bottom < 0:
        liste_projectiles.remove(projectile)


def nouvel_ennemi(id):

    type_ennemi = ["Alien1","Alien2","Alien3"]
    t = random.choice(type_ennemi)
    return {
        
        'image_choice' : t,
        "id": id,
        "position": [random.randint(0,LARGEUR_FENETRE-70), 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        "vie": 100,
        "image": pygame.transform.smoothscale(pygame.image.load(f"./assets/{t}.png").convert_alpha(), (70, 70)),
}

liste_ennemis = []

for x in range(random.randint(1,5)):
    a  = nouvel_ennemi(x)
    a['rect'] = pygame.Rect(a['position'],a['image'].get_size())
    liste_ennemis.append(a)




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
        projectile['position'][0] = joueur['position'][0] + (joueur_taille[0] // 2) - (projectile['taille'][0] // 2)
        projectile_tire = True

# joueur['position'] = joueur['position_initiale']

def afficher_joueur():
    ecran.blit(joueur['image'], (joueur['position']))

def afficher_ennemis():
    global liste_ennemis
    for i in liste_ennemis:
        ecran.blit(i['image'], (i['position']))

def tirer_projectile():
    global projectile, projectile_tire
    if projectile_tire:
        projectile['position'][1] -= projectile['vitesse'][1]
        ecran.blit(projectile['image'], (projectile['position']))
    if projectile['position'][1] < 0:
        projectile_tire = False
    projectile['rect'] = pygame.Rect(projectile['position'],projectile['image'].get_size())
    liste_projectiles.append(projectile)

def detecter_collisions():
    if joueur['position'][0] + joueur_taille[0] >= LARGEUR_FENETRE:
        joueur['position'][0] = LARGEUR_FENETRE - joueur_taille[0]
    if joueur['position'][0] <= 0:
        joueur['position'][0] = 0
    if joueur['position'][1] + joueur_taille[1] >= HAUTEUR_FENETRE:
        joueur['position'][1] = HAUTEUR_FENETRE - joueur_taille[1]
    if joueur['position'][1] <= -200:
        joueur['position'][1] = -200
        clignoter_texte(message, position_message)
    temps_hit = 0
    for ennemi in liste_ennemis[:]:
        if projectile["rect"].colliderect(ennemi["rect"]):
            degats_image = pygame.transform.smoothscale(pygame.image.load(f"./assets/{ennemi['image_choice']}-hit.png").convert_alpha(),(70, 70))
            ecran.blit(degats_image,ennemi['position'])



def clignoter_texte(texte, position):
    global dernier_temps_clignotement, intervalle_clignotement, afficher_texte
    if pygame.time.get_ticks() / 1000 - dernier_temps_clignotement > intervalle_clignotement:
        afficher_texte = not afficher_texte
        dernier_temps_clignotement = pygame.time.get_ticks() / 1000
    if afficher_texte:
        ecran.blit(texte, position)
        pygame.mixer.Sound.play(son_limite)

projectile['position'] = projectile['position_initiale']


pygame.key.set_repeat(40, 20)
en_cours = True
while en_cours:

    afficher_fond()
    gerer_entrees()
    afficher_joueur()
    afficher_ennemis()
    tirer_projectile()
    detecter_collisions()


    pygame.display.flip()
    horloge.tick(60)

pygame.quit()