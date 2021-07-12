from time import strftime
from random import choice

def setThemeGraph(plt):
    """Change le thème du graphique en fonction de s'il fait nuit ou jour"""
    plt.rcdefaults()
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        plt.style.use("seaborn-darkgrid")
    else:
        plt.style.use("dark_background")