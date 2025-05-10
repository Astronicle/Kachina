import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from flask import Flask         #import Flask to create a web server
import threading                #import threading to run Flask in a separate thread
import json
import time # to manage cooldowns
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

# Using the commands extension to create a bot instance
bot = commands.Bot(command_prefix='!', intents = intents)

cooldowns = {} # Dictionary to store cooldowns for each channel





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

@bot.command()
async def character(ctx, *, name: str):
    url = guide(name)
    await ctx.send(f"Character: {name}\nGuide: {url}")




# message event to respond to specific messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # ensuring that commands work

    # cooldown per channel (10 seconds)
    now = time.time()
    cooldown = 10  # seconds
    last_sent = cooldowns.get(message.channel.id, 0)

    if now - last_sent < cooldown:
        return  #skipped

    for key, value in data.items():
        if key in message.content.lower():
            await message.channel.send(eval(f"f'{value}'"))
            cooldowns[message.channel.id] = now
            break
    





# Slash commands
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

# Running the bot with the token from the environment variable
bot.run(token)