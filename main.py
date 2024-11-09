import random

import pygame

pygame.init()


# Couleurs
ROUGE = (255, 0, 0)

# Données de base et fond d ecran
image_fond = pygame.image.load("./assets/map.png")
dimensions_fenetre = (800, 600)
LARGEUR_FENETRE, HAUTEUR_FENETRE = dimensions_fenetre[0], dimensions_fenetre[1]

# Horloge du jeu
horloge = pygame.time.Clock()
# temps_actuel_en_s = pygame.time.get_ticks() / 1000
dernier_temps = 0

# Fenêtre
ecran = pygame.display.set_mode(dimensions_fenetre)


# Message avertissement si on dépasse la limite du jeu
police = pygame.font.SysFont("monospace", HAUTEUR_FENETRE // 20, True)
message = police.render("Vous avez atteint la limite du monde Vous perdez de la vie", True, ROUGE)

message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
position_message = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)
afficher_texte = True
intervalle_clignotement = 0.5
dernier_temps_clignotement = 0




# Son alerte
son_limite = pygame.mixer.Sound("./assets/beep.mp3")
projectile_tire = False


# Icône et titre de la fenêtre
icone_jeu = pygame.image.load("./assets/icon.png")
pygame.display.set_icon(icone_jeu)
pygame.display.set_caption("Space Rush")



# Configuration du joueur
joueur_image = pygame.transform.smoothscale(
    pygame.image.load("assets/spaceship.png").convert_alpha(), (85, 85)
)
joueur_taille = joueur_image.get_size()
joueur = {
    "image": joueur_image,
    "position": [LARGEUR_FENETRE // 2-joueur_taille[0]//2, HAUTEUR_FENETRE - 80],
    "vitesse": [10, 8],
    "vie": 100,
}


# Configuration du projectile
projectile_image = pygame.transform.smoothscale(
    pygame.image.load("assets/projectile.png").convert_alpha(), (20, 30))
projectile_taille = projectile_image.get_size()
def nouveau_projectile():
    return {
        "image": projectile_image,

        "vitesse": 8,
        "position": [joueur['position'][0]+joueur_taille[0]//2-projectile_taille[0]//2, joueur['position'][1]],
    }



# Fonction pour afficher le fond
def afficher_fond():
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.smoothscale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))



def nouveau_ennemi(id):
    global ennemi_taille
    type_ennemi = ["Alien1", "Alien2", "Alien3"]
    t_choice = random.choice(type_ennemi)
    ennemi_image = pygame.transform.smoothscale(
    pygame.image.load(f"./assets/Ennemis/{t_choice}.png").convert_alpha(), (70, 70))
    ennemi_taille = ennemi_image.get_size()
    # Génération initiale de la position
    position_valide = False
    while not position_valide:
        nouvelle_position = [random.randint(0, LARGEUR_FENETRE - 70), -ennemi_taille[1]]
        rect_nouvel_ennemi = pygame.Rect(nouvelle_position, (70, 70))

        # Vérification de la superposition avec les autres ennemis
        position_valide = True
        for ennemi in liste_ennemis:
            if rect_nouvel_ennemi.colliderect(ennemi["rect"]):
                position_valide = False
                break
    vitesses = [0.5, 1, 1.5,2]
    random_vitesse = random.choice(vitesses)
    # Si la position est valide, on crée l'ennemi avec cette position
    ennemi = {
        "image_choice": t_choice,
        "id": id,
        "position": nouvelle_position,
        "vitesse": random_vitesse,
        "acceleration": [0, 0],
        "vie": 100,
        "image": ennemi_image,
    }
    ennemi["rect"] = pygame.Rect(ennemi["position"], ennemi["image"].get_size())
    return ennemi








# Gere les entrées utilisateurs.
temps_tir_precedent = 0
delai_tir = 0.17


def gerer_entrees():
    global temps_tir_precedent
    global en_cours, joueur, projectile, projectile_tire, dernier_temps, dt
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
    touches = pygame.key.get_pressed()
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        joueur["position"][0] += joueur["vitesse"][0]
    if touches[pygame.K_LEFT] or touches[pygame.K_q]:
        joueur["position"][0] -= joueur["vitesse"][0]
    if touches[pygame.K_UP] or touches[pygame.K_z]:
        joueur["position"][1] -= joueur["vitesse"][1]
    if touches[pygame.K_DOWN] or touches[pygame.K_s]:
        joueur["position"][1] += joueur["vitesse"][1]

    if touches[pygame.K_SPACE] and temps_actuel_en_s - temps_tir_precedent > delai_tir:
        tirer_projectile()
        temps_tir_precedent=temps_actuel_en_s







def afficher_joueur():
    ecran.blit(joueur["image"], (joueur["position"]))


liste_projectiles = []
def afficher_projectiles():
    for projectile in liste_projectiles[:]:
        projectile["rect"] = pygame.Rect(projectile["position"], projectile["image"].get_size())
        projectile["position"][1] -= projectile["vitesse"]
        ecran.blit(projectile["image"], projectile["position"])

liste_ennemis = []


dernier_temps_spawn = 0
def generer_ennemis():
    global dernier_temps_spawn
    nbr_aleatoire = random.randint(1, 2)
    if temps_actuel_en_s - dernier_temps_spawn > 2:
        if nbr_aleatoire==2 and len(liste_ennemis)==5:
            nbr_aleatoire = 1
        for x in range(nbr_aleatoire):
            a = nouveau_ennemi(x)
            liste_ennemis.append(a)
            a["rect"] = pygame.Rect(a["position"], ennemi_taille)
        dernier_temps_spawn = temps_actuel_en_s

def afficher_ennemis():
    for i in liste_ennemis:
        ecran.blit(i["image"], (i["position"]))
        i["position"][1] += i["vitesse"]
        i["rect"] = pygame.Rect(i["position"], i["image"].get_size())


def tirer_projectile():
    projectile = nouveau_projectile()
    liste_projectiles.append(projectile)


def detecter_collisions():
    # Vérifie à droite
    if joueur["position"][0] + joueur_taille[0] >= LARGEUR_FENETRE:
        joueur["position"][0] = LARGEUR_FENETRE - joueur_taille[0]
    # Vérifie à gauche
    if joueur["position"][0] <= 0:
        joueur["position"][0] = 0
    # Vérifie en bas
    if joueur["position"][1] + joueur_taille[1] >= HAUTEUR_FENETRE:
        joueur["position"][1] = HAUTEUR_FENETRE - joueur_taille[1]
    # Verifie si le joueur dépasse la limite
    if joueur["position"][1] <= -200:
        joueur["position"][1] = -200
        clignoter_texte(message, position_message)
    #Verifie si les projectiles sont sortis de l'écran
    for projectile in liste_projectiles[:]:
        for ennemi in liste_ennemis[:]:
            if projectile["rect"].colliderect(ennemi["rect"]):
                degats_image = pygame.transform.smoothscale(pygame.image.load(f"./assets/Ennemis/{ennemi['image_choice']}-hit.png").convert_alpha(),(70, 70),)
                ecran.blit(degats_image, (ennemi["position"][0], ennemi["position"][1]-ennemi["vitesse"]))
            if ennemi["position"][1] >= HAUTEUR_FENETRE:
                liste_ennemis.remove(ennemi)


# Sert à faire un texte d'alerte si le joueur dépasse la limite
def clignoter_texte(texte, position):
    global dernier_temps_clignotement, afficher_texte
    if pygame.time.get_ticks() / 1000 - dernier_temps_clignotement> intervalle_clignotement:
        afficher_texte = not afficher_texte
        dernier_temps_clignotement = pygame.time.get_ticks() / 1000
    if afficher_texte:
        ecran.blit(texte, position)
        pygame.mixer.Sound.play(son_limite)


en_cours = True
while en_cours:
    temps_actuel_en_s = pygame.time.get_ticks() / 1000

    afficher_fond()
    gerer_entrees()
    afficher_joueur()
    if random.randint(0, 2) == 0 and len(liste_ennemis)<6:
        generer_ennemis()
    afficher_ennemis()
    afficher_projectiles()
    detecter_collisions()

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
