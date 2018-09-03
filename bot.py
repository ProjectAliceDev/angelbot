import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
import os
import random
import json
import urllib.request

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print("Running")
    await bot.change_presence(game=discord.Game(name='Doki Doki: The Angel Returns'))
    for channel in member.server.channels:
        if channel.name == 'general' or channel.name == 'breakroom':
            await bot.send_message(channel, "Hi, guys! I'm just getting everything warmed up here, ehehe~!")
    

@bot.event
async def on_member_join(member: discord.Member):
    for channel in member.server.channels:
        if channel.name == 'general' or channel.name == 'breakroom':
            await bot.send_message(channel, "Welcome to my studio, \@{}!".format(member.name))


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("STAHP IT!")

    
@bot.command(pass_context=True)
async def get_release(ctx):
    with urllib.request.urlopen('https://theangelreturns.aliceos.app/release.json') as release_json:
        release_data = json.loads(release_json.read().decode())
        await bot.say("The latest release is `" + release_data["beta.build"] + "`")


@bot.command(pass_context=True)
async def cuddle(ctx):
    possible_responses = ["Uhh, I don't know if that works here...", "Ooh, can Eugene join us? :elephant:", "I-I don't know, no one's, uh, really cuddled with me before...", "Ehehe~"]
    await bot.say(random.choice(possible_responses))


@bot.command(pass_context=True)
async def ask(ctx, question):
    if question == "Are you okay?" or question == "How are you?" or question == "Are you alright?":
        possible_responses = ["I'm doing fine, I guess...", "Well, I'd be fine if Mio _wasn't_ having her mood swing right now!", "Why are you asking me this?", "Horrible, actually. What even is reality?", "Well, I'm doing better than yesterday.", "Stop looking for rainclouds. I don't tolerate them on my server!"]
    elif "depression" in question or "rainclouds" in question or "depressed" in question:
        possible_responses = ["Get these rainclouds out of here, baka!", "_No rainclouds in the server_ :PissedAngel:", "I always want this place to be a safe haven."]
    elif "Gman" in question or "Freeman" in question or "Half-Life" in question or "Alyx" in question:
        possible_responses = ["Prepare for unforseen consequences.", "_This is where I get off..._", "Yeah, when _is_ Half-Life 3 coming out, anyway?", "Okay, so maybe I'm tikering around with the Source engine and making  Half-Life fan game. So what?", "Rise and smell the ashes...", "Can we not talk about this? Please?"]
    elif "Monika" in question or "biggest fan" in question or "fan" in question:
        possible_responses = ["Well, I certainly never expected for Monika to like me so much...", "It's both Monika and TZKU that like me. A lot.", "The fan situation's a bit complicated, ehehe~"]
    elif "Where's Boris?" in question:
        possible_responses = ["https://cdn.discordapp.com/attachments/481922610742165514/482312409831309315/Alice_Maymay_2.png "]
    elif "qt" in question or "You're a Qt" in question or "Qt" in question or "you" and "qt" in question:
        possible_responses = ["I NIOT QT!"]
    else:
        possible_responses = ["What the hell are you saying?", "Uh, I know I know programming and all, but I don't understand your question...", "Are you even speaking English?", "Sorry, I don't understand.", ":Uwaa:", "I may be an AI now, but that doesn't mean I've properly implanted myself into Discord. Please understand that I would be more than happy to answer your questions, it's just that I can't properly express them here."]
    await bot.say(random.choice(possible_responses))

bot.run(os.environ.get('BOT_KEY'))
