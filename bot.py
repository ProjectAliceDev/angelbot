import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
import os
import random
import json
from urllib.request import Request, urlopen

bot = commands.Bot(command_prefix="$")
bot.remove_command('help')
possible_games = [
    "Doki Doki: The Angel Returns",
    "Minecraft",
    "Doki Doki Literature Club!",
    "Half-Life 3",
    "with Eugene"
]


@bot.event
async def on_ready():
    print("Running...")
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
async def ask(ctx, question):
    await bot.say("`$ask has been deprecated. Please use $talk instead.`")


@bot.command(pass_context=True)
async def talk(ctx, statement):
    # TODO: Use responses.json instead of hard-coding the answers in.
    if statement == "Are you okay?" or statement == "How are you?" or statement == "Are you alright?":
        possible_responses = [
            "I'm doing fine, I guess...",
            "Well, I'd be fine if Mio _wasn't_ having her mood swing right now!",
            "Why are you asking me this?",
            "Horrible, actually. What even is reality?",
            "Well, I'm doing better than yesterday.",
            "Stop looking for rainclouds. I don't tolerate them on my server!"
        ]

    elif "depression" in statement or "rainclouds" in statement or "depressed" in statement:
        possible_responses = [
            "Get these rainclouds out of here, baka!",
            "_No rainclouds in the server_ :angry:",
            "I always want this place to be a safe haven."
        ]

    elif "Gman" in statement or "Freeman" in statement or "Half-Life" in statement or "Alyx" in statement:
        possible_responses = [
            "Prepare for unforseen consequences.",
            "_This is where I get off..._",
            "Yeah, when _is_ Half-Life 3 coming out, anyway?",
            "Okay, so maybe I'm tinkering around with the Source engine and making a Half-Life fan game. So what?",
            "Rise and smell the ashes...",
            "Can we not talk about this? Please?"
        ]

    elif "Monika" in statement or "biggest fan" in statement or "fan" in statement:
        possible_responses = [
            "Well, I certainly never expected for Monika to like me so much...",
            "It's both Monika and TZKU that like me. A lot.",
            "The fan situation's a bit complicated, ehehe~",
            "I have many fans..."
        ]

    elif "Where's Boris?" in statement:
        possible_responses = [
            "https://cdn.discordapp.com/attachments/481922610742165514/482312409831309315/Alice_Maymay_2.png ",
            "Hippity hoppity, your Boris is now my property. That's how it goes, right?\nBut seriously, though, I have no clue.",
            ":shrug:",
            "W-why are you asking me?",
            "Not here, not there, not anywhere to my knowledge!",
            "Boris out, Eugene in!"
        ]

    elif "qt" in statement or "You're a Qt" in statement or "Qt" in statement or "you" and "qt" in statement:
        possible_responses = [
            "I NIOT QT!",
            "NO\nBAKA",
            "No. Eugene more Qt than me.",
            "no u"
        ]

    elif "Who's Eugene?" in statement:
        possible_responses = [
            "Silly, Eugene's my stuffed mastodon!",
            ":elephant:",
            "B-but I thought you knew... :pensive:",
            "What, am I not allowed to have stuffed animals or something?",
            "He's the _cutest_ little stuffed mastodon!",
            "My cuddle buddy. .^_~"
        ]

    else:
        possible_responses = [
            "Sorry, I don't understand.",
            "Uwaa~!",
            "Sadly, I'm not as complete as you think. It'll take some time before I can answer all of your questions.",
            "E-Eh?",
            "Are you talking to me or to Eugene?"
        ]
    await bot.say(random.choice(possible_responses))

bot.run(os.environ.get('BOT_KEY'))
