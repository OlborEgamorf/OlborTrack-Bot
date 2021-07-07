import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.Divers3 import lignesEmbed
from Core.Fonctions.AuteurIcon import auteur

async def embedMALlist(user,genre,key,page):
    descip=""
    table=await webRequest("https://api.jikan.moe/v3/user/"+user.lower()+"/"+genre.lower()+"list/"+key.lower())
    assert table!=False, "Je ne trouve pas cet utilisateur ou cette catégorie !"

    generation=lignesEmbed(15,table[genre],page)
    debut,borne,pageT=generation[0],generation[1],generation[2]

    for i in range(debut,borne):
        descip+="["+table[genre.lower()][i]["title"]+"]("+table[genre.lower()][i]["url"]+") "
        if key.lower()!="ptr" and key.lower()!="ptw":
            if genre.lower()=="anime":
                descip+="("+str(table[genre.lower()][i]["watched_episodes"])+" ép regardés/"+str(table["anime"][i]["total_episodes"])+")\n"
            else:
                descip+="("+str(table[genre.lower()][i]["read_chapters"])+" chap lus/"+str(table["manga"][i]["total_chapters"])+")\n"
        else:
            descip+="\n"
    embedMAL=discord.Embed(title="Liste de {0} - {1}, {2}".format(user,genre.lower(),key), description=descip, color=0x7c0cb0)
    embedMAL.set_footer(text="Page "+str(page+1)+"/"+str(pageT)+" | OT!mallist")
    embedMAL=auteur(0,0,0,embedMAL,"mal")
    return embedMAL,pageT