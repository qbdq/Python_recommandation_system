"""
PARTIE II : SimilaritÃ© des Des users
 

***Author : 'abderrahmen gharsa 2LNBI3 ' 

***Date du dÃ©pot : du 17 -> 22 MAY 2021

*** Sujet : Un projet python qui permet de crÃ©e la similaritÃ© entre les produits 
et les profiles des utilisateurs pour affichier les produits similaire a un client
lors du navigation du site 

"""

### Importation des Packages


import mysql.connector
import numpy
from scipy import spatial
import sys


#Déclaration de la methode Similarié cosine
def similarteCos(IdUtilisateurX,IdUtilisateurY):
    return(1- spatial.distance.cosine(MatriceNote[IdUtilisateurX],MatriceNote[IdUtilisateurY]))


### Déclaration de la methode  ReturnTop3Users
## Qui retourne une list de top 3 rrecommendation des utilisateurs

def ReturnTop3Users (IdUtilisateur,Matrice_Similarite_Utilisateur):
    i=0
    Max1=0
    Max2=0
    Max3=0
    IndiceMax1=0
    IndiceMax2=0
    IndiceMax3=0
    for j in Matrice_Similarite_Utilisateur[IdUtilisateur-1]:
        if (j>Max1 and j<1):
            Max1=j
            IndiceMax1=i
        i+=1
    i=0
    for j in Matrice_Similarite_Utilisateur[IdUtilisateur-1]:
        if (j>Max2 and j<Max1):
            Max2=j
            IndiceMax2=i
        i+=1
    i=0
    for j in Matrice_Similarite_Utilisateur[IdUtilisateur-1]:
        if (j>Max3 and j<Max2):
            Max3=j
            IndiceMax3=i
        i+=1

    ListTop3=[IndiceMax1,IndiceMax2,IndiceMax3,Max1,Max2,Max3]
    return ListTop3



### cet notation nous permet d'affichier la totalité de la matrice dans le console
numpy.set_printoptions(threshold=sys.maxsize)



###Connexion Ã  la base de donnÃ©e "projetpython2021"
connexion = mysql.connector.connect(host="localhost",username="root",password="",database="projetpython2021")
cursor = connexion.cursor()
print("connexion Ã©tablie !") 


### Execution de la requete_select qui retourne le count de la table utilisateurs
Requete_Select1='select count(*) from customers'
cursor.execute(Requete_Select1)
UsersTuple=cursor.fetchone()
Nombre_Utilsateurs=UsersTuple[0]


### Execution de la requetes select qui retourne tous les produits de la table produits 
requete_select_products = "select * from products"
cursor.execute(requete_select_products)
rows = cursor.fetchall()
Nombre_Produits_Total= len(rows)


## execution de la requete select qyu retournes la table notes de la base de donnée 
Requete_Select2='Select * from notes'
cursor.execute(Requete_Select2)
notes=cursor.fetchall()


### execution de la requete select qui permet de retourner le contenu de la table costumeers
Requete_Select3='Select * from customers'
cursor.execute(Requete_Select3)
Customers=cursor.fetchall()

Requete_Select4='Select * from products'
cursor.execute(Requete_Select4)
Products=cursor.fetchall()

MatriceNote=numpy.zeros((Nombre_Utilsateurs,Nombre_Produits_Total))
i=0
j=0
SelectedItem=notes[0][1]
for note in notes:
   Code_Utilisateur=note[0]
   Code_Produit=note[1]
   if SelectedItem != Code_Produit:
       j=j+1
       i=0
       SelectedItem=Code_Produit
   MatriceNote[i][j]=note[2]
   i+=1    
   


### Cration de la matrice de similaritÃ© des utilisateurs
Matrice_Similarite_Utilisateur=numpy.zeros((Nombre_Utilsateurs,Nombre_Utilsateurs))
for x in range(Nombre_Utilsateurs):
    for j in range(Nombre_Utilsateurs):
        Matrice_Similarite_Utilisateur[x][j]=similarteCos(x,j)




Artice_Recherche=int(input('Please Enter a Valid product Number [1-110] :  '))
ID_User=int(input("Please Enter a Valid User number [1-122]: "))

ListTop3=ReturnTop3Users(ID_User-1,Matrice_Similarite_Utilisateur)
print("\n") 
CustomerID=Customers[ID_User-1][0]
CustomerName=Customers[ID_User-1][1]
ProductCode=Products[Artice_Recherche-1][0]
ProductName=Products[Artice_Recherche-1][1]
ProductType=Products[Artice_Recherche-1][2]


Max1=ListTop3[3]
Max2=ListTop3[4]
Max3=ListTop3[5]
Voisin1=ListTop3[0]
Voisin2=ListTop3[1]
Voisin3=ListTop3[2]

notePrediction=(Max1*MatriceNote[Voisin1][Artice_Recherche-1]) + (Max2*MatriceNote[Voisin2][Artice_Recherche-1]) +(Max3*MatriceNote[Voisin3][Artice_Recherche-1]) / (Max1+Max2+Max3) 

print("Pour le client sous le nom de : "+str(CustomerName)+" Et avec code_ID :"+str(CustomerID))
print("Code produit : "+ProductCode+" Nom du produit  : "+ProductName+" Type de produit = "+ProductType)
print("La note prédite base sur le filtrage collaboratif = "+str(notePrediction))

    