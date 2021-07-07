from time import strftime

"""tempStyle="seaborn-darkgrid"
def setThemeGraph(plt):
    global tempStyle
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        if tempStyle!="seaborn-darkgrid":
            from matplotlib import pyplot as plt
            tempStyle="seaborn-darkgrid"
        plt.style.use("seaborn-darkgrid")
    else:
        if tempStyle!="dark_background":
            from matplotlib import pyplot as plt
            tempStyle="dark_background"
        plt.style.use("dark_background")"""

def setThemeGraph(plt):
    """Change le thème du graphique en fonction de s'il fait nuit ou jour"""
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        plt.style.use("seaborn-darkgrid")
    else:
        plt.style.use("dark_background")