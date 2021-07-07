import wikipediaapi
import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.AuteurIcon import auteur

async def embedWikiSearch(args,pageF):
    lang,descip="fr",""
    search=await webRequest("https://fr.wikipedia.org/w/api.php?action=opensearch&search="+args+"&limit=1&namespace=0&format=json")
    assert search!=False, "Il y a eu une erreur lors de la recherche de la page."
    if search[1]==[]:                
        lang="en"
        search=await webRequest("https://en.wikipedia.org/w/api.php?action=opensearch&search="+args+"&limit=1&namespace=0&format=json")
        assert search!=False, "Il y a eu une erreur lors de la recherche de la page."
    assert search[1]!=[], "Cette page n'existe pas."
    search=search[1][0]
    wik=wikipediaapi.Wikipedia(lang)
    page=wik.page(search)
    id=page.pageid
    if pageF==1:
        if len(page.summary)>500:
            descip=page.summary[0:500]+"..."
        else:
            descip=page.summary
        descip+="\n[Lien]("+page.fullurl+")"
    else:
        h,titre=0,""
        for i in page.sections:
            h+=1
            for k in i.title.split(" "):
                titre+=k
            if len(descip)+len(str(h)+". ["+i.title+"]("+page.fullurl+"#"+titre)<2048:
                descip+=str(h)+". ["+i.title+"]("+page.fullurl+"#"+titre+")\n"
        if len(descip)>=2048:
            descip=descip[0:2048]
    embedW=discord.Embed(title=page.title, description=descip, color=0xfcfcfc)
    try:
        image=await webRequest("https://"+lang+".wikipedia.org/w/api.php?action=query&titles="+search+"&prop=pageimages&format=json&pithumbsize=400")
        embedW.set_thumbnail(url=image["query"]["pages"][str(id)]["thumbnail"]["source"])
    except:
        pass
    embedW.set_footer(text="Page "+str(pageF)+"/2 - OT!wikipedia")
    embedW=auteur(page.fullurl,0,0,embedW,"wp")
    return embedW