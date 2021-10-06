# -*- coding: utf-8 -*-
"""
PARTIE I : Similarité des produits 

***Author : 'abderrahmen gharsa 2LNBI3 

***Date du dépot : du 17 -> 22 MAY 2021

*** Sujet : Un projet python qui permet de crée la similarité entre les produits 
et les profiles des utilisateurs pour affichier les produits similaire a un client
lors du navigation du site 

"""

### Importation des Packages
import os
import nltk
import mysql.connector
import numpy
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from scipy import spatial
import sys
import math

### déclaration de la fonction calcul de similarité cosinus
def similarteCos(idpdtx,idpdty):
    return(1- spatial.distance.cosine(Matrice_De_Frequence[idpdtx],Matrice_De_Frequence[idpdty]))

#,Dictionaire_Occurance_Document
def TFID(Terme):
    Frequence = 0
    for mot in Terme_Dans_Document:
        if Terme==mot:
            Frequence+=1    
    TF=Frequence/len(Terme_Dans_Document)
    Nombre_Descriptions=len(Dictionaire_Des_Mots)
    Nombre_Description_Contenant_Stem=Dictionaire_Occurance_Document[Terme]   
    IDF=math.log(Nombre_Descriptions/Nombre_Description_Contenant_Stem)
    return TF*IDF


def ReturnTop3(indexItem,MatriceDeSimilarite):
    Max1=0
    Max2=0
    Max3=0
    IndiceMax1=0
    IndiceMax2=0
    IndiceMax3=0
    for z in range(Nombre_Des_Produits_Total):
        if (MatriceDeSimilarite[indexItem][z]>Max1 and MatriceDeSimilarite[indexItem][z]<1):
            Max1=MatriceDeSimilarite[indexItem][z]
            IndiceMax1=z
    for z in range(Nombre_Des_Produits_Total):
        if (MatriceDeSimilarite[indexItem][z]>Max2 and MatriceDeSimilarite[indexItem][z]<Max1):
            Max2=MatriceDeSimilarite[indexItem][z]
            IndiceMax2=z
    for z in range(Nombre_Des_Produits_Total):
        if (MatriceDeSimilarite[indexItem][z]>Max3 and MatriceDeSimilarite[indexItem][z]<Max2):
            Max3=MatriceDeSimilarite[indexItem][z]
            IndiceMax3=z         
    IndiceTop3=[IndiceMax1,IndiceMax2,IndiceMax3]  
    return IndiceTop3

### cet notation nous permet d'affichier la totalité de la matrice dans le console
numpy.set_printoptions(threshold=sys.maxsize)





###Connexion à la base de donnée "projetpython2021"
connexion = mysql.connector.connect(host="localhost",username="root",password="",database="projetpython2021")
cursor = connexion.cursor()
print("connexion établie !") 


### Execution de la requete select de tous les produits 
requete_select_products = "select * from products"
cursor.execute(requete_select_products)
rows = cursor.fetchall()
rowduplicated = rows
### Création de la liste Unnecessary qui est la liste du stop words 

Unnecessary =set(stopwords.words('english'))
Unnecessary = list(Unnecessary)
Unnecessary.extend(['!','?',"''",',',"'",'·','£','‘','$','.','%','&','+','-','^','$','﹩','＄','€','£','₤','₾','Ⴊ','ⴊ','ლ','₵','¥','￥','﷼','฿','|',':','.'])


#### Total_Words est une set contennant tous les mots 
###Nombre_Des_Produits_Total est le nombre de produit Total 
## Stemmer est l'english Stemmer importer du package NLTK
# Le dictionaire des mots contenient comme key l'id du produit et ca decription comme valeur
Total_Words=set()
Nombre_Des_Produits_Total=len(rows) 
Stemmer=EnglishStemmer()
Dictionaire_Des_Mots={}
Nombre_Des_Mots=0
Terme_Dans_Document=[]


    
    
    
for row in rows:
    ### Afftation du code et description du produit aux variable suivant 
    productCode=row[0]
    productDescription=row[5]
    
    ### La phase du tokenization et stemming
    mots=nltk.word_tokenize(productDescription)
    
    ### La phase du steaming
    MotsStemmed=[]
    for mot in mots:
        MotsStemmed.append(Stemmer.stem(mot))
        
    ### la phase du filtrage des wordsstops
    Mots_Final=[]
    for m in MotsStemmed:
        if m not in Unnecessary:
            Mots_Final.append(m)
            Terme_Dans_Document.append(m)  
            
      
   ### remplissage du dictionaire Dictionaire_Des_Mots[Code Produit]) 'Description
    for m in Mots_Final:
        Total_Words.add(m)
    Dictionaire_Des_Mots[productCode]=Mots_Final

    

"""
### Affichage du dictionaire ! 
print("----------------Affichage du dictionaire ------------")
for value  , key in Dictionaire_Des_Mots.items():
    print(value+' :',key)
    print("\n")
"""

### Rempllisage du dictionaire d'occurance dans un document pour la TFID 
### Key = Stem unique car Total_Words est un set des mot 
### Value = Nombre d'occurance de ce stem dans chaque description 
### Continue pour enlever la redondance de ce terme dans la meme description
### si il trouve le premier occurance dans une description et passe a l'autre description

Dictionaire_Occurance_Document={}
Occurance_Dans_Description=0
for m in Total_Words:    
    Occurance_Dans_Description=0
    for value in Dictionaire_Des_Mots.values():
        if m in value:
            Occurance_Dans_Description+=1
            continue;
    Dictionaire_Occurance_Document[m]=Occurance_Dans_Description


### remplissage d'une list des keys du dictionaire " Dictionaire_Des_Mots"
### Cet liste nous permet d'acceder dans le remplissage des matrices 
### au keys de chaque  Dictionaire
Value_Dictionary=list(Dictionaire_Des_Mots.keys())



### Deconnection
connexion.close()

Nombre_Des_Mots=len(Total_Words)


### Création du matrice de fréquence d'occurance
Matrice_De_Frequence=numpy.zeros((Nombre_Des_Produits_Total,Nombre_Des_Mots))

### Remplissage du matrice de fréquence : voir au dessous l'exemple du test
print("----------------------")
for i in range(Nombre_Des_Produits_Total):
    k=0
    for j in Total_Words:
        if j in Dictionaire_Des_Mots[Value_Dictionary[i]]:
            Matrice_De_Frequence[i][k]=TFID(j)
        k+=1   

### Affichage de la matric de fréquence
#print(Matrice_Binnaire)



### création de la matrice de similarité 
Matrice_Similarité_Produit=numpy.zeros((Nombre_Des_Produits_Total,Nombre_Des_Produits_Total))

### pour chauqe ligne / latruce dy latruce de matrice de fréquence on applique la  methode de smilaritécosine
for i in range(Nombre_Des_Produits_Total):
    for j in range(Nombre_Des_Produits_Total):
            Matrice_Similarité_Produit[i][j]=similarteCos(i,j)
        

###### Menu princiaple au lieu du site web ##########
ItemSelected=1
ItemScrolled=0
Programme_Running=True
while Programme_Running:
    print("*********Welcome to the our shop****** ")
    print("1-- If you want to see the items")
    print("2-- To Quit")
    ItemScrolled=0
    while 1:
        Message=input("Please enter a valid choice : = ")
        if int(Message)==1:
            ItemScrolled=0
            for row in rows:
                print("--------Product N°"+str(ItemScrolled+1)+"---------")
                productCode=row[0]
                productName=row[1]
                productType=row[2]
                print("Product ID = "+productCode)
                print("Product Name="+productName)
                print("Product Name="+productType)
                ItemScrolled+=1
            print("Would you like to see the full description of a certain item?")
            print("Press 0 if you wana go back to the main menu")
            while 1:
                ItemSelected=int(input("Please Enter a Valid Number from 0 to "+str(Nombre_Des_Produits_Total) +" : "))
                if ItemSelected==0:
                    Programme_Running=False
                    break
                elif (ItemSelected > 0 and ItemSelected<Nombre_Des_Produits_Total+1):
                    
                    ListItemSelected=[]
                    for item in rowduplicated[ItemSelected-1]:
                        ListItemSelected.append(item)
                    os.system("cls")
                    print("Product Code="+ListItemSelected[0])
                    print("Product Name ="+ListItemSelected[1])
                    print("product Line = "+ListItemSelected[2])
                    print("product Scale = "+ListItemSelected[3])
                    print("Product Vendor= "+ListItemSelected[4])
                    print("Product Description= "+ListItemSelected[5])
                    print("Product Quantity= "+str(ListItemSelected[6])+"$")
                    print("Product BuyPrice= "+str(ListItemSelected[7]) +"$")
                    print("**************** Top 3 recommanded items **********")
                    ListStop3=ReturnTop3(ItemSelected-1,Matrice_Similarité_Produit)
                    print("\n")
                    print(rows[ListStop3[0]])
                    print("\n")
                    print(rows[ListStop3[1]])
                    print("\n")
                    print(rows[ListStop3[2]])        
                else:
                     print("Please enter a valid number ! ")  
                    
        elif int(Message)==2:
            Programme_Running=False
            break
        else:
            print("Please enter a valid choice ! ")
            continue
                
        print("*********Welcome to the our shop****** ")
        print("1-- If you want to see the items")
        print("2-- To Quit")

                   
                                                      
                                       
                                       
                                       
                                       
                                       