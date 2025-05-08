import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "hello" in message.content.lower():
        await message.channel.send(f'Hello {message.author.name}!')

# Slash command
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

# Running the bot with the token from the environment variable
bot.run(token, log_handler=handler, log_level=logging.DEBUG)