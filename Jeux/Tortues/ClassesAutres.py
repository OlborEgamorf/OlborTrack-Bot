class Carte:
    def __init__(self,couleur,valeur):
        self.couleur=couleur
        self.valeur=valeur


class Cellule:
    def __init__(self,v,s):
        self.valeur=v
        self.suivante=s


class Pile:
    def __init__(self):
        self.contenu=None
    def est_vide(self):
        return self.contenu is None
    def empiler(self,v):
        self.contenu=Cellule(v,self.contenu)
    def depiler(self):
        if self.est_vide()==True:
            raise IndexError("La liste est vide")
        v=self.contenu.valeur
        self.contenu=self.contenu.suivante
        return v     
    def __len__(self):
        count=0
        cel=self.contenu
        while cel is not None:
            count+=1
            cel=cel.suivante
        return count