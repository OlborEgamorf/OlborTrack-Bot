def triIDTable(element):
    return element.id

def dichotomieTable(tableau,valeur):
    a=0                                
    b=len(tableau)-1                    
    while a<=b:                                  
        c=(a+b)//2                          
        if tableau[c].id==valeur:    
            return True, c         
        elif tableau[c].id<valeur:          
            a=c+1
        else:                            
            b=c-1
    return False, 0

def sommeTable(table):
    total=0
    for i in table:
        total+=i["Count"]
    return total
    
def hideGD(guild,table,curseur):
    listeID=[]
    for i in guild.members:
        listeID.append(i.id)
    for i in table:
        if curseur.execute("SELECT * FROM users WHERE ID={0}".format(i["ID"])).fetchone()==None:
            curseur.execute("INSERT INTO users VALUES({0},{1},{2},{3})".format(i["ID"],False,False,False))
        if i["ID"] not in listeID:
            curseur.execute("UPDATE users SET Leave={0} WHERE ID={1}".format(True,i["ID"]))