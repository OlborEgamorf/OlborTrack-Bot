import asyncio

async def attenteParty(game,temps,event):
    time,done=0,False
    while time!=temps and not done:
        await asyncio.sleep(0.5)
        if event in ("speed","speedfinal"):
            count=len(game.reponses)
        else:
            done=True
        for j in game.reponses:
            if event=="speed" or event=="speedfinal":
                if game.reponses[j]!=None and game.reponses[j]==game.vrai-1:
                    done=True
                elif game.reponses[j]==None:
                    count-=1
            else:
                if game.reponses[j]==None:
                    done=False
        if event in ("speed","speedfinal"):
            if count==len(game.reponses):
                done=True
        time+=0.5

async def attente(game):
    time,done=0,False
    while time!=20 and not done:
        await asyncio.sleep(0.5)
        done=True
        for j in game.reponses:
            if game.reponses[j]==None:
                done=False
        time+=1