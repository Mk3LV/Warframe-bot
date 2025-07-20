import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.command()
async def verify(ctx, *, ign):
    guild = ctx.guild
    member = ctx.author
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
        await ctx.send("Missing permissions to change nickname or roles.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found.")
