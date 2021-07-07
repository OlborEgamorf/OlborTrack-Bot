import emoji

def emoteDetector(message):
    listeFinale=[]
    for i in message:
        if emoji.demojize(i)!=i:
            listeFinale.append(ord(i))
    decoup1=message.split(">")
    decoup2=[]
    for i in decoup1:
        decoup3=i.split(":")
        for j in decoup3:
            decoup2.append(j)
    for i in decoup2:
        try:
            if int(i)>100000000000000 and int(i)<9223372036854775807:
                listeFinale.append(i)
        except:
            pass
    return listeFinale