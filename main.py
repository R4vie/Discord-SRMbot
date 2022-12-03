import os
import discord

my_secret = os.environ['token-sramon-2']

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
  print('We have logged {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  """"""""""
  if message.content.startswith('$hello'):
    await message.channel.send(
      'hello')  #https://cdn.7tv.app/emote/637be9fba61dcabc5095a32e/4x.webp')
  """""""""
  if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

try:
  client.run(my_secret)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  system('kill 1')
