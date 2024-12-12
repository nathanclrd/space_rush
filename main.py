"""
    Jeu Space Rush
    Repo : 
    Auteur :  COLARD Nathan
    Date :  2024-12-11
    Version :  1.0
    Description :  Jeu de tir en 2D semblable à Space Invaders.
    
    Source :
        Bibliothèque utilisées :
            - Pygame : https://www.pygame.org/
            - Random : https://docs.python.org/3/library/random.html
        Images : 
            -Map ; https://www.freepik.com/premium-vector/stars-darkness-background_6756913.htm
            -Spaceship : https://www.istockphoto.com/fr/vectoriel/%C3%A9l%C3%A9ments-de-lespace-r%C3%A9tro-arcade-jeu-pixel-envahisseurs-les-vaisseaux-les-gm950674686-259493753 
            -Projectile :https://www.istockphoto.com/fr/vectoriel/%C3%A9l%C3%A9ments-de-lespace-r%C3%A9tro-arcade-jeu-pixel-envahisseurs-les-vaisseaux-les-gm950674686-259493753  
            -Aliens : https://opengameart.org/content/space-shooter-environment
            -Meteorite : https://www.freepik.com/premium-vector/pixel-art-meteor-game-asset-design_359072043.htm
            -Logo menu : Leonardo AI
            -Gameover inspiré de : https://pngimg.com/image/83334
            -Aliens + modifié:https://stock.adobe.com/fr/images/character-sitting-in-spaceship-vector-alien-floating-in-space-pixelated-personage-of-8-bit-pixel-game-ufo-monster-with-prolonged-head-shape-flat-style-pixel-cosmic-monster-for-mobile-app-games/288837890?asset_id=334711288
        Polices : 

            - Pixelify :https://fonts.google.com/specimen/Pixelify+Sans 
        Effets sonores :
            -MP3 : https://pixabay.com/sound-effects/
            
    """

import random
import pygame


pygame.init()
pygame.mixer.init()
# Couleurs
ROUGE = (199, 9, 9)
VERT = (0, 204, 0)
BLANC = (255, 255, 255)

# Données de base et fond d ecran
image_fond = pygame.image.load("./assets/Others/map.png")
dimensions_fenetre = [800, 600]
LARGEUR_FENETRE, HAUTEUR_FENETRE = dimensions_fenetre[0], dimensions_fenetre[1]



# Horloge du jeu
horloge = pygame.time.Clock()
# temps_actuel_en_s = pygame.time.get_ticks() / 1000
dernier_temps = 0

# Fenêtre
ecran = pygame.display.set_mode(dimensions_fenetre)

# Message avertissement si on dépasse la limite du jeu
police = pygame.font.Font("assets/Polices/pixelify.ttf", HAUTEUR_FENETRE // 20)
message = police.render("Vous avez atteint la limite du monde", True, BLANC)

message_largeur, message_hauteur = police.size("Vous avez atteint la limite du monde")
position_message = ((LARGEUR_FENETRE - message_largeur) // 2, HAUTEUR_FENETRE // 3)
afficher_texte = True
intervalle_clignotement = 0.5
dernier_temps_clignotement = 0

#score
score = 0

# Son alerte
son_limite = pygame.mixer.Sound("./assets/Sons/beep.mp3")
son_limite.set_volume(0.8)
musique_menu = pygame.mixer.Sound("./assets/Sons/musique_menu.mp3")

#Son de tir
son_tir = pygame.mixer.Sound("./assets/Sons/projectile.mp3")
son_tir.set_volume(0.09)

#Son de heal
son_heal = pygame.mixer.Sound("./assets/Sons/heal.mp3")
son_heal.set_volume(0.09)

# Icône et titre de la fenêtre
icone_jeu = pygame.image.load("./assets/Others/icon.png")
pygame.display.set_icon(icone_jeu)
pygame.display.set_caption("Space Rush")

# Configuration du joueur
joueur_image = pygame.transform.scale(
    pygame.image.load("assets/Joueur/spaceship.png").convert_alpha(), (85, 85))
joueur_image_hit = pygame.transform.scale(
    pygame.image.load("assets/Joueur/spaceship-hit.png").convert_alpha(), (85, 85))
joueur_taille = joueur_image.get_size()
joueur = {
    "image": joueur_image,
    "image-hit" : joueur_image_hit,
    "position": [LARGEUR_FENETRE // 2 - joueur_taille[0] // 2, HAUTEUR_FENETRE - 80],
    "vitesse": [10, 8],
    "vie": 100,
    "puissance_tir" : 20,
    "touche":False,
    "touche_recente":100
}
# Configuration du projectile
projectile_image = pygame.transform.scale(
    pygame.image.load("assets/Others/projectile.png").convert_alpha(), (20, 30))
projectile_taille = projectile_image.get_size()

#image meteorite
meteorite_image = pygame.transform.scale(pygame.image.load("assets/Others/meteor.png").convert_alpha(), (60, 60))
def meteorite():
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

#image medkit
medkit_img = pygame.image.load("./assets/Others/medkit.png")
def soin():
    medkit_image = pygame.transform.scale(medkit_img,(60,50))
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
            if joueur["vie"] < 100:
                if joueur["vie"] +20 >100:
                    joueur["vie"] =100
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
image_menu =pygame.image.load("./assets/Others/logo_menu.png")
h = -50
affiche_all = False
def afficher_menu():
    global h,affiche_all
    afficher_fond()
    titre = pygame.transform.smoothscale(image_menu.convert_alpha(), (370, 250))
    jouer_texte = police.render("Appuyez sur Entrée pour jouer", True, BLANC)
    quitter_texte = police.render("Appuyez sur Echap pour quitter", True, BLANC)
    attention_texte = police.render("Attention , les météorite",True,ROUGE)
    attention_texte2 = police.render("vous tuent instantanément",True,ROUGE)
    if h< HAUTEUR_FENETRE // 9:
        h+=1
    else:
        affiche_all = True    
    
        
    ecran.blit(titre, (LARGEUR_FENETRE // 2 - titre.get_width() // 2, h))
    if affiche_all:
        ecran.blit(jouer_texte, (LARGEUR_FENETRE // 2 - jouer_texte.get_width() // 2, HAUTEUR_FENETRE // 2))
        ecran.blit(quitter_texte, (LARGEUR_FENETRE // 2 - quitter_texte.get_width() // 2, HAUTEUR_FENETRE // 2 + 60))
        ecran.blit(attention_texte,(LARGEUR_FENETRE // 2 - attention_texte.get_width() // 2, HAUTEUR_FENETRE // 2 + 120))
        ecran.blit(attention_texte2,(LARGEUR_FENETRE // 2 - attention_texte2.get_width()//2, HAUTEUR_FENETRE // 2 + 160))
    
    pygame.mixer.Sound.play(musique_menu)
    pygame.display.flip()


# Fonction pour afficher le fond
def afficher_fond():
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.scale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))

#aliens_image
def charger_ressources_ennemis():
    global tailles_alien,type_ennemi
    """Charge toutes les images et tailles des ennemis."""
    type_ennemi = ["Alien1","Alien2", "Alien3", "Alien4", "Alien5"]
    tailles_alien = {
        "Alien1": (70, 70),
        "Alien2": (100,100),
        "Alien3": (70, 70),
        "Alien4": (70, 70),
        "Alien5": (70, 70),
    }

    ressources_ennemis = {}
    for ennemi in type_ennemi:
        image = pygame.image.load(f"./assets/Aliens/{ennemi}.png").convert_alpha()
        image_redimensionnee = pygame.transform.scale(image, tailles_alien[ennemi])
        ressources_ennemis[ennemi] = {
            "image": image_redimensionnee,
            "taille": tailles_alien[ennemi],
        }

    return ressources_ennemis

ressources_ennemis = charger_ressources_ennemis()
exclude = True

def creer_ennemi(exclude):
    if exclude:
        
        choix_stage1 = random.choice([alien for alien in ressources_ennemis.keys() if alien != 'Alien2'])
        choix = ressources_ennemis[choix_stage1]
        ennemi_taille = choix["taille"]   
        ennemi_image = choix["image"]
        return ennemi_image,ennemi_taille,choix_stage1
    else:
        choix_stage1 = random.choice([alien for alien in ressources_ennemis.keys()])
        choix = ressources_ennemis[choix_stage1]
        ennemi_taille = choix["taille"]   
        ennemi_image = choix["image"]
        return ennemi_image,ennemi_taille,choix_stage1


def nouveau_ennemi(id):
    global tailles_alien,type_ennemi,ennemi_image,ennemi_taille,choix_stage1
    ennemi_image, ennemi_taille, choix_stage1 = creer_ennemi(exclude)
    # Génération initiale de la position
    position_valide = False
    while not position_valide:
        nouvelle_position = [random.randint(0, LARGEUR_FENETRE - 70), -ennemi_taille[1]]
        rect_nouvel_ennemi = pygame.Rect(nouvelle_position, (70, 70))

        # Vérification de la superposition avec ls autres ennemis
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
        "image_choice": choix_stage1,
        "id": id,
        "position": nouvelle_position,
        "vitesse": [random_vitesse_x, random_vitesse_y],
        "vie": 100,
        "image": ennemi_image,
        "max_vie" :100,
        "touche_recente":100,
        "touche":False
    }
    if choix_stage1 == "Alien2":
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
    global exclude
    if joueur["vie"] <= 0:
        lose = True
        clear_screen()
        exclude = True
        joueur["puissance_tir"]=20
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
    gameover = pygame.transform.smoothscale(pygame.image.load("./assets/Others/gameover.png").convert_alpha(), (400, 300))
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
    if joueur["position"][1] + joueur_taille[1] >= HAUTEUR_FENETRE+200:
        joueur["position"][1] = HAUTEUR_FENETRE - joueur_taille[1]+200
        clignoter_texte(message, position_message)
    # Verifie si le joueur dépasse la limite
    if joueur["position"][1] <= -200:
        joueur["position"][1] = -200
        clignoter_texte(message, position_message)
    #Verifie si les projectiles sont sortis de l'écran
    for projectile in liste_projectiles[:]:
        for ennemi in liste_ennemis[:]:
            if projectile["rect"].colliderect(ennemi["rect"]):
                ennemi["touche"] = True
                ennemi["vie"] -= joueur["puissance_tir"]
                if ennemi["vie"] <= 0:
                    score += 1
                    liste_ennemis.remove(ennemi)
                    for barre in barres_de_vie[:]:
                        if barre["ennemi"] == ennemi:
                            barres_de_vie.remove(barre)
                if projectile in liste_projectiles:
                    liste_projectiles.remove(projectile)
                if projectile["position"][1] < -projectile["image"].get_size()[1] and projectile in liste_projectiles:
                    liste_projectiles.remove(projectile)
            
                            
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


            joueur["position"][1] += ennemi["rect"].height //2
            joueur["touche"] = True
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


compteur_affichage=100
def stage2():
    global compteur_affichage,joueur,type_ennemi,tailles_alien,exclude
    clear_screen()
    taille_fenetre = ecran.get_size()
    image_redimensionnee = pygame.transform.scale(image_fond, taille_fenetre)
    ecran.blit(image_redimensionnee, (0, 0))
    texte_stage2 = police.render("Stage 2",True,BLANC)
    texte_power_down = police.render("Attention, votre arme fait moins de dégâts !",True,BLANC)
    ecran.blit(texte_stage2,(LARGEUR_FENETRE//2-texte_stage2.get_width()//2,HAUTEUR_FENETRE//2))
    ecran.blit(texte_power_down,(LARGEUR_FENETRE//2-texte_power_down.get_width()//2,HAUTEUR_FENETRE//2+40))
    if compteur_affichage==100:
        joueur["puissance_tir"]-=5
        exclude= False
    compteur_affichage-=1

def score_temporaire():
    global score
    if score == 20 and compteur_affichage >0:
        stage2()
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
    if joueur["touche"]==True and joueur["touche_recente"] != 0:

        ecran.blit(joueur_image_hit,(joueur["position"]))
        joueur["touche_recente"] -=2
        if joueur["touche_recente"] == 0:
            joueur["touche"] = False
            joueur["touche_recente"] = 100
    for ennemi in liste_ennemis:
        if ennemi["touche_recente"] !=0 and ennemi["touche"]:
            degats_image = pygame.transform.scale(pygame.image.load(f"./assets/Aliens/{ennemi['image_choice']}-hit.png").convert_alpha(),tailles_alien[ennemi["image_choice"]] )
            ecran.blit(degats_image,(ennemi["position"][0] - ennemi["vitesse"][0], ennemi["position"][1] - ennemi["vitesse"][1]))
            ennemi["touche_recente"] -=2
            if ennemi["touche_recente"] == 0:
                ennemi["touche"] = False
                ennemi["touche_recente"] = 100
    
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
        if rand_nombre == 0 and len(liste_ennemis) < 30:
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


