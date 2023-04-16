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
        self.command_pickup_description = ""
        self.command_pickup_openai_prompt = ""
        self.command_chat_description = ""
        self.command_chat_openai_prompt = ""
        self.config_file_path = "/data/config.yml"

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
        
        env_config_path=os.environ.get("JRW_CONFIG_PATH")
        print("env_config_path : " + str(env_config_path))
        if env_config_path != None:
            print("is non None env_config_path : " + str(env_config_path))
            self.config_file_path = env_config_path
        print(" now " + self.config_file_path + " is the config file path")
        self.load_config_file()
        # Construct the absolute file path to the config file

    def load_config_file(self):
        
        # Read the YAML file
        with open(self.config_file_path, "r") as file:
            config = yaml.safe_load(file)

        # Access the values in the YAML file

        # commands
        ## pickup
        self.command_pickup_description = config["FR"]["commands"]["pickup"]["description"]
        self.command_pickup_openai_prompt = config["FR"]["commands"]["pickup"]["openai"]["prompt"]
        self.command_pickup_openai_model = config["FR"]["commands"]["pickup"]["openai"]["model"]
        self.command_pickup_openai_max_tokens = config["FR"]["commands"]["pickup"]["openai"]["max_tokens"]
        ## chat
        self.command_chat_description = config["FR"]["commands"]["chat"]["description"]
        self.command_chat_openai_prompt = config["FR"]["commands"]["chat"]["openai"]["prompt"]
        self.command_chat_openai_model = config["FR"]["commands"]["chat"]["openai"]["model"]
        self.command_chat_openai_max_tokens = config["FR"]["commands"]["chat"]["openai"]["max_tokens"]

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
            print(f"test : Version: 0.1.2")
            try:
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
            except Exception as e:
                print(e)
        # gen a pickup line with context
        @bot.tree.command(name="pickup")
        @app_commands.describe(pickup_context = self.command_pickup_description)
        async def pickup(interaction: discord.Interaction, pickup_context: str):
            if  interaction.channel_id == self.specific_channel_id:
                await interaction.response.send_message(f"chargement de la meilleure phrase d'accroche possible avec le contexte donné : {pickup_context}")
                self.load_config_file()
                gpt_result = openai.ChatCompletion.create(
                model=self.command_pickup_openai_model,
                max_tokens=self.command_pickup_openai_max_tokens,
                messages=[
                {"role" : "system", "content" : self.command_pickup_openai_prompt},
                {"role" : "user", "content" : pickup_context}
                ]
                )
                response=gpt_result.choices[0].message.content.strip()
                await interaction.edit_original_response(content=f'contexte : \n  {pickup_context} \n \n  réponses : \n{response}')

        @bot.tree.command(name="chat")
        @app_commands.describe(chat_context = self.command_chat_description)
        async def chat(interaction: discord.Interaction, chat_context: str):
            if  interaction.channel_id == self.specific_channel_id:
                await interaction.response.send_message(f"chargement de la meilleure réponse possible avec le contexte donné : {chat_context}")
                self.load_config_file()
                gpt_result = openai.ChatCompletion.create(
                model=self.command_chat_openai_model,
                max_tokens=self.command_pickup_openai_max_tokens,
                messages=[
                    {"role" : "system", "content" : self.command_chat_openai_prompt},
                    {"role" : "user", "content" : chat_context}
                ]
                )
                response=gpt_result.choices[0].message.content.strip()
                await interaction.edit_original_response(content=f'contexte : \n  {chat_context} \n \n  réponses : \n {response}')
        # Démarrer le bot
        bot.run(self.discordtoken)
        

