class Table:
    def __init__(self,option,mois,annee,*ids):
        idt=""
        if type(ids[0])==tuple:
            ids=ids[0]
        self.type=option
        self.table=[]
        self.idcomp=ids
        for i in ids:
            idt+=str(i)
        self.id=int(idt)
        self.mois=mois
        self.annee=annee

class UserEvol:
    def __init__(self,id):
        self.id=id
        self.mois=[]