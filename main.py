import os
import discord
import requests
import json

my_secret = os.environ['token-sramon-2']

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents=intent)#intents=discord.Intents.default())

shitty_words = [
                "guwno", "gówno", "gowno", "gówniany", "gówniana",
                "gowniany", "gowniana", "zasrany", "zasrana",                      "obsrana", "zasrani"
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
  
  if msg.startswith('$inspire'): 
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in shitty_words):
    await message.channel.send(shitty_image)

    
   # await message.channel.send('hello')  #https://cdn.7tv.app/emote/637be9fba61dcabc5095a32e/4x.webp')

try:
  client.run(my_secret)
except discord.errors.HTTPException:  #DISCORD CONNECTION ERROR --- RATE LIMITS ---
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  system('kill 1')
