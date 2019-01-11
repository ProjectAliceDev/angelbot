#########################################################
# Angelbot                                              #
# The Alice Angel bot of HYPERDEATH                     #
#########################################################
import os
from asriel.soul import *
from angeldiscord.discord import *
from matrix.matrix import *
from multiprocessing import Process

# Run each part of Angelbot in a thread. This allows for Angelbot
# to work simultaneously.
p1 = Process(target=client.listen_forever)
p1.start()

p2 = Process(target=bot.run(os.environ.get('BOT_KEY')))
p2.start()
