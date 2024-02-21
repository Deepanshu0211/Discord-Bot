import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

# Discord bot token (replace 'YOUR_TOKEN' with your actual bot token)
TOKEN = ''

# Define intents
intents = discord.Intents.default()

# Discord client
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

# Function to generate a random code
def generate_code():
    import random
    import string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=18))
    return f'discord.gift/{code}'

# Function to fetch a random meme from the API
def get_meme():
    import requests
    response = requests.get('https://meme-api.com/gimme')
    data = response.json()
    return data['url']

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name='with balls'))

# Slash command to send a random meme
@slash.slash(name="meme",
             description="Get a random meme")
async def meme(ctx: SlashContext):
    meme_url = get_meme()
    await ctx.send(meme_url)

# Slash command to generate codes
@slash.slash(name="code",
             description="Generate gift codes",
             options=[
                 {
                     "name": "quantity",
                     "description": "Number of codes to generate",
                     "type": 4,
                     "required": True
                 }
             ])
async def generate_codes(ctx: SlashContext, quantity: int):
    # Get the channel where the user wants to send the codes
    channel = ctx.channel

    # Generate and send codes
    for _ in range(quantity):
        code = generate_code()
        await channel.send(code)

    await ctx.send(f'Successfully sent {quantity} codes to {channel.mention}')

# Slash command for help
@slash.slash(name="help",
             description="Get bot help")
async def help_command(ctx: SlashContext):
    embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())

    embed.add_field(name="/meme", value="Get a random meme", inline=False)
    embed.add_field(name="/code [quantity]", value="Generate gift codes", inline=False)
   

    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
