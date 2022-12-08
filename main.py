import os, discord, requests, json, slots, datetime, asyncio
#import discord
#import requests
#import json
#import slots
from replit import db
from keep_alive import keep_alive
from os import system

my_secret = os.environ['token-sramon-2']
daily_remainder = os.environ['DailyRemainder']

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)

shitty_words = [
                "guwno", "gówno", "gowno", "gówniany", "gówniana",
                "gowniany", "gowniana", "zasrany", "zasrana", "obsrana", "zasrani", "lol", "lola" , "lolu", "liga" , "lige", "lidze" "ligusi", "ligusie"
               ]
shitty_image = "https://cdn.7tv.app/emote/637be9fba61dcabc5095a32e/4x.webp"

def get_quote():  #Get random quote
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  
  
@client.event  #Bot starts
async def on_ready():
  print('We have logged {0.user}'.format(client))
  await schedule_daily_message()

  
async def schedule_daily_message():#Every day at specific hour run script
  now = datetime.datetime.now()
  #then = now+datetime.timedelta(days=1)
  then = now.replace(hour=14, minute=30)#Set time !!!UTC time!!!
  wait_time = (then-now).total_seconds()
  
  await asyncio.sleep(wait_time)

  channel = client.get_channel(774724352561250324)

  await channel.send(daily_remainder)

@client.event  #On message print
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  msg_author = str(message.author)
  
  if msg.startswith("!Inspire"): 
    quote = get_quote()
    await message.channel.send(quote)

  elif msg.startswith("!slots"):  #Starts slots 
    slots.slots_machine.clear()
    
    await message.channel.send(slots.slots() + "\n" + slots.points())
    
    if msg_author not in db.keys():
      msg_author = 0
    elif msg_author in db.keys():
      result = slots.get_result()
      point = int(db[msg_author])
      points = point + int(result)
      db[msg_author] = points
      await message.channel.send("Twoja kaska: " + str(points) + "$") 
      
  
    
  elif msg.startswith("!slotRanks"): #I am not proud this piece of code, it was created later, after slots, after this bad dictionary {name : value} much better and easier to sort would be [{name : discord_nickname, value: points}, {name : discord_nickname2, value: points}] I hope at least 
    
    db1 = dict(sorted(db.items(), key=lambda item: item[1], reverse=True))
    scoreName = []
    scorePoints = []
    for name in db1:
      scoreName.append(name)
    for points in db1.values():
      scorePoints.append(points)
    await message.channel.send("Najbogatsi: ")
    for i in range(len(scoreName)):
      await message.channel.send(str(i+1)+". " + str(scoreName[i]) + " - " + str(scorePoints[i]) + "$")

      
  if any(word in msg for word in shitty_words):  
    await message.add_reaction("<:sramon:1049037728517472276>")  #Add reaction emote to a message
  
try:
  keep_alive()
  client.run(my_secret)
except discord.errors.HTTPException:  #DISCORD CONNECTION ERROR --- RATE LIMITS ---
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("restarter.py")
  system('kill 1')
