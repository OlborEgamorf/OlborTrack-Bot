from Core.Fonctions.TempsVoice import tempsVoice

def descipMoyennes(option,result):
    numb=len(result)
    count=0
    for i in result:
        count+=i["Count"]
    dictBloc={
        "Voicechan":"Total temps en vocal : {0}\Salons : {1}\nMoyenne par salon : {2}\nMeilleur salon : {3}\nMédiane : {4}\nPire salon : {5}".format(tempsVoice(count),numb,tempsVoice(int(count/numb)),tempsVoice(result[0]["Count"]),tempsVoice(result[len(result)//2]["Count"]),tempsVoice(result[len(result)-1]["Count"])),
        "Emotes":"Total emotes utilisées : {0}\nEmotes différentes : {1}\nMoyenne par emote : {2}\nMeilleure emote : {3}\nMédiane : {4}\nPire emote : {5}".format(count,numb,round(count/numb,3),result[0]["Count"],result[len(result)//2]["Count"],result[len(result)-1]["Count"]),
        "Reactions":"Total réactions utilisées : {0}\nRéactions différentes : {1}\nMoyenne par réaction : {2}\nMeilleure réaction : {3}\nMédiane : {4}\nPire réaction : {5}".format(count,numb,round(count/numb,3),result[0]["Count"],result[len(result)//2]["Count"],result[len(result)-1]["Count"]),
        "Salons":"Salons utilisés : {0}\nMoyenne messages par salon : {1}\nMeilleur salon : {2}\nMédiane : {3}\nPire salon : {4}".format(numb,round(count/numb,3),result[0]["Count"],result[len(result)//2]["Count"],result[len(result)-1]["Count"]),
        "Freq":"Heures actives : {0}\nMoyenne messages par heure : {1}\nMeilleure heure : {2}\nMédiane : {3}\nPire heure : {4}".format(numb,round(count/numb,3),result[0]["Count"],result[len(result)//2]["Count"],result[len(result)-1]["Count"]),
    }
    return dictBloc[option]