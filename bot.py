import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required to manage nicknames and roles

bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')  # Get token from environment variable

@bot.event
async def on_ready():
    from discord import __version__
    print(f'📦 Discord library version: {__version__}')
    print(f'✅ Bot is ready as {bot.user}')

@bot.command()
async def verify(ctx, *, ign):
    guild = ctx.guild
    member = ctx.author

    # These should exactly match your role names
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
        await ctx.send("⚠️ I don't have permission to change your nickname or roles.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: DISCORD_TOKEN environment variable not found. Please add it to Secrets.")
