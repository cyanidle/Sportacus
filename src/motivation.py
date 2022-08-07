import hikari

async def motivation(event: hikari.GuildMessageCreateEvent):
    if event.content.startswith("Спортакус, дай мне мотивацию"):
        await event.message.respond("Fuck you!")