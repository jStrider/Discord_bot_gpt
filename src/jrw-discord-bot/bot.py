import os
import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from discord import Intents
import openai
from dotenv import load_dotenv
import yaml



class jrw_bot:
    
    def __init__(self):
        self.discordtoken = ""
        self.specific_channel_id = 0
        self.pickup_description = ""
        self.init_prompt_pickup = ""
        self.chat_description = ""
        self.init_prompt_chat_seduction = ""

    async def get_gpt_answer_to_prompt(interaction: discord.Interaction, prompt: str, context: str):
        gpt_result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=150,
        messages=[
            {"role" : "system", "content" : prompt},
            {"role" : "user", "content" : context}
        ]
        )
        response=gpt_result.choices[0].message.content.strip()
        await interaction.edit_original_response(content=f'{response}')

    def load_config(self):
        # load env variables
        load_dotenv()
        # Chargement des variables d'environnement
        # Discord
        config_env_not_set=False
        self.discordtoken = os.environ.get("JRW_DISCORD_TOKEN")
        self.specific_channel_id = int(os.environ.get("JRW_CHANNEL"))
        # OpenAI
        openai.api_key = os.environ.get("JRW_OPENAI_TOKEN")
        openai.organization = os.environ.get("JRW_OPENAI_ORGID")
        config_env_not_set=False
        if self.discordtoken == None:
            print("JRW_DISCORD_TOKEN not set")
            config_env_not_set=True
        if self.specific_channel_id == None:
            print("JRW_CHANNEL not set")
            config_env_not_set=True
        if openai.api_key == None:
            print("JRW_OPENAI_TOKEN not set")
            config_env_not_set=True
        if openai.organization == None:
            print("JRW_OPENAI_ORGID not set")
            config_env_not_set=True

        if config_env_not_set:
            print("Please set the environment variables")
            exit(1)
        # Get the absolute path to the current directory
        current_dir = os.path.abspath(os.path.dirname(__file__))

        # Construct the absolute file path to the config file
        config_file_path = os.path.join(current_dir, "config.yml")
        # Read the YAML file
        with open(config_file_path, "r") as file:
            config = yaml.safe_load(file)

        # Access the values in the YAML file
        self.pickup_description = config["FR"]["commands"]["pickup"]["description"]
        self.init_prompt_pickup = config["FR"]["prompts"]["init_prompt_pickup"]
        self.chat_description = config["FR"]["commands"]["chat"]["description"]
        self.init_prompt_chat_seduction = config["FR"]["prompts"]["init_prompt_chat_seduction"]



        
    def init_bot(self):
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
        # gen a pickup line with context
        @bot.tree.command(name="pickup")
        @app_commands.describe(pickup_context = self.pickup_description)
        async def pickup(interaction: discord.Interaction, pickup_context: str):
            await interaction.response.send_message(f"chargement de la meilleure phrase d'accroche possible avec le contexte donné : {pickup_context}")
            gpt_result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=150,
            messages=[
            {"role" : "system", "content" : self.init_prompt_pickup},
            {"role" : "user", "content" : pickup_context}
            ]
            )
            response=gpt_result.choices[0].message.content.strip()
            await interaction.edit_original_response(content=f'{response}')

        @bot.tree.command(name="chat")
        @app_commands.describe(chat_context = self.chat_description)
        async def chat(interaction: discord.Interaction, chat_context: str):
                if  interaction.channel_id == self.specific_channel_id:
                    await interaction.response.send_message(f"chargement de la meilleure réponse possible avec le contexte donné : {chat_context}")
                    task = asyncio.create_task(sendAsyncMessage(interaction,chat_context))
                    gpt_result = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens=150,
                    messages=[
                        {"role" : "system", "content" : self.init_prompt_chat_seduction},
                        {"role" : "user", "content" : prompt}
                    ]
                    )
                    response=interaction.response.send_message(gpt_result.choices[0].message.content.strip())
                    await interaction.edit_original_response(content=f'{response}')
        # Démarrer le bot
        bot.run(self.discordtoken)
        

