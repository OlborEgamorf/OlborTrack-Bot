async def seekMessage(bot,payload):
    try:
        message=(await bot.get_channel(payload.channel_id).fetch_message(payload.message_id))
        if payload.member==None:
            user=bot.get_user(payload.user_id)
        else:
            user=payload.member
    except:
        try:
            user=bot.get_user(payload.user_id)
            message=(await user.fetch_message(payload.message_id))
        except:
            return None, None
    if user.bot:
        return None,None
    return message, user