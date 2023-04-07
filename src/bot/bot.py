import os
import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from discord import Intents
import openai
from dotenv import load_dotenv
import yaml
# Chargement des variables d'environnement
load_dotenv()
#Discord
TOKEN = os.getenv("DISCORD_TOKEN")
specific_channel_id = int(os.getenv("CHANNEL"))
#OpenAI
openai.organization = os.getenv("OPENAI_ORGID")
openai.api_key = os.getenv("OPENAI_TOKEN")

# Chargement de la configuration
# Read the YAML file
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Access the values in the YAML file
init_prompt_pickup = config["prompt"]["init_prompt_pickup"]
init_prompt_chat_seduction = config["prompt"]["init_prompt_chat_seduction"]

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
            try:
                print(gpt_result.choices[0].message.content)
                await interaction.response.send_message(str(gpt_result.choices[0].message.content))
            except Exception as e:
                print(e)

@bot.tree.command(name="chat")
@app_commands.describe(chat_context = "envoi ici le dernier message de ton crush on l'historique de conversation, j'y répondrais pour toi")
async def chat(interaction: discord.Interaction, chat_context: str):
        if  interaction.channel_id == specific_channel_id:
            await interaction.response.send_message("loading an answer...")
            task = asyncio.create_task(sendAsyncMessage(interaction,chat_context))

@bot.tree.command(name="info")
#@app_commands.describe("tu verras les prompts que j'utilise pour generer mes réponses")
async def info(interaction: discord.Interaction):
        if  interaction.channel_id == specific_channel_id:
            await interaction.response.send_message(f"""Voici les prompts utilisés :  

        **pour la phrase d'accroche :** 
            
            {init_prompt_pickup}

        **pour la réponse au chat :**
                
            {init_prompt_chat_seduction}
            
            """)

async def sendAsyncMessage(interaction: discord.Interaction, prompt: str ):
    gpt_result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=150,
    messages=[
        {"role" : "system", "content" : init_prompt_chat_seduction},
        {"role" : "user", "content" : prompt}
    ]     
    )
    await interaction.response.send_message(gpt_result.choices[0].message.content.strip())
# Démarrer le bot
bot.run(TOKEN)
