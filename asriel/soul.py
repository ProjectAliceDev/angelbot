from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

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

def fill_with_determination():
    '''
    Trains the AI with given data.
    '''
    print("Filling Alice with DETERMINATION...")
    determination.train("chatterbot.corpus.english")
    determination.train(determination_set)
    print("Done.")