import matplotlib.pyplot as plt
from tkinter import *
from random import uniform
try: import operator
except ImportError: sortkey = lambda x:x.rapport
else: sortkey = operator.attrgetter("rapport")
import math

class Objet:
    def __init__(self, poids, valeur):
        '''
        poids : float
        valeur : float
        '''
        #Les objets de la classe Objet héritent
        #des propriétés "poids", "valeur" et "rapport".
        self.poids = poids
        self.valeur = valeur
        self.rapport = valeur / poids

class Interface(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre,**kwargs)

        #Déclaration d'une variable 'AffichageValeurFinale' et affectation à 0
        self.AffichageValeurFinale = 0
        #Déclaration d'une liste 'liste' et affectation à l'ensemble vide
        self.liste =[]

        #Globalisation des variables get des champs de saisie (utiliser self. ???)
        global entree1, entree2, entree3, entree4, entree5, entree6



        ###################### Affichage Graphique ###############################

        #Affichage (Texte) de la valeur finale (Glouton et Résolution exacte)
        self.message = Label(fenetre, text="Entrez les valeurs")
        self.message.grid(row=1, column=2)
        self.message2 = Label(fenetre, text="")
        self.message2.grid(row=2, column=2)

        #Bouton Quitter (utilise .destroy)
        fenetre.bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.destroy)
        fenetre.bouton_quitter.grid(row=1, column=1)
        #Bouton d'affichage (def Affiche)
        self.affiche = Button(fenetre, text="Afficher", command=self.Affiche)
        self.affiche.grid(row=1, column=3)

        '''
        Textes et champs de saisie des différents paramètres
        nécessaire à la création des objets/de la liste d'objets.
        Pour les champs de saisie : .insert(0, "...") = valeur de base/pré-enregistrée
        '''
        self.display = Label(fenetre, text="Capacite : ")
        self.display.grid(row=3, column=1)
        entree1 = Entry(fenetre, width=10)
        entree1.insert(0, "100")
        entree1.grid(row=3, column=2)
        self.display = Label(fenetre, text="Nombre d'objet(s) : ")
        self.display.grid(row=4, column=1)
        entree2 = Entry(fenetre, width=10)
        entree2.insert(0, "5")
        entree2.grid(row=4, column=2)
        self.display = Label(fenetre, text="Poids minimal : ")
        self.display.grid(row=5, column=1)
        entree3 = Entry(fenetre, width=10)
        entree3.insert(0, "10")
        entree3.grid(row=5, column=2)
        self.display = Label(fenetre, text="Poids maximal : ")
        self.display.grid(row=6, column=1)
        entree4 = Entry(fenetre, width=10)
        entree4.insert(0, "100")
        entree4.grid(row=6, column=2)
        self.display = Label(fenetre, text="Valeur minimale : ")
        self.display.grid(row=7, column=1)
        entree5 = Entry(fenetre, width=10)
        entree5.insert(0, "10")
        entree5.grid(row=7, column=2)
        self.display = Label(fenetre, text="Valeur maximale : ")
        self.display.grid(row=8, column=1)
        entree6 = Entry(fenetre, width=10)
        entree6.insert(0, "100")
        entree6.grid(row=8, column=2)

        #Bouton de création d'objets (def Definition)
        self.bouton_definition = Button(fenetre, text="Création d'objets", command=self.Definition)
        self.bouton_definition.grid(row=9, column=1)
        #Bouton d'algo de résolution avec méthode 'Glouton' (def Glouton)
        self.bouton_glouton = Button(fenetre, text="Glouton", command=self.Glouton)
        self.bouton_glouton.grid(row=9, column=2)
        #Bouton d'algo de résolution exacte (def SolExa)
        self.bouton_solExa = Button(fenetre, text="Résolution Exacte", command=self.SolExa)
        self.bouton_solExa.grid(row=9, column=3)


        #Déclaration des variables pour l'arbre de résolution (Canvas)
        self.largeur = 400
        self.hauteur = 400
        self.angle = math.pi/5 #facteur d'angle de séparation de deux branches
        self.taille = 0.58 #facteur de taille des branches
        #Canvas d'arbre de résolution exacte
        self.canvas = Canvas(fenetre, width = self.largeur, height = self.hauteur,bg="white")
        self.canvas.grid(row=1, rowspan=11, column=4)

        #Texte de la listebox
        self.display = Label(fenetre, text="Valeur")
        self.display.grid(row=10, column=1)
        self.display = Label(fenetre, text="Poids")
        self.display.grid(row=10, column=2)
        self.display = Label(fenetre, text="Rapport")
        self.display.grid(row=10, column=3)

        #Scrollbar de la listebox
        self.scrollbar = Scrollbar(fenetre)
        self.scrollbar.grid(row=11, column=4, sticky=W+N+S)

        #Listebox affichant les valeurs des propriétés des objets uniques
        self.listbox = Listbox(fenetre, width=60, yscrollcommand = self.scrollbar.set)
        self.listbox.grid(row=11, column=1, columnspan=3)



    def Glouton(self):
        '''
        Renvois la solution au problème du sac à dos selon la méthode 'glouton'.
        (ie. renvois une variable 'valeurFinale', un float.)
        '''
        #Affectation à 'capacite' de la valeur du champ de saisie 'entree'
        capacite = float(entree1.get())
        #Affectation à 'listing_des_objets' de la liste 'renvoyée' par Definition()
        listing_des_objets = self.liste
        #Déclaration et Affectation de la variable valeurFinale à 0
        #(ie. valeur optimale selon la méthode "glouton")
        valeurFinale = 0

        #Tri décroissant de la liste d'objets (selon leur propriété "rapport") 'renvoyée' par la fonction Definition()
        listing_des_objets = sorted(listing_des_objets, key=sortkey, reverse=True)

        #On parcourt la liste des objets triées
        for position in range(len(listing_des_objets)):
            #Si l'objet peut entrée dans le sac
            if listing_des_objets[position].poids <= capacite :
                #Alors on soustrait le poids de l'objet à la capacité du sac
                capacite -= listing_des_objets[position].poids
                #Et on ajoute la valeur de l'objet à la valeur totale/finale
                valeurFinale += listing_des_objets[position].valeur

        #Affiche la valeur de la variable 'valeurFinale' dans un label (champ) de texte
        self.AffichageValeurFinale = valeurFinale
        self.message["text"] = "Valeur Finale : {}".format(self.AffichageValeurFinale)

        

    def SolExa(self):
        '''
        Renvois la solution exacte au problème du sac à dos.
        (ie. renvois une variable 'valeurFinale', un float.)
        '''
        #Affectation à 'listing_des_objets' de la liste 'renvoyée' par Definition()
        listing_des_objets = self.liste

        if len(listing_des_objets) < 10:
            #Déclaration de la liste 'résultat' et affectation à l'ensemble vide
            resultat = []
            #Déclaration et Affectation de la variable valeurFinale à 0
            valeurFinale = 0
            #Affectation à 'capacite' de la valeur du champ de saisie 'entree'
            capacite = float(entree1.get())
            #Affectation à 'liste_des_permutation' de la liste des permutations (chemins) renvoyés par Permutation()
            liste_des_permutations = Permut(listing_des_objets)

            '''
            Affecation à la variable 'temporaire' du couple (valeurFinale, liste_des_objets)
            pour le premier chemin possible renvoyé par la fonction Calc
            '''
            self.temporaire = Calc(liste_des_permutations[0])
            #Pour chaque chemin possible
            for position in range(len(liste_des_permutations)-1):
                '''
                Si la valeur de la variable en position 0 du couple renvoyé par la fonction "Calc"
                ie. la valeur de la varaible "valeurFinale" du chemin numero position-ième, est supérieur à la valeur
                de la variable "valeurFinale" du couple affecté à la variable "temporaire"
                '''
                if Calc(liste_des_permutations[position])[0]>self.temporaire[0]:
                    '''
                    Alors on affecte à 'temporaire', le couple dont la valeur de la variable en position 0
                    (ie. valeurFinale)
                    '''
                    self.temporaire = Calc(liste_des_permutations[position])
                '''
                Sinon alors cela signifie que temporaire[0] est supérieur donc on garde la valeur
                de temporaire[0] comme valeur finale jusqu'à rencontrer un chemin avec une valeur finale supérieur.
                Ou alors la fonction SolExa 'renvoit' la valeur de temporaire[0], en tant que valeur finale
                et donc temporaire[1] est le chemin le plus optimisé.
                '''    

            #Affiche la valeur de la variable 'resultat[0]' dans un label (champ) de texte
            resultat = self.temporaire[0]
            self.chemin = self.temporaire[2]
            self.message2["text"] = "Valeur Finale : {}".format(resultat)

            ##################### Affichage Graphique ##############################
            #Affichage du Canvas/de l'arbre de la résolution exacte
            self.canvas.delete("line")
            #Autant de couche que d'objet (logique)
            couche = len(listing_des_objets)
            #Renvois le résultat de la fonction AfficheBranche
            self.AfficheBranche(couche, self.largeur/2, self.hauteur, self.hauteur/3, math.pi/2, couleur="black")
            self.AfficherChemin(couche, self.largeur/2, self.hauteur, self.hauteur/3, math.pi/2)
            ##########################################################
            rang = len(self.temporaire[1])
            for position in range(len(self.temporaire[1])):
                #On récupère les valeurs des propriétés de chacun des objets
                poids = self.temporaire[1][position].poids
                valeur = self.temporaire[1][position].valeur
                rapport = valeur/poids
            
                #Mise à jour de la listebox (On utilise les valeurs récupérées juste avant)
                self.listbox.insert(END, str(valeur) + ' | ' + str(poids) + ' | ' + str(rapport) + ' | ' + str(rang))
                self.listbox.grid(row=11, column=1, columnspan=3)
                #Mise à jour de la scrollbar
                self.scrollbar.config(command = self.listbox.yview)
                rang -= 1



    def Definition(self):
        '''
        Crée une liste d'objets de class Objet qui hérite d'un poids aléatoire (float)
        et d'une valeur aléatoire (float)
        '''
        
        #Affectation aux variables les valeurs des champs de saisie
        quantite = int(entree2.get())
        min_poids = float(entree3.get())
        max_poids = float(entree4.get())
        min_valeur = float(entree5.get())
        max_valeur = float(entree6.get())
        
        #Déclaration de liste qui contiendra quantite-ième objets crées,
        #affectation/initialisation à l'ensemble vide
        listing_des_objets = []

        for cree_objet in range(quantite):
            #création d'un objet de class Objet qui hérite d'un poids aléatoire et d'une valeur aléatoire
            objet_unique = Objet(uniform(min_poids, max_poids), uniform(min_valeur, max_valeur))
            #ajout de l'objet à liste des objets
            listing_des_objets.append(objet_unique)

        #Récupère la liste crée par Definition()
        self.liste = listing_des_objets


        ##################### Affichage Graphique ############################
        #Tri de la liste (Du meilleur rapport au plus mauvais)
        liste = sorted(self.liste, key=sortkey, reverse=True)
        #liste= self.liste
        self.listbox.delete(0, 'end')
        for position in range(len(self.liste)):
            #On récupère les valeurs des propriétés de chacun des objets
            poids = liste[position].poids
            valeur = liste[position].valeur
            rapport = valeur/poids
            
            #Mise à jour de la listebox (On utilise les valeurs récupérées juste avant)
            self.listbox.insert(END, str(valeur) + ' | ' + str(poids) + ' | ' + str(rapport))
            self.listbox.grid(row=11, column=1, columnspan=3)
            #Mise à jour de la scrollbar
            self.scrollbar.config(command = self.listbox.yview)



    # Affichage Graphique #    
    def Affiche(self):
        '''
        La fonction Affiche permet l'affichage d'une courbe des objets
        (avec le rang des objets annotés selon leur rapport)
        avec un axe x (poids) et un axe y (valeur)
        '''
        
        #On récupère (avec .get) les paramètres des champs de saisie
        #précisement : poids et valeur (min et max)
        min_poids = float(entree3.get())
        max_poids = float(entree4.get())
        min_valeur = float(entree5.get())
        max_valeur = float(entree6.get())
        
        #On déclare deux listes vides
        #(une liste des poids et une liste des valeurs)
        self.liste_poids = []
        self.liste_valeur = []
        self.temporaire_poids = []
        self.temporaire_valeur = []

        #Déclaration de n une liste vide
        n = []
        for i in range(1, len(self.liste)+1):
            n.append(i)

        self.liste = sorted(self.liste, key=sortkey, reverse=True)
        for position in range(len(self.liste)):
            self.liste_poids.append(self.liste[position].poids)
            self.liste_valeur.append(self.liste[position].valeur)

        #Definition des axes x et y
        #l'axe x : poids
        x = self.liste_poids
        plt.xlabel('Poids')
        #l'axe y : valeur
        y = self.liste_valeur
        plt.ylabel('Valeur')

        for position in range(len(self.temporaire[1])):
            self.temporaire_poids.append(self.temporaire[1][position].poids)
            self.temporaire_valeur.append(self.temporaire[1][position].valeur)

        xSolExa = self.temporaire_poids
        ySolExa = self.temporaire_valeur

        #Définition des limitations des axes (On utilise les paramètres récupérés)
        plt.axis([min_poids, max_poids, min_valeur, max_valeur])
        #Place les points selon les coordonnées des listes x et y
        plt.scatter(x,y, marker="+")
        plt.scatter(xSolExa, ySolExa, marker="x")
        for position, txt in enumerate(n):
            #Annotation des rangs des objets
            plt.annotate(txt, (x[position], y[position]))
            
        #Affichage de la courbe
        plt.show()


    # Affichage Graphique #
    def AfficheLigne(self, x1, y1, x2, y2, couleur):
        '''
        La fonction AfficheLigne permet l'affichage d'une ligne sur le canvas.
        x1, y1, x2, y2 : float
        couleur : string
        '''
        self.canvas.create_line(x1,y1, x2,y2, fill = couleur,  tags = "line")


    # Affichage Graphique #
    def AfficheBranche(self, couche, x1, y1, longueur, angle, couleur):
        '''
        La fonction AfficheBranche est une fonction récursive
        permettant l'affichage de branches selon le nombre de couche, ie. le nombre d'objets.
        couche : integer
        x1, y1, longueur : float
        angle : math.pi (float)
        couleur : string
        '''
        #Si le nombre de couche/d'objet est supérieur à 0 (nécessaire pour résolution) Alors:
        if couche >= 0:
            couche -= 1
            x2 = x1 + int(math.cos(angle) * longueur)
            y2 = y1 - int(math.sin(angle) * longueur)

            #Affiche une ligne
            self.AfficheLigne(x1,y1, x2,y2, couleur)
            
            if self.chemin[couche] == 1:
                #Affiche la branche de gauche
                self.AfficheBranche(couche, x2, y2, longueur * self.taille, angle + self.angle, couleur="green")
                #Affiche la branche de droite
                self.AfficheBranche(couche, x2, y2, longueur * self.taille, angle - self.angle, couleur="red")
            else:
                #Affiche la branche de gauche
                self.AfficheBranche(couche, x2, y2, longueur * self.taille, angle + self.angle, couleur="green")
                #Affiche la branche de droite
                self.AfficheBranche(couche, x2, y2, longueur * self.taille, angle - self.angle, couleur="red")

            #Annotation des branches avec l'objet correspondant (en vert si sélectionné, rouge sinon)
            if couche != len(self.liste)-1 :
                self.canvas.create_text(x2, y2, text=len(self.liste)-couche-1, fill = "black")


    # Affichage Graphique #
    def AfficherChemin(self, couche, x1, y1, longueur, angle):
        if couche >= 0:
            couche -= 1
            x2 = x1 + int(math.cos(angle) * longueur)
            y2 = y1 - int(math.sin(angle) * longueur)

            self.AfficheLigne(x1, y1, x2, y2, "blue")
            if self.chemin[couche]==1:
                self.AfficherChemin(couche, x2, y2, longueur * self.taille, angle + self.angle)
            else:
                self.AfficherChemin(couche, x2, y2, longueur * self.taille, angle - self.angle)
        


# Affichage Graphique #
'''def Chemin(resultat, liste_des_objets):
    capacite = float(entree1.get())
    #liste = liste_des_objets
    liste = sorted(liste_des_objets, key=sortkey, reverse=False)
    #resultat = sorted(resultat[1], key=sortkey, reverse=False)
    #resultat[1].reverse()
    chemin=[]
    objet_manquant=0
    retirer = 0
    for position in range(len(resultat[1])):
        if resultat[1][position-retirer].poids < capacite:
            capacite -= resultat[1][position].poids
        else:
            resultat[1].remove(resultat[1][position-retirer])
            retirer += 1
    for position in range(len(resultat[1])):
        if resultat[1][position-objet_manquant]==liste[position]:
            chemin.append(1)
        else:
            chemin.append(0)
            objet_manquant+=1
    while len(chemin) < len(liste):
        chemin.append(0)
    return chemin
'''

def Permut(liste):
    '''
    La fonction Permut est une fonction récursive
    renvoyant une liste de toute les permutations possible d'une liste d'objets.
    liste : list
    '''

    #On déclare résultat une liste vide
    #(la futur liste des permutations renvoyées par la fonction)
    resultat=[]

    #Si la liste ne contient qu'un seul objet
    if len(liste)==1:
        #Alors aucune permutation n'est possible
        resultat = [liste]
    else :
        #Sinon
        for position in range(len(liste)):
            '''
            Affectation à la variable permutation d'une liste de permutation.
            Cette liste de permutation est renvoyée par la fonction Permut.
            Ainsi la fonction Permut s'appelle elle-même on parle de récursivité.
            '''
            permutation=Permut(liste[0:position]+liste[position+1:len(liste)])
            #On parcourt la liste permutation
            for position_2 in range(len(permutation)):
                #Ajout à la liste resultat, d'une liste des permutations.
                resultat.append([liste[position]]+permutation[position_2])
    #Renvois la liste des permuations possible
    return resultat


def Calc(liste_objets):
    '''
    liste_objets : une liste d'objets de class Objet
    Renvois un couple d'un rapport et d'une liste d'objet
    '''
    #Récupère la capacite du champ de saisie (de base = 1000)
    capacite = float(entree1.get())
    #Déclaration du couple renvoyé par la fonction
    couple = (0, 0, 0)
    #Déclaration et Affectation des variables valeur et poids à 0
    valeur=0
    chemin = []
    for position in range(len(liste_objets)):
        '''Si le poids de l'objet en position 'position' et inférieur ou égale
        à la capacite et que le poids totale calculer jusque maintenant est inférieur
        à la capacite (ie. si l'objet suivant peut être ajouté au sac (selon son
        propre poids et la capacite restante)) alors :'''
        if liste_objets[position].poids < capacite:
            #calcule du poids total et de la valeur totale
            capacite -= liste_objets[position].poids
            valeur += liste_objets[position].valeur
            chemin.append(1)
        else:
            chemin.append(0)
    #affectation de la variable valeur et de la liste d'objets au couple
    couple = (valeur, liste_objets, chemin)
    return couple


fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
interface.destroy()
