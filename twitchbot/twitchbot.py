#Scriptet är till 99% skamlöst stulet från https://twitchio.readthedocs.io/en/latest/quickstart.html Thx af!

from twitchio.ext import commands
import datetime

import sqlite3

#Läs in variabler från Variables.txt
def get_pair(line):
    key, sep, value = line.strip().partition("=")
    return key, value

with open("../Variables.txt") as fd:
    var_list = dict(get_pair(line) for line in fd)

twitch_access_token=var_list["twitch_access_token"]
twitch_channel=var_list["twitch_channel"]
twitch_client_id=var_list["twitch_client_id"]
twitch_nick=var_list["twitch_nick"]

conn = sqlite3.connect('../database.db')


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        super().__init__(token=twitch_access_token, prefix='?', initial_channels=[twitch_channel], client_id=twitch_client_id, nick=twitch_nick)


    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        msg_content=str(message.raw_data)

        if "WHISPER" in msg_content:

            #Fult sätt att hämta information ur chattmeddelande
            username=msg_content[msg_content.find("display-name=")+len("display-name="):msg_content.rfind(";emotes")]
            guess=msg_content[msg_content.rfind(":")+1:len(msg_content)]
            date_text=datetime.datetime.now()
            timestamp=date_text.timestamp()

            print("Username: "+username+"\n"+"Guess: "+guess+"\n"+"Date: "+str(date_text))

            #Hämta nuvarande fråga ur SQLite-databasen
            cursor = conn.execute("SELECT GAME_ID, QUESTION_ID, LEVEL from CURRENT_QUESTION")
            current_answer=cursor.fetchone()
            game_id=current_answer[0]
            question_id=current_answer[1]
            level=current_answer[2]

            #Skriv in i databasen
            db_string="INSERT INTO ANSWERS (GAME_ID,QUESTION_ID,USERNAME,GUESS,LEVEL) \
            VALUES ("+str(game_id)+","+str(question_id)+", '"+username+"','"+guess+"',"+ str(level)+" )"
            #print(db_string)
            conn.execute(db_string)
            conn.commit()

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        #await ctx.send(f'Hello {ctx.author.name}!')
        await ctx.channel.send(f"Hejhej @{ctx.author.name}")


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
