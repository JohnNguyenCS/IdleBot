import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load Token From .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Basic Intents
intents = discord.Intents.default()
intents.message_content = True  # Allows Bot To See Command Messages
intents.voice_states = True # Change 1 

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
bot.remove_command("help")  # Remove Default Help Command

LOG_CHANNEL_ID = # Change 2 / Testing

last_voice_channel_id: dict[int, int] = {} # Change 3 Remembers The Last Voice Channel
manual_disconnect_guilds: set[int] = set() # Change 4 Tracks Manual Disconnects
reconnect_tasks: dict[int, asyncio.Task] = {} # Change 5 Manages Reconnect Tasks

# Change 6 Logging Function
async def log_debug(message: str):
    print(message)
    if LOG_CHANNEL_ID:
        ch = bot.get_channel(LOG_CHANNEL_ID)
        if ch:
            try:
                await ch.send(message)
            except Exception as e:
                print(f"[LOG_CHANNEL send failed] {type(e).__name__}: {e}")

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

    last_voice_channel_id[ctx.guild.id] = voice_channel.id # Change 7 Store Last Channel
    manual_disconnect_guilds.discard(ctx.guild.id) # Change 8 Joining Resets Manual Disconnect

    # Move Locations If Already Connected
    if ctx.voice_client:
        if ctx.voice_client.channel == voice_channel:
            return await ctx.reply(f"Already in **{voice_channel.name}**.")
        else:
            await ctx.voice_client.move_to(voice_channel)
            return await ctx.reply(f"Moved to **{voice_channel.name}**.")
    else:
        # CHANGE 9 reconnect=True helps discord.py handle brief drops better
        await voice_channel.connect(reconnect=True)
        return await ctx.reply(f"Joined **{voice_channel.name}**.")


@bot.command(name="leave")
async def leave(ctx: commands.Context):
    """Leaves The Voice Channel"""
    if ctx.voice_client:
        manual_disconnect_guilds.add(ctx.guild.id) # Change 10 Mark As Manual Leave (no auto-rejoin)
        await ctx.voice_client.disconnect()
        return await ctx.reply("Disconnected.")
# Change 11: When Leaving VC, Log + Attempt Reconnect (Unless Manual Leave)
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if not bot.user or member.id != bot.user.id:
        return

    # Bot Disconnected From Voice
    if before.channel is not None and after.channel is None:
        guild_id = member.guild.id
        await log_debug(f"🔌 Bot left VC in **{member.guild.name}** (was: **{before.channel.name}**)")

        # If You Used The Leave Command, Do Nothing
        if guild_id in manual_disconnect_guilds:
            await log_debug("🛑 Manual leave detected — not reconnecting.")
            return

        # Start A Reconnect Attempt (Cancel Old Task If Any)
        old_task = reconnect_tasks.get(guild_id)
        if old_task and not old_task.done():
            old_task.cancel()

        reconnect_tasks[guild_id] = asyncio.create_task(reconnect_loop(member.guild))

# ----------------------------------------------------------
# Change 12: Minimal Reconnect Loop 
async def reconnect_loop(guild: discord.Guild):
    guild_id = guild.id
    channel_id = last_voice_channel_id.get(guild_id)

    if not channel_id:
        await log_debug(f"⚠️ No saved VC for **{guild.name}**. Use `join` once.")
        return

    for attempt in range(1, 7):  # ~6 Tries
        try:
            channel = guild.get_channel(channel_id)
            if channel is None:
                await log_debug(f"⚠️ Saved VC not found in **{guild.name}**.")
                return

            await log_debug(f"🔁 Reconnect attempt {attempt} → **{guild.name}** / **{channel.name}**")
            await channel.connect(reconnect=True)
            await log_debug(f"✅ Reconnected to **{channel.name}** in **{guild.name}**")
            return
        except Exception as e:
            await log_debug(f"⚠️ Reconnect failed ({type(e).__name__}): {e}")
            await asyncio.sleep(5)

    await log_debug(f"❌ Gave up reconnecting in **{guild.name}** after multiple attempts.")
# ----------------------------------------------------------

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

