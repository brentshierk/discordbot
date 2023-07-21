import discord
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import get
import requests
import json
import asyncio
import time
import asyncio
from weather import *
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DISCORD_API_KEY =os.getenv('DISCORD_API_KEY')
WEATHER_API_KEY =os.getenv('WEATHER_API_KEY')
command_prefix = '!'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#http://127.0.0.1:8000/api/score/update
#"https://salty-lake-34967-ee129c6a2f28.herokuapp.com/api/random"

def get_score():
    response = requests.get("http://127.0.0.1:8000/api/score/leaderboard")
    leaderboard = ''
    id = 1
    json_data = json.loads(response.text)

    for item in json_data:
        leaderboard += str(id) + ' ' + item['name'] + ". " + str(item['points']) + "\n"
        id += 1
    return (leaderboard)

def update_score(user, points):
    url = 'http://127.0.0.1:8000/api/score/update/'
    new_score = {'name':user,'points':points}
    x = requests.post(url, data = new_score)

    return 

def get_question():
    qs = ''
    id = 1
    answer = 0
    points = 0
    response = requests.get("http://127.0.0.1:8000/api/random")
    json_data = json.loads(response.text)
    qs += "Question: \n"
    qs += json_data[0]['title'] + '\n'

    for item in json_data[0]['answer']:
        qs +=  str(id) + ". " + item['answer'] + "\n"

        if item['is_correct']:
            answer = id
        
        id += 1
    points = json_data[0]['points']
    return(qs, answer, points)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!s'):
        leaderboard = get_score()
        await message.channel.send(leaderboard)

    if message.content.startswith('!q'):
        q, ans,points = get_question()
        await message.channel.send(q)
    
        def check(m):
            return m.author == message.author and m.content.isdigit()
        
        try:
            guess = await client.wait_for('message',check=check,timeout=10.0)
        except asyncio.TimeoutError:
            return await message.channel.send('Sorry, you did not answer quick enough')
        
        if int(guess.content) == ans:
            
            user = guess.author
            msg = str(guess.author.name) + 'Correct! +' + str(points) + 'points'
            await message.channel.send(msg)
            update_score(user, points)
        else:
            await message.channel.send('Sorry thats incorrect')



client.run(DISCORD_API_KEY)