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


def fill_with_determination():
    '''
    Trains the AI with given data.
    '''
    print("Filling Alice with DETERMINATION...")
    determination.train("chatterbot.corpus.english")
    determination.train(determination_set)
    print("Done.")


def talk_callback(room, event):
    '''
    Sends a message.
    '''
    message = (event['content']['body']).replace("Alice Angel (Bot): ", "")
    room.send_text(str(determination.get_response(message)))

def upload_emoji(emote_name):
    '''
    Upload an emoji to Matrix.
    '''
    try:
        with open("emotes/" + emote_name + ".png", 'rb') as f:
            imgdata = f.read()
        data_url = client.upload(imgdata, 'image/png')
        room.send_image(data_url, emote_name + '.png')
    except Exception as e:
        room.send_text("It looks like I can't do that... Error Info: " + str(e))

def emoji_callback(room, event):
    '''
    Send an emoji
    '''
    args = event['content']['body'].split()
    upload_emoji(args[1])
    
def handle_invite(room_id, state):
    """This function handles new invites to Matrix rooms by accepting them.
    :param room_id: Matrix room is
    :param state: State of the Matrix room
    """
    room = client.join_room(room_id)
    room.add_listener(handle_message)
    
def handle_message(room, event):
    """This function handles incoming matrix events and reacts on the keyword xkcd.
    :param room: Matrix room where message event occurred
    :param event: Matrix event of the message
    """
    # Make sure we didn't send this message ourselves
    print(event)
    if "@" + matrix_username in event['sender']:
        return
    try:
        if not event['content']['msgtype'] == 'm.text':
            print('No text message, ignoring...')
            return
        text = event['content']['body']
    except KeyError:
        print('Cannot handle that request')
        return
    print('Received: %s' % text)
    if text.startswith('!emote'):
        emoji_callback(room, event)
    elif text.startswith("Alice Angel (Bot):"):
        talk_callback(room, event)

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

client = MatrixClient(matrix_server)
client.login_with_password(matrix_username, matrix_password)
client.add_invite_listener(handle_invite)
for _, room in client.get_rooms().items():
    room.add_listener(handle_message)
client.start_listener_thread()
while True:
    input()
