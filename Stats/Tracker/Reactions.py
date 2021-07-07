from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeObj
from Stats.Tracker.Divers import exeDiversSQL
from Stats.SQL.Verification import verifExecSQL

async def exeReactClient(option,message,react,user,guild):
    if verifExecSQL(guild,message.channel,user)==False or bool(guild.mstats[3]["Statut"])==False:
        return
    exeDiversSQL(user.id,{"Réactions":1},option,guild,None,None)
    if react.id not in (772766034376523776,772766034335236127,772766034558058506,717710058548625479,717710058460282980,717710058213081150,717710058422796319,717710058258956309,717710058200367176,717710058452156416,786595775118704690,772766034356076584,772766033996021761,772766034163400715,705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206,800024049535025162,800024049401069598,800023868756197376,800023868659335168,833666016491864114,833736320919797780):
        if len(react.name)==1:
            exeReactionsSQL(user.id,ord(react.name),1,guild,option)
        elif react.id==None:
            pass
        else:
            exeReactionsSQL(user.id,react.id,1,guild,option)
    return

def exeReactionsSQL(id,emote,count,guild,option):
    connexionGuild,curseurGuild=connectSQL(guild.id,"Guild","Guild",None,None)
    if option!="+":
        count=-count
    exeClassic(count,emote,"Reactions",curseurGuild,guild)
    exeObj(count,emote,id,True,guild,"Reactions")
    connexionGuild.commit()