import os
import discord
from dotenv import load_dotenv
from discord import Intents

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
specific_channel_id = int(os.getenv("CHANNEL"))

# Créer un objet Intents avec les intents par défaut
intents = Intents.default()
intents.message_content=True

# Initialiser le client Discord
client = discord.Client(intents=intents)

# Définir l'événement pour les messages reçus
@client.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == client.user:
        return

    print(f"Message reçu de {message.author} dans le canal {message.channel.id}: {message.content}")  # Ajouter un message de débogage

    # Répondre dans le canal spécifique
    if message.channel.id == specific_channel_id:
        print("bon message dans le bon channel")
        await message.channel.send("Bonjour !")
        print(message.content)
        if message.content.lower().startswith("bonjour"):  # Modification de la condition
            await message.channel.send("Bonjour !")

# Afficher un message lorsque le bot est prêt
@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !")

# Démarrer le bot
client.run(TOKEN)
