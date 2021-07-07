import wikiquote
from random import choice
import discord
from Core.Fonctions.AuteurIcon import auteur

async def embedWikiQuote(args):
    lang="fr"
    search=wikiquote.search(args,lang="fr")
    if search==[]:                
        lang="en"
        search=wikiquote.search(args)
    assert search!=[], "Cette page n'existe pas."
    quote=choice(wikiquote.quotes(search[0],lang=lang))
    embedW=discord.Embed(title=search[0],description=quote,color=0xfcfcfc)
    embedW.set_footer(text="OT!wikiquote")
    link=""
    for i in search[0].split(" "):
        link+=i+"_"
    embedW=auteur("https://"+lang+".wikiquote.org/wiki/"+link[0:len(link)-1],0,0,embedW,"wp")
    return embedW

async def embedWikiQOTD():
    search=wikiquote.qotd(lang="fr")
    embedW=discord.Embed(title=search[1],description=search[0],color=0xfcfcfc)
    embedW.set_footer(text="OT!wikiquote")
    link=""
    for i in search[1].split(" "):
        link+=i+"_"
    embedW=auteur("https://fr.wikiquote.org/wiki/"+link[0:len(link)-1],0,0,embedW,"wp")
    return embedW