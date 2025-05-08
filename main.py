import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from flask import Flask         #import Flask to create a web server
import threading                #import threading to run Flask in a separate thread

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


# Prefix commands
@bot.command(name="ping", help="Check the bot's latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! {latency}ms')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "hello" in message.content.lower():
        await message.channel.send(f'Hello {message.author.name}!')
    if "matcalc" in message.content.lower():
        await message.channel.send(f'https://material-calculator-for-genshin-impact.vercel.app/')
    if "syllixa" in message.content.lower():
        await message.channel.send(f'<@1199779674620952687> onee chan!')
    if "fuck" in message.content.lower():
        await message.channel.send(f'no cursing smh')
    if "owned" in message.content.lower():
        await message.channel.send(f'lol owned')
    # if "ping" in message.content.lower():
    #     await message.channel.send(f'pong')
    

# Slash commands
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

# Running the bot with the token from the environment variable
bot.run(token)