from Core.Fonctions.WebRequest import webRequest
from Stats.Graphiques.Carte import graphMap
import json
from Core.OS.Keys3 import opencageKey

async def embedGeoSearch(arg,option) -> (str, str):
    """Renvoie la carte d'un lieu donné en argument ou alors de la position actuelle de l'ISS, en fonction de la commande demandée.
    
    Renvoie l'image et un texte pour la commande, qui représente les coordonnées géographiques."""
    if option=="iss":
        tableLieu=await webRequest("http://api.open-notify.org/iss-now.json")
        arg=str(tableLieu["iss_position"]["latitude"])+" "+str(tableLieu["iss_position"]["longitude"])
    table=await webRequest("https://api.opencagedata.com/geocode/v1/json?key="+opencageKey+"&language=fr&limit=1&q="+arg)
    assert len(table["results"])>0 and table!=False, "Je n'ai rien trouvé !"
    with open("JSON/"+str(table["results"][0]["geometry"]["lat"])+str(table["results"][0]["geometry"]["lng"])+".txt","w") as outfile:
        json.dump(table,outfile)
    image=graphMap(float(table["results"][0]["geometry"]["lat"]),float(table["results"][0]["geometry"]["lng"]),table,option)
    try:
        contenu=table["results"][0]["annotations"]["flag"]+" "+str(table["results"][0]["geometry"]["lat"])+" "+str(table["results"][0]["geometry"]["lng"])
    except:
        contenu=":map: "+str(table["results"][0]["geometry"]["lat"])+" "+str(table["results"][0]["geometry"]["lng"])
    return image,contenu