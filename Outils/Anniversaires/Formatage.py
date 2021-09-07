from time import strftime

def formatageAnniv(alerte,user):
    new=""
    mention=alerte.split("{user}")
    longMention=len(mention)
    for i in range(longMention):
        new+=mention[i]
        if i!=longMention-1:
            new+="<@{0}>".format(user.id)
    
    newN=""
    name=new.split("{name}")
    longName=len(name)
    for i in range(longName):
        newN+=name[i]
        if i!=longName-1:
            newN+="{0}".format(user.name)

    newG=""
    guildName=newN.split("{date}")
    longGuild=len(guildName)
    for i in range(longGuild):
        newG+=guildName[i]
        if i!=longGuild-1:
            newG+="{0}/{1}/20{2}".format(strftime("%d"),strftime("%m"),strftime("%y"))
    
    return newG