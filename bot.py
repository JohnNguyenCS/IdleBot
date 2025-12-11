import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load Token From .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Basic Intents
intents = discord.Intents.default()
intents.message_content = True  # Allows Bot To See Command Messages

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
bot.remove_command("help")  # Remove Default Help Command

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    # "Lament" Status
    activity = discord.Activity(type=discord.ActivityType.playing, name="lament")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command(name="join")
async def join(ctx: commands.Context):
    """Joins The Voice Channel"""
    # User In Voice Channel First
    if not ctx.author.voice or not ctx.author.voice.channel:
        return

    voice_channel = ctx.author.voice.channel

    # Move Locations If Already Connected
    if ctx.voice_client:
        if ctx.voice_client.channel == voice_channel:
            return
        else:
            await ctx.voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect()


@bot.command(name="leave")
async def leave(ctx: commands.Context):
    """Leaves The Voice Channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command(name="help")
async def help_command(ctx: commands.Context):
    """All Available Commands."""

    embed = discord.Embed(
        title="Available Commands",
        description="You Called?\n\nWhy Would Anyone Want... *Sigh* Forget It, It's Not My Concern.",
        color=0x5865F2  
    )

    embed.add_field(
        name="`@dj xiao join`",
        value="Hello!",
        inline=False
    )
    embed.add_field(
        name="`@dj xiao leave`",
        value="Bye Bye!",
        inline=False
    )
    embed.add_field(
        name="`@dj xiao help`",
        value="For All Commands!",
        inline=False
    )

    embed.set_footer(text="DJ Xiao • 2025")

    await ctx.send(embed=embed)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not found in .env")
    bot.run(TOKEN)
