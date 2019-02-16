import discord
import os
import random
import pkg_resources
from discord.ext import commands
import asyncio
import aiml
import re
import atexit

STARTUP_FILE = "std-startup.xml"
BOT_PREFIX = ('?', '!')


class ChattyCathy:
    def __init__(self, channel_name, bot_token, brn, rname, oname):
        self.channel_name = channel_name
        self.token = bot_token
        self.brn = brn
        self.rname = rname
        self.oname = oname

        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()
        initial_dir = os.getcwd()
        if not self.brn:
           # if no brain defined just load normal startup
           os.chdir(pkg_resources.resource_filename(__name__, ''))  # Change directories to load AIML files properly
           startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
           self.aiml_kernel.learn(startup_filename)
           self.aiml_kernel.respond("LOAD AIML B")
        else:
           # if brain file defined check to see if it exists, if not create it and load
           if os.path.isfile(self.brn):
              self.aiml_kernel.loadBrain(self.brn)
           else:
              os.chdir(pkg_resources.resource_filename(__name__, ''))  # Change directories to load AIML files properly
              startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
              self.aiml_kernel.learn(startup_filename)
              self.aiml_kernel.respond("LOAD AIML B")
              self.aiml_kernel.saveBrain(self.brn)

        
        os.chdir(initial_dir)

        # try and save brain on close if it exists
        atexit.register(self.save)
        # Set up Discord client
        self.discord_client = commands.Bot(command_prefix=BOT_PREFIX)
        self.setup()

    def setup(self):

        @self.discord_client.event
        @asyncio.coroutine
        def on_ready():
            BOT_NAME = self.discord_client.user.name
            self.aiml_kernel.setBotPredicate('name',BOT_NAME)
            self.aiml_kernel.setBotPredicate('owner',self.oname)
            self.aiml_kernel.setBotPredicate('master',self.oname)
            self.aiml_kernel.setBotPredicate('admin',self.oname)
            print("Bot Online!")
            print("Name: {}".format(BOT_NAME))
            print("Channel: {}".format(self.channel_name))
            if self.rname == True:
                print("Name Response Only Mode Active")

            print("ID: {}".format(self.discord_client.user.id))
            yield from self.discord_client.change_presence(game=discord.Game(name='Chatting with Humans'))

        @self.discord_client.event
        @asyncio.coroutine
        def on_message(message):
            BOT_NAME = self.discord_client.user.name
            if message.author.bot or (str(message.channel) != self.channel_name) and (not str(message.channel).startswith("Direct Message")):
                print("ALL Message: " + str(message.channel) + str(message.content))
                return

            if message.content is None:
                print("Empty message received.")
                return

            print("Message: " + str(message.content))

            def findWholeWord(w):
                return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

            if message.content.startswith(BOT_PREFIX):
                # Pass on to rest of the client commands
                yield from self.discord_client.process_commands(message)
            elif self.rname != True or str(message.channel).startswith("Direct Message"):
                # if no aiml response we don't want to cause an exception trying to send an empty http message
                aiml_response = self.aiml_kernel.respond(message.content)
                if aiml_response:
                   yield from self.discord_client.send_typing(message.channel)
                   yield from asyncio.sleep(random.randint(1,3))
                   yield from self.discord_client.send_message(message.channel, aiml_response)
            elif findWholeWord(BOT_NAME)(message.content):
                nmsg = re.sub(BOT_NAME, '', message.content, flags=re.IGNORECASE)
                aiml_response = self.aiml_kernel.respond(nmsg)
                if aiml_response:
                   yield from self.discord_client.send_typing(message.channel)
                   yield from asyncio.sleep(random.randint(1,3))
                   yield from self.discord_client.send_message(message.channel, aiml_response)

        #@self.discord_client.event
        #@asyncio.coroutine
        #def on_dm(message):

    def save(self):
        if os.path.isfile(self.brn):
           self.aiml_kernel.saveBrain(self.brn)

    def run(self):
        self.discord_client.run(self.token)

    def __del__(self):
        print('Shutting Down')