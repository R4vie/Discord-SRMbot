import os, discord, requests, json, slots, datetime, asyncio
from replit import db
from keep_alive import keep_alive
from os import system
from discord.ext import commands

my_secret = os.environ['token-sramon-2']
daily_remainder = os.environ['DailyRemainder']

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

#client = discord.Client(intents=intent)
bot = commands.Bot(command_prefix='!', intents=intent)


shitty_words = [
                "guwno", "gówno", "gowno", "gówniany", "gówniana", "gówna", "gowna",
                "gowniany", "gowniana", "gównem", "gownem", "zasrany", "zasrana", "obsrana", "zasrani", "lol", "lola" , "lolu", "liga" , "lige", "lidze" "ligusi", "ligusie"
               ]
shitty_image = "https://cdn.7tv.app/emote/637be9fba61dcabc5095a32e/4x.webp"

def get_quote():  #Get random quote
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  

  
@bot.event  #Bot starts
async def on_ready():
  print('We have logged {0.user}'.format(bot))
  await schedule_daily_message()

  
async def schedule_daily_message():#Every day at specific hour run script
  now = datetime.datetime.now()
  then = now+datetime.timedelta(days=1)
  then.replace(hour=14, minute=30)  #Set UTC time
  wait_time = (then-now).total_seconds()
  
  await asyncio.sleep(wait_time)

  channel = bot.get_channel(774724352561250324)

  await channel.send(daily_remainder)

  
@bot.command()
@commands.cooldown(1,2)
async def punch(ctx, arg): 
    quote = get_quote()
    await ctx.send(f"guwno {arg}"+quote)
      

@bot.event  #On message print                  
async def on_message(message):
  if message.author == bot.user:
    return
  msg = message.content
  msg_author = str(message.author)
  """
  if msg.startswith("!Inspire"): 
    quote = get_quote()
    await message.channel.send(quote)
  """
  if msg.startswith("!slots"):  #Starts slots 
    slots.slots_machine.clear()
    
    await message.channel.send(slots.slots() + "\n" + slots.points())
    
    if msg_author not in db.keys():
      db.update({msg_author : int(slots.get_result())})
    elif msg_author in db.keys():
      result = slots.get_result()
      point = int(db[msg_author])
      points = point + int(result)
      db[msg_author] = points

      await message.channel.send("Kaska " + message.author.mention + ": "  + str(db[msg_author]) + "$") 
      
  
    
  elif msg.startswith("!slotRanks"): 
    
    db1 = dict(sorted(db.items(), key=lambda item: item[1], reverse=True)) #Sorts the dictionary from largest value to lowest
    await message.channel.send("Najbogatsi: ")
    i=1
    for name, points in db1.items(): 
      await message.channel.send(str(i) + ". " + name + " - " + str(points) + "$") #Sends scoreboard
      i +=1
      
  if any(word in msg for word in shitty_words):  
    await message.add_reaction("<:sramon:1049037728517472276>")  #Add reaction emote to a message
  
try:
  keep_alive()
  bot.run(my_secret)
except discord.errors.HTTPException:  #DISCORD CONNECTION ERROR --- RATE LIMITS ---
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("restarter.py")
  system('kill 1')
