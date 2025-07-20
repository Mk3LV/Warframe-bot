import os
import discord
from discord.ext import commands

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for nicknames and roles

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Get the bot token from Render environment variables
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")


@bot.command()
async def verify(ctx, *, ign: str):
    """Verifies a user by setting nickname and roles."""
    guild = ctx.guild
    member = ctx.author

    # Role names must exactly match your server
    unverified_role = discord.utils.get(guild.roles, name="🚫 Unverified")
    verified_role = discord.utils.get(guild.roles, name="✅ Verified")

    try:
        await member.edit(nick=ign)

        if unverified_role in member.roles:
            await member.remove_roles(unverified_role)

        if verified_role not in member.roles:
            await member.add_roles(verified_role)

        await ctx.send(f"✅ {member.mention}, you've been verified as `{ign}`!")

    except discord.Forbidden:
        await ctx.send("⚠️ I don't have permission to change your nickname or roles.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN environment variable not found.")
