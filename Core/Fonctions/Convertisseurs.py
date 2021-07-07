### Convertisseurs 
def convINT(table,*args):
    for i in table:
        for j in args:
            i[j]=int(i[j])
    return table
def convFLOAT(table,*args):
    for i in table:
        for j in range(0,len(args)-1):
            i[args[j]]=int(i[args[j]])
        i[args[len(args)-1]]=float(i[args[len(args)-1]])
    return table
#####

### Nique
def convZero(nombre):
    if len(str(nombre))==1:
        nombre="0"+str(nombre)
    return nombre
#####

def inverse(option,count):
    if option!="+":
        return -count
    return count