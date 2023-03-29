import os
import discord
from discord import app_commands
from discord.ext import commands
import openai
from dotenv import load_dotenv
from discord import Intents

# Chargement des variables d'environnement
load_dotenv()
#Discord
TOKEN = os.getenv("DISCORD_TOKEN")
specific_channel_id = int(os.getenv("CHANNEL"))
#OpenAI
openai.organization = os.getenv("OPENAI_ORGID")
openai.api_key = os.getenv("OPENAI_TOKEN")
init_prompt_pickup = os.getenv("INIT_PROMPT_PICKUP")
init_prompt_chat_seduction = os.getenv("INIT_PROMPT_CHAT_SEDUCTION")
if TOKEN == None:
    print("discord undefined token")
if openai.api_key == None:
    print("openai undefined token")

# Créer un objet Intents avec les intents par défaut
intents = Intents.default()
intents.message_content=True


# On initialise le bot avec le prefixe de comande 
bot = commands.Bot(command_prefix="!",intents=intents)

# # Afficher un message lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user} est connecté à Discord !")
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


#gen a pickup line with context
@bot.tree.command(name="pickup")
@app_commands.describe(pickup_context = "donne moi le contexte et je t'ecris ma meilleur disquette ;)")
async def pickup(interaction: discord.Interaction, pickup_context: str):
        if  interaction.channel_id == specific_channel_id:
            gpt_result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=150,
            messages=[
                {"role" : "system", "content" : init_prompt_pickup},
                {"role" : "user", "content" : pickup_context}
            ]     
            )
            await interaction.response.send_message(gpt_result.choices[0].message.content.strip())

@bot.tree.command(name="chat")
@app_commands.describe(chat_context = "envoi ici le dernier message de ton crush on l'historique de conversation, j'y répondrais pour toi")
async def pickup(interaction: discord.Interaction, chat_context: str):
        if  interaction.channel_id == specific_channel_id:
            gpt_result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=150,
            messages=[
                {"role" : "system", "content" : init_prompt_chat_seduction},
                {"role" : "user", "content" : chat_context}
            ]     
            )
            await interaction.response.send_message(gpt_result.choices[0].message.content.strip())


# Démarrer le bot
bot.run(TOKEN)
