async def unpin(message):
    try:
        await message.unpin()
    except:
        pass

async def pin(message):
    try:
        await message.pin()
    except:
        pass