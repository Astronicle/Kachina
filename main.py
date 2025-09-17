import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from flask import Flask         #import Flask to create a web server
import threading                #import threading to run Flask in a separate thread
import json
from datetime import timedelta #for timer functionality
from character_scrape import guide



# Load environment variables from .env file
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')




# Flask app setup
app = Flask(__name__)

# Flask to provide a web server for the bot
@app.route('/')
def index():
    return "Kachina Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 4000))  
    app.run(host="0.0.0.0", port=port, threaded=True)

# Start Flask in a background thread
threading.Thread(target=run_flask).start()




# Enabling Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Using the commands extension to create a bot instance
bot = commands.Bot(command_prefix='!', intents = intents)





# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    try:
        synced = await bot.tree.sync()  # Syncing commands to Discord
        print(f"Synced {len(synced)} application command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    commands = await bot.tree.fetch_commands()
    print(f"Registered commands: {[command.name for command in commands]}")





# Importing the message replies from the message_replies.json file
with open('message_replies.json', 'r') as file:
    data = json.load(file)





# Prefix commands
@bot.command(name="ping", help="Check the bot's latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! {latency}ms')

@bot.command(name="info", help="Get information about the bot")
async def info(ctx):
    info_message = (
        f"Bot Name: {bot.user.name}\n"
        f"Bot ID: {bot.user.id}\n"
        f"Bot Latency: {round(bot.latency * 1000)}ms\n"
        f"Prefix: {bot.command_prefix}"
    )
    await ctx.send(info_message)

@bot.command(name="character", help="Get character guide for specified Genshin character")
async def character(ctx, *, name: str):
    url = guide(name)
    await ctx.send(f"Character: {name}\nGuide: {url}")

@bot.command(name="code", help="Get the Genshin code redeem link")
async def code(ctx, *, code: str):
    code_url = f"https://genshin.hoyoverse.com/en/gift?code={code}"
    await ctx.send(code_url)

@bot.command(name="pfp", help="Get the profile picture of a user by their ID")
async def pfp(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    if user:
        embed = discord.Embed(title=f"{user.name}'s Profile Picture", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found.")

@bot.command(name="say", help="Send a message to a specific channel")
async def say(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        await ctx.send(f"Message sent to {channel.mention}")
    else:
        await ctx.send("Channel not found.")

# command to set timer by acceprting a time and pinging the user when the time is up. accepts time in days, hours, minutes, and seconds
@bot.command(name="timer", help="Set a timer for a specified duration")
async def timer(ctx, duration: str):
    try:
        # Parse the duration string
        time_parts = duration.split(':')
        if len(time_parts) == 4:  # days:hours:minutes:seconds
            days, hours, minutes, seconds = map(int, time_parts)
        elif len(time_parts) == 3:  # hours:minutes:seconds
            days, hours, minutes, seconds = 0, *map(int, time_parts)
        elif len(time_parts) == 2:  # minutes:seconds
            days, hours, minutes, seconds = 0, 0, *map(int, time_parts)
        elif len(time_parts) == 1:  # seconds
            days, hours, minutes, seconds = 0, 0, 0, int(time_parts[0])
        else:
            await ctx.send("Invalid duration format. Use 'days:hours:minutes:seconds' or 'hours:minutes:seconds' or 'minutes:seconds' or 'seconds'.")
            return

        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        if total_seconds <= 0:
            await ctx.send("Please provide a positive duration.")
            return

        await ctx.send(f"Timer set for {duration}. I will ping you when the time is up!")

        await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=total_seconds))
        await ctx.send(f"{ctx.author.mention}, your timer for {duration} is up!")
    except Exception as e:
        await ctx.send(f"An error occurred while setting the timer: {e}")


# Dictionary to store the previous presence status of users
previous_presence = {}

@bot.event
async def on_presence_update(before, after):
    user_to_track = 552000406281125889  # Replace with actual user ID

    if after.id != user_to_track:
        return

    if after.bot:
        return

    channel_id = 1417741299573985320
    channel = bot.get_channel(channel_id)

    if not channel:
        return

    previous_status = previous_presence.get(after.id, 'offline')
    current_status = str(after.status)

    if previous_status == 'offline' and current_status in ['online', 'idle', 'dnd']:
        embed = discord.Embed(
            title="User Online",
            description=f"{after.mention} is now online!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=after.avatar.url if after.avatar else discord.Embed.Empty)
        embed.set_footer(text=f"User ID: {after.id}")
        await channel.send(embed=embed)

    elif previous_status in ['online', 'idle', 'dnd'] and current_status == 'offline':
        embed = discord.Embed(
            title="User Offline",
            description=f"{after.mention} has gone offline.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=after.avatar.url if after.avatar else discord.Embed.Empty)
        embed.set_footer(text=f"User ID: {after.id}")
        await channel.send(embed=embed)

    previous_presence[after.id] = current_status





# message event to respond to specific messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # ensuring that commands work

    # Respond with an embed to "I'm new here"
    if message.content.lower() in ["i'm new here", "im new here", "im new", "new here"]:
        embed = discord.Embed(
            title="🎉 Welcome!",
            description="We're glad you're here! Feel free to ask questions or just hang out. 😊",
            color=discord.Color.green()
        )
        embed.set_footer(text="Welcome Bot • Kachina")
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else discord.Embed.Empty)
        await message.channel.send(embed=embed)
        return  # Optional: skip JSON replies for this message
    
    if message.content.lower() in ["wuv you"]:
        embed = discord.Embed(
            title="wuv",
            description="you too",
            color=discord.Color.green()
        )
        embed.set_footer(text="a lot...")
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else discord.Embed.Empty)
        await message.channel.send(embed=embed)
        return  # Optional: skip JSON replies for this message

    # Check for message replies in message_replies.json
    for key, value in data.items():
        if key in message.content.lower():
            await message.channel.send(eval(f"f'{value}'"))
            break
            



# Slash commands
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")



# Running the bot with the token from the environment variable
bot.run(token)
