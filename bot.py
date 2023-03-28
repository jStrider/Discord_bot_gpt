import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
from discord import Intents




# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
specific_channel_id = int(os.getenv("CHANNEL"))
#OPENAI
openai.organization = os.getenv("OPENAI_ORGID")
openai.api_key = os.getenv("OPENAI_TOKEN")
init_prompt = os.getenv("INIT_PROMPT")


# Créer un objet Intents avec les intents par défaut
intents = Intents.default()
intents.message_content=True


# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix="!",intents=intents)

# Define the 'hello' command
@bot.command()
async def pickup(ctx, *, text: str):

    if ctx.channel.id == specific_channel_id:
        gpt_result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=150,
        messages=[
            {"role" : "system", "content":init_prompt},
            {"role" : "user", "content" : text}
        ] 

    )

    await ctx.channel.send(gpt_result.choices[0].message.content.strip())
  
# # Afficher un message lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user} est connecté à Discord !")

# Démarrer le bot
bot.run(TOKEN)
