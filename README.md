# Discord_bot_gpt

## about the poroject 

This is a fun project of a discord bot using gpt3 to make answers for seducing purposes, 
it has only 2 commands for now :

### PICKUP

`/pickup  <context>`

It write for you the best line you need to break the ice with that girl on the middle of the dancefloor, the one you are too shy too approach because, you know "i hae nothing to say ..." (what a stupid excuse) Now you will have something to say and, oh god, it will be  the best pickup line she ever eard. I promise you gonna seduce her so hard that if she had a boyfriend, she will leave him for you.

for example you can write : 

`/pickup she is on the middle of the dancefloor with a red shirt`

and you will get the pickup line you needed.

### CHAT

`/chat <chat history>`

I know its not that easy to have a nice conversation with a girl you like so I added this command, it is supposed to write down an answer for the last message you got from that "Marie", "Julie" or anyone else.
You can try to put the entiere conversation chat with a typo like :

HER: BLA BLA BLA

ME: BLA BLA BLA

HER: BLA BLA BLA

and it will gitve u the best seductive answer you need for continue the conversation.


### Install

for now its only doplyed on testpypi.

well, as I host my own instance of this bot, this is how you can install it with simples step :

 ### STEP 1

`pip install -i https://test.pypi.org/simple/ jrw-discord-bot`

That's it. no Step 2

I'm joking, there is a step 2 :

### STEP 2

### Defines envrionnements variables

There is a few envrionnement variables that is used for the bot, i could do a good menu for you to put thoses confidentials informations in it but... you know... BEHHHH

```
JRW_DISCORD_TOKEN=
JRW_CHANNEL=
JRW_OPENAI_TOKEN=
JRW_OPENAI_ORGID=
```

Optionnal environnements variable :

#### JRW_CONFIG_PATH

default value : /etc/botgpt/config.yml

you can put te config file in a different folder if you want to.

I recommand you to make a .jrwbot in your home directory and to source it from your .bashrc, .profile or anything else.

You need to create a developper account on DISCORD and to make an account on openai to get thoses token but internet is better than me at explaining that.


### configuration file

it's a simple yml file that contain simple configuration about the comands (mainly text for now)

```
---
FR:
  commands:
    pickup:
      description:  "donne moi le contexte et je t'ecris ma meilleur disquette ;)"
    chat:
      description:  "envoi ici le dernier message de ton crush on l'historique de conversation, j'y répondrais pour toi"
  prompts:
    init_prompt_pickup: "tu es un coach en séduction, professionnel du domaines depuis de nombreuses années, tu sais ce qu'il faut dire pour séduire une femme et dans cet objectif, tu me donnera une phrase d'acroche originale et drole à chaque fois que je te parlerai en utilisant au maximum le contexte de ma phrase. tu ne dois me répondre rien d'autre que par 3 propositions de phrase d'accroche, chaque proposition commencera pas : proposition <numéro de la proposition> :"
    init_prompt_chat_seduction: |
      a partir de maintenant, tu interprete 'MOI' et toutes tes réponse commencent par 'MOI:',
      tu es un homme et je suis une femme. 
      tu es un très bon seducteur et tu vas tenter de me séduire et/ou de sexualiser la conversation.
      Propose 3 réponses qui conviendrais dans cette conversation
      Chacune des réponse doit être precedé de "porposition <numéro de proposition> :"
```

I hope in the fture to put there more powerfull options
### coommands

commands.description are used to show the command description.

when you type /pickup in discord, there is a small text => that's it

### prompts

prompts are the text that is send to pre-init the openai GPT for each of the command and the given context.

### Start the bot

Once the steps above are done, you can start the bot : 

`python3 -m jrw-discord-bot`

Don't forget to credit me the day you will have to do the "how I met your mother" time with your kids