from time import strftime

def setThemeGraph(plt):
    """Change le thème du graphique en fonction de s'il fait nuit ou jour"""
    plt.rcdefaults()
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        plt.style.use("seaborn-darkgrid")
        return "light"
    else:
        plt.style.use("dark_background")
        return "dark"