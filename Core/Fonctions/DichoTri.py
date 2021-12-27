### Dichotomies
def dichotomieID(tableau,valeur,option):
    a=0                                
    b=len(tableau)-1         
    if tableau==[]:
        return False, 0       
    while a<=b:                                  
        c=(a+b)//2                          
        if tableau[c][option]==valeur:    
            return True, c        
        elif tableau[c][option]<valeur:          
            a=c+1
        else:                            
            b=c-1
    return False, 0

def dichotomiePlage(tableau,valeur):
    a=0                                
    b=len(tableau)-1                    
    while a<=b:                                  
        c=(a+b)//2                          
        if tableau[c]==valeur:    
            return True, c         
        elif tableau[c]<valeur:          
            a=c+1
        else:                            
            b=c-1
    return False, 0
#####


### Tri
def nombre(element):
    return element["Count"]
def triID(element):
    return element["ID"]
def triVal(element):
    return element["Val"]
#####


def triPeriod(curseur,nom,tri):
    dictReverse={"periodAsc":False,"periodDesc":True}
    table=curseur.execute("SELECT * FROM {0}".format(nom)).fetchall()
    for i in table:
        i["Val"]=int(i["Annee"]+i["Mois"])
    table.sort(key=triVal,reverse=dictReverse[tri])
    return table