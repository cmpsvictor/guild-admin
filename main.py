import discord
import logging
from dotenv import load_dotenv


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# dotenv
load_dotenv()
TOKEN = os.getenv('discord_token')
GUILD = os.getenv('discord_guild')

# Intents setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
   
# Events functions

@client.event
async def on_ready():
    # Startup prints the following:
    print(f'The following channels have {client.user} currently in them:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    channelName = message.guild
    
    # Saves the users with privileges in the guild
    validUsers = []
    for guild in client.guilds:
        for member in guild.members:
            for role in member.roles:
                if role.name == 'Admin': # Insert according to desired privileged user roles
                    validUsers.append(member.discriminator)
    
    # Parsing user name to print message
    if message.author.nick != None:
        nick = message.author.nick
    else:
        nick = message.author.name

    # Answering user messages
    if message.content == ".help":
        await message.channel.send(
        f'\n.users - Lists the amount of users in {channelName}\n' \
        '.mute - Mutes everyone within the user\'s voice channel\n' \
        '.unmute - Unmutes everyone within the user\'s voice channel\n' \
        '.help - Prints this usage screen'
        )
    

    if message.content == ".users":
        await message.channel.send(f'Number of users in {channelName} = {channelName.member_count}\n')
    

    elif message.content == ".mute":
        if message.author.discriminator in validUsers:
            if message.author.voice == None:
                await message.channel.send(f'{nick}, you\'re not currently in a voice channel!')
                return
            voiceChannel = message.author.voice.channel
            for member in voiceChannel.members:
                await member.edit(mute=True)
            await message.channel.send(f'{nick} has muted {voiceChannel}!')
        else:
            await message.channel.send(f'Since when do I take orders from you?')
    

    elif message.content == ".unmute":
        if message.author.discriminator in validUsers:
            if message.author.voice == None:
                await message.channel.send(f'{nick}, you\'re not currently in a voice channel!')
                return
            voiceChannel = message.author.voice.channel
            for member in voiceChannel.members:
                await member.edit(mute=False)
            await message.channel.send(f'{nick} has unmuted {voiceChannel}!')
        else:
            await message.channel.send(f'You lack the required privileges to use this command.')
 

client.run(TOKEN)



