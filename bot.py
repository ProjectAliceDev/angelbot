#########################################################
# Angelbot                                              #
# The Alice Angel bot of HYPERDEATH                     #
#########################################################
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
import os
import random
import json
from urllib.request import Request, urlopen
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from matrix_client.client import MatrixClient

matrix_username = os.environ.get(('MATRIX_USERNAME'))
matrix_password = os.environ.get(('MATRIX_PASSWORD'))
matrix_server = "https://matrix.org"

# Create basic chatbot
determination = ChatBot("Alice Angel")
determination.set_trainer(ListTrainer)

# Create an array from chats.txt
determination_set = []

with open('chats.txt', 'r') as f:
    for line in f:
        line_strip = line.strip()
        if not line_strip.startswith("#"):
            determination_set.append(line_strip)

# Create the Discord bot.
bot = commands.Bot(command_prefix="$")
bot.remove_command('help')
possible_games = [
    "Doki Doki: The Angel Returns",
    "Minecraft",
    "Doki Doki Literature Club!",
    "Half-Life 3",
    "with Eugene",
    "Undertale",
    "DELTARUNE"
]

'''
Trains the AI with given data.
'''
def fill_with_determination():
    print("Filling Alice with DETERMINATION...")
    determination.train("chatterbot.corpus.english")
    determination.train(determination_set)
    print("Done.")
    
    
'''
Upload an emoji to Matrix.
'''
def upload_emoji(emote_name):
    with open("emotes/" + emote_name + ".png", 'rb') as f:
        imgdata = f.read()
    data_url = client.upload(imgdata, 'image/png')
    room.send_image(data_url, emote_name + '.png')

bbot'''
Send an emoji
'''
def emoji_callback(room, event):
    args = event['content']['body'].split()
    upload_emoji(args[1])

@bot.event
async def on_ready():
    print("Running...")
    print("Press Ctrl+C to quit anytime.")
    fill_with_determination()
    game_name = random.choice(possible_games)
    if game_name == possible_games[0]:
        await bot.change_presence(game=discord.Game(name=possible_games[0]), status='dnd')
    else:
        await bot.change_presence(game=discord.Game(name=game_name))


@bot.event
async def on_member_join(member: discord.Member):
    for channel in member.server.channels:
        if channel.name == 'general' or channel.name == 'breakroom':
            await bot.send_message(channel, "Welcome to my studio, {}!".format(member.mention))


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        color=0xf9c440
    )
    embed.set_author(
        name="Alice Angel Help Service",
        icon_url="https://cdn.discordapp.com/app-icons/474592037988204556/4288eaa321797be8b09df8e68e4542cf.png?size=512"
    )

    embed.add_field(name="$ping", value="Pings me", inline=False)
    embed.add_field(name="$get_release", value="Get the latest nightly release information.", inline=False)
    embed.add_field(name="$cuddle", value="Lets you cuddle with me :heart:", inline=False)
    embed.add_field(name="$talk", value="Lets you communicate with me such as questions, statements, compliments...", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def ping(ctx):
    possible_responses = [
        "STAHP IT!",
        "This isn't funny!",
        "Please stop.",
        "Uwaaa~!",
        "I don't like this!",
        "Halp!",
        "`ping error`"
    ]
    await bot.say(random.choice(possible_responses))

    
@bot.command(pass_context=True)
async def get_release(ctx):
    try:
        release_request = Request('https://raw.githubusercontent.com/TheAngelReturns/campbell/master/release.json')
        release_request.add_header('User-Agent', "Magic Browser")
        release_data = json.loads(urlopen(release_request).read().decode())

        base_url = "https://github.com/TheAngelReturns/the-angel-returns/releases/tag/"

        embed = discord.Embed(
            color=0xf9c440
        )

        embed.set_author(
            name="Nightly Information Release Service",
            icon_url="https://raw.githubusercontent.com/TheAngelReturns/the-angel-returns/nightly/game/mod_assets/logo.png"
        )

        embed.add_field(
            name="Build Number (Git Commit Hash)",
            value=release_data["beta"]["build"],
            inline=False
        )

        embed.add_field(
            name="Download Link",
            value=base_url + release_data["beta"]["build"],
            inline=False
        )

        await bot.say(embed=embed)

    except Exception as e:
        await bot.say("Umm, something's not working.\nUmm, creators, what does this mean: " + str(e) + "?")


@bot.command(pass_context=True)
async def cuddle(ctx):
    possible_responses = [
        "Uhh, I don't know if that works here...",
        "Ooh, can Eugene join us? :elephant:",
        "I-I don't know, no one's, uh, really cuddled with me before...",
        "Ehehe~"
    ]
    await bot.say(random.choice(possible_responses))


@bot.command(pass_context=True)
async def liven_chat(ctx):
    await bot.say(":pineapple:")

@bot.command(pass_context=True)
async def talk(ctx, statement):
    await bot.say(determination.get_response(statement))

# Run the bot. This needs the environment key BOT_KEY to run!
# This is set through Heroku usually, but can also work for
# regular servers. Go to https://discordapp.com/developers/ to
# create your bot key.
bot.run(os.environ.get('BOT_KEY'))
