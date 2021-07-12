import geopandas as gpd
import geoplot
import geoplot.crs as gcrs
from Core.Fonctions.GraphTheme import setThemeGraph
from matplotlib import pyplot as plt

dictConfidence={10:"< 0.25 km",9:"< 0.5 km",8:"< 1 km",7:"< 5 km",6:"< 7.5 km",5:"< 10 km",4:"< 15 km",3:"< 20 km",2:"< 25 km",1:"+ de 25km ",0:"Incalculable"}

def graphMap(table):
    setThemeGraph(plt)
    data=gpd.read_file("GeoJson/World.geo.json")
    data2=gpd.read_file("GeoJson/iss.geo.json")
    ax=geoplot.pointplot(data2,projection=gcrs.WebMercator())
    #geoplot.polyplot(data, edgecolor='darkgrey', facecolor='lightgrey', linewidth=.3, ax=ax)
    geoplot.webmap(data, projection=gcrs.WebMercator(),ax=ax)
    
    plt.xlabel("Type : "+table["results"][0]["components"]["_category"]+" - "+table["results"][0]["components"]["_type"]+"\n"+table["results"][0]["formatted"]+"\nPrécision : "+dictConfidence[table["results"][0]["confidence"]],fontsize=12)
    plt.title("Position actuelle de l'ISS\nType : {0} - {1}\n{2}\nPrécision : {3}".format(table["results"][0]["components"]["_category"],table["results"][0]["components"]["_type"],table["results"][0]["formatted"],dictConfidence[table["results"][0]["confidence"]]),fontsize=12)

    plt.tight_layout()
    plt.savefig("Graphs/map.png")
    plt.clf()
