import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed to manage nicknames and roles

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def verify(ctx, *, ign):
    guild = ctx.guild
    member = ctx.author

    # These roles must exist on your server
    unverified_role = discord.utils.get(guild.roles, name="🚫 Unverified")
    verified_role = discord.utils.get(guild.roles, name="✅ Verified")

    try:
        await member.edit(nick=ign)
        if unverified_role in member.roles:
            await member.remove_roles(unverified_role)
        if verified_role not in member.roles:
            await member.add_roles(verified_role)
        await ctx.send(f"{member.mention}, you've been verified as `{ign}`!")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change your nickname or roles.")
    except Exception as e:
        await ctx.send(f"Something went wrong: {str(e)}")

# Run bot using token from environment
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("DISCORD_TOKEN not found in environment variables.")