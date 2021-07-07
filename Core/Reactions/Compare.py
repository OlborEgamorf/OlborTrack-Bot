### TOTALEMENT OBSOLETE

from Core.Reactions.Outils import removeReact, embedE
import discord

async def reactCompare(message,user):
    if message.embeds[0].footer.text.split(" ")[0]!="OT!compare":
        return
    id, bas, compare = message.embeds[0].author.icon_url.split("/")[4], message.embeds[0].footer.text, False
    user1=user.guild.get_member(int(id))
    dictMode={"messages":"M","mots":"W","freq":"F","chan":"C","voice":"V","trivia":"T"}
    if user.id==int(id):
        await removeReact(message,772766033996021761,user)
    elif message.embeds[0].footer.icon_url==discord.Embed.Empty:
        compare=True
    elif message.embeds[0].footer.icon_url.split("/")[4]==str(user.id):
        compare=True
    else:
        await removeReact(message,772766033996021761,user)
    if compare==True:
        embedC=embedCompare(id,user.id,dictMode[bas.split(" ")[1]],0,user.guild.id,user1.color.value,user1.name,user.name,user1.avatar,user.avatar)
        await message.edit(embed=embedC)
        try:
            await message.clear_reactions()
        except discord.errors.Forbidden:
            await message.channel.send(embed=embedE,delete_after=8)
        if embedC.footer.text=="Avertissement":
            return
        if embedC.footer.text.split(" ")[3]!="1":
            try:
                await message.add_reaction("<:otGAUCHE:772766034335236127>")
                await message.add_reaction("<:otDROITE:772766034376523776>")
            except discord.errors.Forbidden:
                embedP=discord.Embed(title="<:otRED:718392916061716481> Permission manquante", description="Cette commande fonctionne avec des réactions ! Vous ne pourrez pas tout voir si vous ne me donnez pas la permission 'ajout de réactions'...",color=0xff0000)
                embedP.set_footer(text="Permission")
                await message.channel.send(embed=embedP,delete_after=8)
    return