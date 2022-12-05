import os
import discord
import requests
import json
import slots
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['token-sramon-2']

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)#intents=discord.Intents.default())

shitty_words = [
                "guwno", "gówno", "gowno", "gówniany", "gówniana",
                "gowniany", "gowniana", "zasrany", "zasrana", "obsrana", "zasrani"
               ]
shitty_image = "https://cdn.7tv.app/emote/637be9fba61dcabc5095a32e/4x.webp"

def get_quote():  #GETTING RANDOM QUOTE
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event  #BOT STARTING
async def on_ready():
  print('We have logged {0.user}'.format(client))


@client.event  #ON MESSAGE PRINT
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  msg_author = str(message.author)
  if msg.startswith("Inspiruj"): 
    quote = get_quote()
    await message.channel.send(quote + "\n" + str(message.author))
  elif msg.startswith("1"):
    await message.add_reaction("<:sramon:1049037728517472276>")
  elif msg.startswith("!slots"):  #START SLOTS MACHINE IF !slots 
   # msg_author = str(message.author) 
    slots.slots_machine.clear()
    
    await message.channel.send(slots.slots() + "\n" + slots.points())
    
    if msg_author not in db.keys():
      msg_author = 0
    elif msg_author in db.keys():
      result = slots.get_result()
      point = int(db[msg_author])
      points = point + int(result)
      db[msg_author] = points
      await message.channel.send("Twoje Punkty: " + str(points)) 
      
  
    
  elif msg.startswith("!slotsRanks"):
    return None

    
  if any(word in msg for word in shitty_words):  
    await message.add_reaction("<:sramon:1049037728517472276>")  #ADD REACTION EMOTE TO A MESSAGE
  
try:
  keep_alive()
  client.run(my_secret)
except discord.errors.HTTPException:  #DISCORD CONNECTION ERROR --- RATE LIMITS ---
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  system('kill 1')
