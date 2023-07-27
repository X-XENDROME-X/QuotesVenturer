
import discord
from discord.ext import commands
import requests
import random

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_random_quote():
    response = requests.get('https://zenquotes.io/api/random')  
    if response.status_code == 200:
        quotes = response.json()
        random_quote = random.choice(quotes)
        return random_quote['q']  
    else:
        return 'Failed to fetch a quote'

@bot.command()
async def quote(ctx):
    """Get a random quote."""
    random_quote = get_random_quote()
    await ctx.send(random_quote)

@bot.command()
async def hello(ctx):
    """Greet the user with a hello message."""
    await ctx.send("Hello :)")

command_explanations = {
    "quote": "Get a random quote.",
    "hello": "Greet the user with a hello message.",
    "help": "Get a list of available commands and their functionalities."
}

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help_embed = discord.Embed(title="QuoteVenturer Commands", color=0x00ff00)
        for cog, commands_list in mapping.items():
            command_signatures = [f"**!{command.name}**: {command_explanations.get(command.name, 'No description.')}" for command in commands_list]
            if command_signatures:
                cog_name = cog.qualified_name if cog else "No Category"
                command_list = "\n".join(command_signatures)
                help_embed.add_field(name=cog_name, value=command_list, inline=False)
        destination = self.get_destination()
        await destination.send(embed=help_embed)

bot.help_command = CustomHelpCommand()

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    welcome_message = f"Welcome to the server, {member.mention}! Enjoy some random quotes!"
    await channel.send(welcome_message)

@bot.event
async def on_ready():
    print("Hello! I am QuoteVenturer, ask me some quotes.")
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! I am QuoteVenturer, ask me some quotes.")

bot.run(BOT_TOKEN)
