import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.AuteurIcon import auteur

async def embedMALsearch(genre,search,page):
    descipS,descipG="",""
    table=await webRequest("https://api.jikan.moe/v3/search/"+genre.lower()+"?q="+search.lower()+"&page=1")
    table=await webRequest("https://api.jikan.moe/v3/"+genre.lower()+"/"+str(table["results"][page]["mal_id"])+"/")
    assert table!=False, "Je ne trouve rien !"
    if len(table["synopsis"])>1000:
        table["synopsis"]=table["synopsis"][0:1000]+"..."
    embedMAL=discord.Embed(description=table["synopsis"],url=table["url"],title=table["title"],color=0x7c0cb0)
    embedMAL.add_field(name="Type", value=table["type"],inline=True)
    embedMAL.add_field(name="Rank", value=str(table["rank"])+" ("+str(table["score"])+")",inline=True)
    for i in table["genres"]:
        descipG+="["+i["name"]+"]("+i["url"]+")\n"
    try:
        embedMAL.set_thumbnail(url=table["image_url"])
    except:
        pass
    if genre.lower()=="anime":
        
        embedMAL.add_field(name="Episodes", value=table["episodes"],inline=True)
        embedMAL.add_field(name="Durée", value=table["duration"],inline=True)
        for i in table["studios"]:
            descipS+="["+i["name"]+"]("+i["url"]+")\n"
        embedMAL.add_field(name="Studios", value=descipS,inline=True)
        embedMAL.add_field(name="Genres",value=descipG, inline=True)
        embedMAL.add_field(name="Diffusion", value=table["aired"]["string"],inline=False)
        
    else:
        for i in table["authors"]:
            descipS+="["+i["name"]+"]("+i["url"]+")\n"
        embedMAL.add_field(name="Auteurs", value=descipS,inline=True)
        embedMAL.add_field(name="Chapitres", value=table["chapters"],inline=True)
        embedMAL.add_field(name="Genres",value=descipG, inline=True)
        embedMAL.add_field(name="Date", value=table["published"]["string"],inline=True)
    embedMAL.set_footer(text="Page "+str(page+1)+"/"+str(10)+" | OT!malsearch "+genre+" "+search)
    embedMAL=auteur(0,0,0,embedMAL,"mal")
    return embedMAL,10