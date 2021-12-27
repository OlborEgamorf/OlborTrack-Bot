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