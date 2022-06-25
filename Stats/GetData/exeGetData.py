from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.OTGuild import OTGuild
from Stats.GetData.GetData import newGetData


@OTCommand
async def exeGetData(ctx,bot,args,guildOT):
    if len(args)!=0 and args[0]=="start":
        assert ctx.guild.get_member(699728606493933650).guild_permissions.read_message_history,"Je ne peux pas récupérer vos anciennes stats sans avoir la permission 'read_message_history'..."
        bot.loop.create_task(newGetData(ctx.message.guild,ctx.message.channel,bot,guildOT))
    else:
        embed=createEmbed("GetData - Avertissement","La procédure Olbor Track GetData analyse tous les messages du serveur de tous les salons que le bot peut voir, pour générer toutes les tables de statistiques qui seront utilisées dans les commandes.\nLes messages des autres bots sont ignorés.\nAvant toute chose, il va supprimer toutes les données déjà récoltées, pour repartir sur de nouvelles bases. Vous ne pourrez exécuter aucune commande pendant.\nVous pouvez continuer à parler et gérer votre serveur pendant l'opération. Il est juste déconseillé de retirer des permissions au bot avant la fin. Les messages envoyés pendant ne sont pas comptés dans les statistiques.\nNe pensez pas que le bot a planté, si c'est le cas vous le verrez.\nPour lancer la procédure, faites **OT!getdata start**.\nCe sera peut-être long.\nMerci me m'avoir lu.",0x220cc9,"getdata",bot.user)
        await ctx.channel.send(embed=embed)
