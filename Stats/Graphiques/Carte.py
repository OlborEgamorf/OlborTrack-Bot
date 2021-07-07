### CODE OBSOLETE

import pandas as pd
from matplotlib import pyplot as plt

try:
    from mpl_toolkits.basemap import Basemap
except:
    pass

dictConfidence={10:"< 0.25 km",9:"< 0.5 km",8:"< 1 km",7:"< 5 km",6:"< 7.5 km",5:"< 10 km",4:"< 15 km",3:"< 20 km",2:"< 25 km",1:"+ de 25km ",0:"Incalculable"}

def graphMap(lat,lon,table,option):
    dictTitres={"iss":"Position actuelle de l'ISS","geosearch":"Recherche géographique"}
    data = pd.DataFrame({'lon':[lon],'lat':[lat],'name':['ISS']})
    if option=="iss":
        m=Basemap(llcrnrlon=-180, llcrnrlat=-80,urcrnrlon=180,urcrnrlat=80)
    else:
        leftlowLON=[-166,-100,-24,-18,91,36,28,-180]
        leftlowLAT=[6,-58,33,-36,-48,5,41,-80]
        rightupLON=[-55,-30,41,53,180,149,180,180]
        rightupLAT=[71,15,75,38,9,58,85,80]
        for i in range(8):
            lon1,lat1,lon2,lat2=leftlowLON[i],leftlowLAT[i],rightupLON[i],rightupLAT[i]
            if lon>=lon1 and lon<=lon2 and lat>=lat1 and lat<=lat2:
                break
        m=Basemap(llcrnrlon=lon1, llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
    m.drawcoastlines(linewidth=0.1, color="white")
    m.drawcountries(color="white")
    m.drawmapboundary()

    m.plot(data['lon'], data['lat'], linestyle='none', marker="h", markersize=14, alpha=0.6, c="orange", markeredgecolor="black", markeredgewidth=1)
    if len(table["results"])>0:
        plt.xlabel("Type : "+table["results"][0]["components"]["_category"]+" - "+table["results"][0]["components"]["_type"]+"\n"+table["results"][0]["formatted"]+"\nPrécision : "+dictConfidence[table["results"][0]["confidence"]],fontsize=12)
    plt.title(dictTitres[option],fontsize=12)
    plt.tight_layout()
    plt.savefig("CSV/Graphs/map.png")
    plt.clf()
    return "CSV/Graphs/map.png"