import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.setMaxPage import bornesReport
from Core.Fonctions.Embeds import embedAssert
from Core.Fonctions.AuteurIcon import auteur

async def embedMALuser(user,page):
    table=await webRequest("https://api.jikan.moe/v3/user/"+user.lower()+"/profile")
    assert table!=False, "Je ne trouve pas cet utilisateur ou cette catégorie !"
    if len(table["about"])>1000:
        table["about"]=table["about"][0:1000]+"..."
    embedMAL=discord.Embed(url=table["url"],description="**"+str(table["about"])+"**",color=0x7c0cb0)
    if table["image_url"]!=None:
        embedMAL.set_thumbnail(url=table["image_url"])
    if page==0:
        listeArgs=["completed","episodes_watched","days_watched","mean_score","watching","on_hold","plan_to_watch"]
        listeTitres=["Animes terminés","Episodes vus","Jours vus","Score moyen","En cours","En suspens","A regarder"]
        for i in range(7):
            if table["anime_stats"][listeArgs[i]]!=0:
                embedMAL.add_field(name=listeTitres[i], value=str(table["anime_stats"][listeArgs[i]]),inline=True)
        if embedMAL.fields==discord.Embed.Empty:
            page+=1
        embedMAL.title=table["username"]+" - Animes"
    if page==1:
        listeArgs=["completed","chapters_read","days_read","mean_score","reading","on_hold","plan_to_read"]
        listeTitres=["Mangas terminés","Chapitres lus","Jours lus","Score moyen","En cours","En suspens","A regarder"]
        for i in range(7):
            if table["manga_stats"][listeArgs[i]]!=0:
                embedMAL.add_field(name=listeTitres[i], value=str(table["manga_stats"][listeArgs[i]]),inline=True)
        if embedMAL.fields==discord.Embed.Empty:
            page+=1
        embedMAL.title=table["username"]+" - Mangas"
    if page==2:
        listeArgs=["Anime","Manga"]
        for k in range(2):
            borne=bornesReport(table["favorites"][listeArgs[k].lower()],8)
            descip=""
            for i in range(borne):
                descip+="["+table["favorites"][listeArgs[k].lower()][i]["name"]+"]("+table["favorites"][listeArgs[k].lower()][i]["url"]+")\n"
            if borne!=0:
                embedMAL.add_field(name=listeArgs[k]+" favoris", value=descip,inline=False)
        if embedMAL.fields==discord.Embed.Empty:
            return embedAssert("Cette page est vide !")
        embedMAL.title=table["username"]+" - Favoris"
    pagef=0
    if table["anime_stats"]["completed"]!=0 or table["anime_stats"]["episodes_watched"]!=0 or table["anime_stats"]["days_watched"]!=0 or table["anime_stats"]["mean_score"]!=0 or table["anime_stats"]["watching"]!=0 or table["anime_stats"]["on_hold"]!=0 or table["anime_stats"]["plan_to_watch"]!=0:
        pagef+=1
    if table["manga_stats"]["completed"]!=0 or table["manga_stats"]["chapters_read"]!=0 or table["manga_stats"]["days_read"]!=0 or table["manga_stats"]["mean_score"]!=0 or table["manga_stats"]["reading"]!=0 or table["manga_stats"]["on_hold"]!=0 or table["manga_stats"]["plan_to_read"]!=0:
        pagef+=1
    if len(table["favorites"]["manga"])!=0 or len(table["favorites"]["anime"])!=0:
        pagef+=1
    embedMAL.set_footer(text="Page "+str(page+1)+"/"+str(pagef))
    embedMAL=auteur(0,0,0,embedMAL,"mal")
    return embedMAL,pagef