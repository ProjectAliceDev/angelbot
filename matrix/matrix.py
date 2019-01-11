import asyncio
import chalk
import os
import random
import json
from urllib.request import Request, urlopen
from matrix_client.client import MatrixClient
from asriel.soul import *

matrix_username = os.environ.get(('MATRIX_USERNAME'))
matrix_token = os.environ.get(('MATRIX_TOKEN'))
matrix_server = "https://matrix.org"

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


def emoji_list_callback(room, event):
    '''
    List all emojis
    '''
    message = "Current Emojis: ["
    for root, dirs, files in os.walk("emotes"):
        for file in files:
            message += file.replace(".png", "") + ", "
    message += "]"
    room.send_text(message)

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
    # Make sure we didn't send this message ourselves
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
    elif text.startswith('!listemoji'):
        emoji_list_callback(room, event)
    elif text.startswith("Alice Angel (Bot):"):
        talk_callback(room, event)

client = MatrixClient(matrix_server, token=matrix_token, user_id="@"+matrix_username+":matrix.org")
client.add_invite_listener(handle_invite)
for _, room in client.get_rooms().items():
    room.add_listener(handle_message)