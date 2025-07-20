import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # Needed to manage nicknames and roles

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def verify(ctx, ign: str):
    guild = ctx.guild
    member = ctx.author

    # Fetch roles
    verified_role = discord.utils.get(guild.roles, name="Verified")
    unverified_role = discord.utils.get(guild.roles, name="Unverified")

    # Change nickname
    try:
        await member.edit(nick=ign)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change your nickname.")
        return

    # Assign and remove roles
    if verified_role:
        await member.add_roles(verified_role)
    else:
        await ctx.send("❌ 'Verified' role not found.")

    if unverified_role:
        await member.remove_roles(unverified_role)

    await ctx.send(f"✅ You have been verified as `{ign}`!")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
