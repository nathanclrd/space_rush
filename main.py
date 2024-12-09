import random

import pygame

pygame.init()
pygame.mixer.init()
# Couleurs
ROUGE = (199, 9, 9)
VERT = (0, 204, 0)
JAUNE = (255, 255, 0)
ORANGE = (255, 128, 0)
BLANC = (255, 255, 255)

# Données de base et fond d ecran
image_fond = pygame.image.load("./assets/map.png")
dimensions_fenetre = [800, 600]
LARGEUR_FENETRE, HAUTEUR_FENETRE = dimensions_fenetre[0], dimensions_fenetre[1]



# Horloge du jeu
horloge = pygame.time.Clock()
# temps_actuel_en_s = pygame.time.get_ticks() / 1000
dernier_temps = 0

# Fenêtre
ecran = pygame.display.set_mode(dimensions_fenetre)

# Message avertissement si on dépasse la limite du jeu
police = pygame.font.SysFont("monospace", HAUTEUR_FENETRE // 20, True)
message = police.render("Vous avez atteint la limite du monde", True, BLANC)

message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
position_message = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)
afficher_texte = True
intervalle_clignotement = 0.5
dernier_temps_clignotement = 0

#score
score = 0

# Son alerte
son_limite = pygame.mixer.Sound("./assets/beep.mp3")
son_limite.set_volume(0.8)
musique_menu = pygame.mixer.Sound("./assets/musique_menu.mp3")

#Son de tir
son_tir = pygame.mixer.Sound("./assets/projectile.mp3")
son_tir.set_volume(0.09)

#Son de heal
son_heal = pygame.mixer.Sound("./assets/heal.mp3")
son_heal.set_volume(0.09)

# Icône et titre de la fenêtre
icone_jeu = pygame.image.load("./assets/icon.png")
pygame.display.set_icon(icone_jeu)
pygame.display.set_caption("Space Rush")

# Configuration du joueur
joueur_image = pygame.transform.scale(
    pygame.image.load("assets/spaceship.png").convert_alpha(), (85, 85))
joueur_image_hit = pygame.transform.scale(
    pygame.image.load("assets/spaceship-hit.png").convert_alpha(), (85, 85))
joueur_taille = joueur_image.get_size()
joueur = {
    "image": joueur_image,
    "image-hit" : joueur_image_hit,
    "position": [LARGEUR_FENETRE // 2 - joueur_taille[0] // 2, HAUTEUR_FENETRE - 80],
    "vitesse": [10, 8],
    "vie": 100,
}
# Configuration du projectile
projectile_image = pygame.transform.scale(
    pygame.image.load("assets/projectile.png").convert_alpha(), (20, 30))
projectile_taille = projectile_image.get_size()


def meteorite():
    meteorite_image = pygame.transform.scale(
        pygame.image.load("assets/meteor.png").convert_alpha(), (50, 50))
    meteorite_taille = meteorite_image.get_size()
    meteorite = {
        "image": meteorite_image,
        "position": [random.randint(0, LARGEUR_FENETRE - 70), -meteorite_taille[1]],
        "vitesse": [0, 2],
    }
    liste_meteorites.append(meteorite)


liste_meteorites = []
def afficher_meteorite():
    for i in liste_meteorites:
        ecran.blit(i["image"], (i["position"]))
        i["position"][1] += i["vitesse"][1]
        i["position"][0] += i["vitesse"][0]
        i["rect"] = pygame.Rect(i["position"], i["image"].get_size())

def soin():
    medkit_image = pygame.transform.scale(pygame.image.load("./assets/medkit.png"),(60,50))
    medkit = {
        "image": medkit_image,
        "position": [random.randint(0, LARGEUR_FENETRE - 70), -medkit_image.get_size()[1]],
        "vitesse": [0, 2.5],
    }
    liste_medkit.append(medkit)
liste_medkit = [] 
def afficher_soin():
    for s in liste_medkit:
        ecran.blit(s["image"], (s["position"]))
        s["position"][1] += s["vitesse"][1]
        s["position"][0] += s["vitesse"][0]
        s["rect"] = pygame.Rect(s["position"], s["image"].get_size())
        if s["rect"].colliderect(joueur["rect"]):
            if joueur["vie"] < 100 and joueur["vie"]+20 <= 100:
                joueur["vie"] += 20
                pygame.mixer.Sound.play(son_heal)
            liste_medkit.remove(s)



def nouveau_projectile():
    return {
        "image": projectile_image,
        "vitesse": 8,
        "position": [joueur['position'][0] + joueur_taille[0] // 2 - projectile_taille[0] // 2, joueur['position'][1]],
    }

# Afficher le menu
def afficher_menu():
    afficher_fond()
    titre = pygame.transform.smoothscale(pygame.image.load("./assets/logo_menu.png").convert_alpha(), (370, 250))
    jouer_texte = police.render("Appuyez sur Entrée pour jouer", True, BLANC)
    quitter_texte = police.render("Appuyez sur Echap pour quitter", True, BLANC)
    ecran.blit(titre, (LARGEUR_FENETRE // 2 - titre.get_width() // 2, HAUTEUR_FENETRE // 9))
    ecran.blit(jouer_texte, (LARGEUR_FENETRE // 2 - jouer_texte.get_width() // 2, HAUTEUR_FENETRE // 2))
    ecran.blit(quitter_texte, (LARGEUR_FENETRE // 2 - quitter_texte.get_width() // 2, HAUTEUR_FENETRE // 2 + 60))
    pygame.mixer.Sound.play(musique_menu)
    pygame.display.flip()


# Fonction pour afficher le fond
def afficher_fond():
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.scale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))


def nouveau_ennemi(id):
    global ennemi_taille, tailles_alien
    type_ennemi = ["Alien1", "Alien2", "Alien3", "Alien4", "Alien5"]
    tailles_alien = {
        "Alien1": (70, 70),
        "Alien2": (100, 100),
        "Alien3": (70, 70),
        "Alien4": (70, 70),
        "Alien5": (70, 70),
    }
    t_choice = random.choice(type_ennemi)
    ennemi_image = pygame.transform.scale(
        pygame.image.load(f"./assets/Ennemis/{t_choice}.png").convert_alpha(), tailles_alien[t_choice])
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
    vitesses_x = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]
    vitesses_y = [0.5, 1, 1.5, 2]
    random_vitesse_x = random.choice(vitesses_x)
    random_vitesse_y = random.choice(vitesses_y)
    # Si la position est valide, on crée l'ennemi avec cette position

    ennemi = {
        "image_choice": t_choice,
        "id": id,
        "position": nouvelle_position,
        "vitesse": [random_vitesse_x, random_vitesse_y],
        "vie": 100,
        "image": ennemi_image,
        "max_vie" :100,
        "touche_recente":100,
        "touche":False
    }
    if t_choice == "Alien2":
        ennemi["vie"] = 250
        ennemi["max_vie"] = 250
    ennemi["rect"] = pygame.Rect(ennemi["position"], ennemi_taille)
    barre_vie = nouvelle_barre_de_vie(ennemi)
    barres_de_vie.append(barre_vie)
    return ennemi


#Fonction barre de vie
barres_de_vie = []


def nouvelle_barre_de_vie(ennemi):
    largeur_barre = ennemi["image"].get_size()[0]
    return {
        "ennemi": ennemi,
        "hauteur_barre": 5,
        "largeur_barre": largeur_barre,
    }


# Gere les entrées utilisateurs.
temps_tir_precedent = 0
delai_tir = 0.18


    

def gerer_principal():
    global en_cours, menu,jeu,lose,score
    for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                jeu = False
                pygame.quit()
            if evenement.type == pygame.KEYDOWN:
                if en_cours:
                    if evenement.key == pygame.K_ESCAPE:
                        menu = True
                        en_cours = False
                elif menu:
                    if evenement.key == pygame.K_ESCAPE:
                        menu = False
                        en_cours = False
                        jeu = False
                        pygame.quit()
                    elif evenement.key == pygame.K_RETURN:
                        menu = False
                        en_cours = True
                        score = 0
                        pygame.mixer.Sound.stop(musique_menu)
                elif lose:
                    if evenement.key == pygame.K_ESCAPE:
                        lose = False
                        menu = True


def gerer_entrees():
    global en_cours, joueur, temps_tir_precedent,menu,jeu
    gerer_principal()

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
        temps_tir_precedent = temps_actuel_en_s

def afficher_joueur():
    if joueur["vie"] <= 0:
        lose = True
        clear_screen()
    ecran.blit(joueur["image"], (joueur["position"]))
    joueur["rect"] = pygame.Rect(joueur["position"], joueur_taille)
    pygame.draw.rect(ecran, ROUGE, (20, 20, joueur_taille[0], 5), border_radius=2)
    pygame.draw.rect(ecran, VERT, (20, 20, joueur_taille[0] * (joueur["vie"] / 100), 5),border_radius=2)

liste_projectiles = []
def afficher_projectiles():
    for projectile in liste_projectiles[:]:
        projectile["rect"] = pygame.Rect(projectile["position"], projectile["image"].get_size())
        projectile["position"][1] -= projectile["vitesse"]
        ecran.blit(projectile["image"], projectile["position"])

# Génère les ennemis
liste_ennemis = []
dernier_temps_spawn = 0

def generer_ennemis():
    global dernier_temps_spawn
    nbr_aleatoire = random.randint(1, 2)
    if temps_actuel_en_s - dernier_temps_spawn > 2:
        if nbr_aleatoire == 2 and len(liste_ennemis) == 5:
            nbr_aleatoire = 1
        for x in range(nbr_aleatoire):
            a = nouveau_ennemi(x)
            liste_ennemis.append(a)
            a["rect"] = pygame.Rect(a["position"], ennemi_taille)
        dernier_temps_spawn = temps_actuel_en_s


#affiche les ennemis
def afficher_ennemis():
    for i in liste_ennemis:
        ecran.blit(i["image"], (i["position"]))
        i["position"][1] += i["vitesse"][1]
        i["position"][0] += i["vitesse"][0]
        i["rect"] = pygame.Rect(i["position"], i["image"].get_size())
        for barre in barres_de_vie:
            if barre["ennemi"] == i:
                pygame.draw.rect(ecran, ROUGE, (i["position"][0], i["position"][1] - 10, barre["largeur_barre"], barre["hauteur_barre"]))
                pygame.draw.rect(ecran, VERT, (i["position"][0], i["position"][1] - 10, barre["largeur_barre"] * (i["vie"]/i["max_vie"]), barre["hauteur_barre"]))
#Tire un projectile
def tirer_projectile():
    projectile = nouveau_projectile()
    pygame.mixer.Sound.play(son_tir)
    liste_projectiles.append(projectile)

def ecran_lose():
    afficher_fond()
    gameover = pygame.transform.smoothscale(pygame.image.load("./assets/gameover.png").convert_alpha(), (400, 300))
    score_texte = police.render(f"Score :  {score}", True, ROUGE)
    jouer_texte = police.render("Appuyez sur Echap pour quitter", True, ROUGE)
    ecran.blit(gameover, (LARGEUR_FENETRE // 2 - 400 // 2, 100))
    ecran.blit(jouer_texte, (LARGEUR_FENETRE // 2 - jouer_texte.get_width() // 2, HAUTEUR_FENETRE-120 ))
    ecran.blit(score_texte, (LARGEUR_FENETRE // 2 - score_texte.get_width() // 2, HAUTEUR_FENETRE-170 ))
    pygame.mixer.Sound.play(musique_menu)
    pygame.display.flip()



compteur_ennemi_passe = 0
def detecter_collisions():
    global score, tailles_alien, barres_de_vie,lose,en_cours,temps_image_precedent,compteur_ennemi_passe
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
                ennemi["touche"] = True
                ennemi["vie"] -= 20
                if ennemi["vie"] <= 0:
                    score += 1
                    liste_ennemis.remove(ennemi)
                    for barre in barres_de_vie[:]:
                        if barre["ennemi"] == ennemi:
                            barres_de_vie.remove(barre)
                ennemi["touche_recente"] -=1
                liste_projectiles.remove(projectile)
                if ennemi["touche_recente"] == 0:
                    ennemi["touche"] = False
                    ennemi["touche_recente"] = 100
            
                            
    #Verifier si les aliens touchent un des bords
    for ennemi in liste_ennemis[:]:
        if ennemi["position"][0] + tailles_alien[ennemi["image_choice"]][0] >= LARGEUR_FENETRE:
            ennemi["vitesse"][0] = -ennemi["vitesse"][0]
        if ennemi["position"][0] <= 0:
            ennemi["vitesse"][0] = -ennemi["vitesse"][0]
        if ennemi["position"][1] >= HAUTEUR_FENETRE:
            joueur["vie"] -= 100/3
            liste_ennemis.remove(ennemi)
            ecran.blit(joueur["image-hit"], (joueur["position"]))

            if joueur["vie"] <= 0:
                lose = True
                en_cours = False
                joueur["vie"] = 100
                clear_screen()
        if ennemi["rect"].colliderect(joueur["rect"]):
            joueur["vie"] -= 100/5

            if joueur["position"][1]+joueur_taille[1]+ennemi["rect"].height//2> HAUTEUR_FENETRE:
                if joueur["position"][0]-joueur_taille[0]//2 >= LARGEUR_FENETRE//2:
                    joueur["position"][0] -= ennemi["rect"].width //2
                elif joueur["position"][0]-joueur_taille[0]//2 < LARGEUR_FENETRE//2:
                    joueur["position"][0] += ennemi["rect"].width //2
            else:
                joueur["position"][1] += ennemi["rect"].height //2
                ecran.blit(joueur["image-hit"], (joueur["position"]))
            if joueur["vie"] <= 0:
                lose = True
                en_cours = False
                joueur["vie"] = 100
                clear_screen()


    for meteor in liste_meteorites:
        if meteor["rect"].colliderect(joueur["rect"]):
            joueur["vie"] -= 99
            if joueur["vie"] <= 0:
                lose = True
                en_cours = False
                joueur["vie"] = 100
                clear_screen()



# Sert à faire un texte d'alerte si le joueur dépasse la limite
def clignoter_texte(texte, position):
    global dernier_temps_clignotement, afficher_texte
    if pygame.time.get_ticks() / 1000 - dernier_temps_clignotement > intervalle_clignotement:
        afficher_texte = not afficher_texte
        dernier_temps_clignotement = pygame.time.get_ticks() / 1000
    if afficher_texte:
        ecran.blit(texte, position)
        pygame.mixer.Sound.play(son_limite)


def score_temporaire():
    global score
    ecran.blit(police.render(f"Score: {score}", True, BLANC), (LARGEUR_FENETRE // 2 - 50, 10))

dernier_temps_meteorite = 0
def generer_meteor():
    global dernier_temps_meteorite
    dt = temps_actuel_en_s - dernier_temps_meteorite
    if dt > 5:
        meteorite()
        dernier_temps_meteorite = temps_actuel_en_s

dernier_temps_soin = 0
def generer_soin():
    global dernier_temps_soin
    dt = temps_actuel_en_s - dernier_temps_soin
    if dt > 10:
        soin()
        dernier_temps_soin = temps_actuel_en_s

def clear_screen():
    liste_meteorites.clear()
    liste_ennemis.clear()
    liste_medkit.clear()
    
    
def afficher_hit():
    for ennemi in liste_ennemis:
        if ennemi["touche_recente"] !=0 and ennemi["touche"]:
            degats_image = pygame.transform.scale(pygame.image.load(f"./assets/Ennemis/{ennemi['image_choice']}-hit.png").convert_alpha(),tailles_alien[ennemi["image_choice"]] )
            ecran.blit(degats_image,(ennemi["position"][0] - ennemi["vitesse"][0], ennemi["position"][1] - ennemi["vitesse"][1]))
            print(ennemi["touche_recente"])
            

jeu = True
en_cours = False
menu = True
lose = False

while jeu:
    if menu:
        afficher_menu()
        gerer_principal()
    if lose:
        ecran_lose()
        gerer_principal()
    if en_cours:
        temps_actuel_en_s = pygame.time.get_ticks() / 1000
        afficher_fond()
        gerer_entrees()
        afficher_joueur()
        rand_nombre = random.randint(0, 100)
        if rand_nombre == 0 and len(liste_ennemis) < 6:
            generer_ennemis()
        generer_meteor()
        generer_soin()
        afficher_soin()
        afficher_ennemis()
        afficher_hit()
        afficher_projectiles()
        afficher_meteorite()
        detecter_collisions()
        score_temporaire()
        
        
        pygame.mixer.Sound.stop(musique_menu)
        pygame.display.flip()
        
        
        horloge.tick(60)

