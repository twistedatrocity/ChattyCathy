# ChattyCathy
Artificial intelligence (AI) chat bot for Discord written in Python

# Project Home Page

Visit the project page on DevDungeon.com for more information.

https://www.devdungeon.com/content/chatty-cathy

# AIML Tutorial

For more details on using AIML with Python, see the tutorial on DevDungeon.

https://www.devdungeon.com/content/ai-chat-bot-python-aiml

# Live Demo

Chat with Chatty Cathy in the DevDungeon Discord server channel #chat-with-cathy.

https://discord.gg/unSddKm

# Set up your own bot

Run your own bot by following the instructions below.

## Installation

    pip install cathy
    
Or download this package and install with setup.py 

    python setup.py install
    
## Running

    cathy --help
    
## Usage

    Cathy.

    Discord chat bot using AIML artificial intelligence

    Usage:
       cathy -c <channel> -t <token> -r
    
    Options:
       -c <channel>   Name of channel to chat in (required)
       -t <token>     Bot's Discord API token (required)
       -b <brainfile> Brainfile to use for learning (optional)
       -r             Respond only when bot name mentioned (optional)
       -o             Set owner name of the bot (optional)
       -h --help      Show this screen.
      
## Example Usage

    Basic:
       cathy -c somechannel -t XXXXXXSECRETTOKENXXXXXXX
    All:
       cathy -c somechannel -t XXXXXXSECRETTOKENXXXXXXX -b /path/to/brain.file -r -o SomeName

## Contact

nanodano@devdungeon.com
