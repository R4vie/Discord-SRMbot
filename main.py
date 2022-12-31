import os, discord, requests, json, slotsy, datetime, asyncio, io
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


magic_words = []

with io.open('Magic_words.txt', 'r', encoding='utf8') as f:
    for line in f:
        magic_word = line.strip(",\n").split(", ")
        for word in magic_word:
            if word not in magic_words:
                magic_words.append(word)

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
    then = now.replace(hour=15, minute=20)  #Set UTC time
    if then < now:
      then += datetime.timedelta(days=1)
    wait_time = (then-now).total_seconds()
    await asyncio.sleep(wait_time)

    channel = bot.get_channel(1048683921216393309)
    await channel.send(daily_remainder)
    await asyncio.sleep(1)

  
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  msg = message.content
  if any(word in msg for word in magic_words):
    try:
      await message.add_reaction("<:sramon:1049037728517472276>")
    except:
      await message.channel.send(":robot: Wrong emoji code :robot:")#Add reaction emote to a message
  await bot.process_commands(message)

  
@bot.command()
@commands.cooldown(1,3)
async def punch(ctx, arg): 
    quote = get_quote()
    await ctx.send(f"guwno {arg}, {quote}")

  
@bot.command()
@commands.cooldown(1,10)
async def slots(ctx):
  slotsy.slots_machine.clear()
  
  msg_author = str(ctx.author)
  
  await ctx.channel.send(slotsy.slots() + "\n" + str(slotsy.points()))
    
  if msg_author not in db.keys():
    db.update({msg_author : int(slotsy.get_result())})
  elif msg_author in db.keys():
    result = slotsy.get_result()
    point = int(db[msg_author])
    points = point + int(result)
    db[msg_author] = points

    await ctx.channel.send("Kaska " + ctx.author.mention + ": "  + str(db[msg_author]) + "$") 
    
@bot.command()
@commands.cooldown(1,5)
async def slotsRanks(ctx):
  db1 = dict(sorted(db.items(), key=lambda item: item[1], reverse=True)) #Sorts the dictionary from largest value to lowest
  await ctx.channel.send("Najbogatsi: ")
  i=1
  for name, points in db1.items(): 
    await ctx.channel.send(str(i) + ". " + name + " - " + str(points) + "$") #Sends scoreboard
    i +=1

    
try:
  keep_alive()
  bot.run(my_secret)
except discord.errors.HTTPException:  #DISCORD CONNECTION ERROR --- RATE LIMITS ---
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("restarter.py")
  system('kill 1')
