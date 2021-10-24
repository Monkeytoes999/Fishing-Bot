import discord
from discord.ext import tasks, commands
import random
import json
import time
import math

file = open('users.json',)
users = json.load(file)
mFile = open('market.json',)
market = json.load(mFile)
eqFile = open('equipment.json')
equipment = json.load(eqFile)

bot = commands.Bot(command_prefix = 'f.', case_insensitive=(True))
TOKEN = 'OTAxNDg4Mjg5MDIwODAxMTI0.YXQmZA.ZOoylTHa_LhRgFBFboV_bS7wSU0'

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')
    channel = bot.get_channel(901489176384507917)
    print (f'Ok {bot.user.name} is online now')

async def createUser(userID):
    users['{}'.format(userID)] = {
        "pos": len(users),
        "money": 0,
        "fishlog": {
        "fish0": 0,
        "fish1": 0
        },
        "equipment": {"fishEq":{"name": "Stick", "quality": 0.1, "price": 0}, "boat":{"name": "raft", "cooldown": 5, "dur": 5, "price": 0}, "cookEq":{"name": "Microwave", "quality": 0.01, "price": 0} },
        "inv": {},
        "contacts": {},
        "reputation": 1,
        "lastFish": 0,
        "isFishing": 0,
        "lastDur": 0,
        "lastCd": 0
    }
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile) 
           
async def pullFish(userPos):
    rr = await rarity()
    fish = {"from":userPos, "rarity": rr, "quality": random.random(), "prepBonus": 0}
    return fish

rarityAr = ['common bass','common\'t cod','rare snapper']

async def rarity():
    rarity = random.random()
    if (rarity < .75):
        return 1
    elif (rarity < .95):
        return 2
    else:
        return 3

async def value(rarity, quality, foreign, prep):
    if (foreign):
        return round(3 + rarity*5 + quality*5 + prep) 
    else:
        return round(rarity*5 + quality*5 + prep)
    
async def qualify(quality):
    if (quality == 1):
        return "perfect"
    elif (quality > .75):
        return "good"
    elif (quality > .25):
        return "decent"
    else:
        return "bad"

@bot.event
async def on_command(ctx):
    if not str(ctx.author.id) in users:
        createUser(ctx.author.id)

@bot.command()
async def fish(ctx):
    userInfo = users.get('{}'.format(ctx.author.id))
    if (userInfo["isFishing"] == 0 and (userInfo["lastFish"] - time.time() < 0)):
        users[f'{ctx.author.id}']["lastFish"] = time.time() + userInfo["equipment"]["boat"]["cooldown"] + userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.author.id}']["isFishing"] = 1
        users[f'{ctx.author.id}']["lastDur"] = userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.author.id}']["lastCd"] = userInfo["equipment"]["boat"]["cooldown"]
        await ctx.send(f'Your fishing trip has started! Come back in {userInfo["equipment"]["boat"]["dur"]} seconds to see the results!')
    elif (userInfo["isFishing"] == 1 and (userInfo["lastCd"] >= userInfo["lastFish"] - time.time())):
        totVal = 0
        numCaught = math.floor(userInfo["equipment"]["fishEq"]["quality"]*20*userInfo["lastDur"]/60)
        if numCaught == 0:
            numCaught = random.randint(0,1)
        for i in range(numCaught):
            fish = await pullFish(userInfo.get("pos"))
            users[f'{ctx.author.id}']["inv"][f'{len(userInfo.get("inv"))}'] = fish
            q = fish.get("quality")
            r = fish.get("rarity")
            totVal += await value(r,q,False,0)
        users[f'{ctx.author.id}']["isFishing"] = 0
        await ctx.send(f'Your fishing trip yieded {numCaught} fish! Their total value is {totVal} perles! :fishing_pole_and_fish:')
    elif (userInfo["lastCd"] < userInfo["lastFish"] - time.time()):
        await ctx.send(f'You\'re still fishing! Come back in {round(userInfo["lastFish"] - time.time() - userInfo["lastCd"])} seconds!')
    else: 
        await ctx.send(f'You need to wait {round(userInfo["lastFish"]-time.time())} more seconds before fishing again for conservation reasons!')
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)

@bot.command()
async def trade(ctx, slot:int):
    userInfo = users.get('{}'.format(ctx.author.id))
    if (slot>len(userInfo.get('inv'))):
        await ctx.channel.send('Invalid inventory slot')
    else:
        slot -= 1
        if (userInfo.get('inv').get(f'{slot}').get("from") == userInfo.get("pos")):
            userFish = userInfo.get('inv').get(f'{slot}')
            marketSlot = random.randint(0,99999)
            print(marketSlot)
            marketFish = market.get("slot{}".format(marketSlot))
            userFish["prepBonus"] = 0
            market["slot{}".format(marketSlot)] = userFish
            userInfo['inv'][f'{slot}'] = marketFish
            q = marketFish.get("quality")
            r = marketFish.get("rarity")
            await ctx.send(f'Your new fish is a {rarityAr[r-1]} and is in {await qualify(q)} condition. It is worth {await value(r,q,True,0)} perles! :fish:')
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)
        else:
            await ctx.channel.send('You can\'t send this fish back!')

@bot.command()
async def prepare(ctx, slot:int):
    if (slot>len(users.get(f'{ctx.author.id}').get('inv'))):
        await ctx.channel.send('Invalid inventory slot')
    elif (users[f'{ctx.author.id}']['inv'][f'{slot-1}']['prepBonus'] == 0):
        slot -= 1
        fish = users.get(f'{ctx.author.id}').get('inv').get(f'{slot}')
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") == users[f'{ctx.author.id}']["pos"]
        skill = users.get(f'{ctx.author.id}').get(f'{"reputation"}')
        users[f'{ctx.author.id}']['inv'][f'{slot}']['prepBonus'] += skill
        await ctx.channel.send(f'You were able to increase the value of this fish by {skill}! It is now worth {await value(r,q,f,skill)} perles! :cook:')
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    else:
        await ctx.channel.send('This fish has already been prepared!')

@bot.command(aliases=['inventory'])
async def inv(ctx):
    num = len(users[f'{ctx.author.id}']['inv'])
    n = 25 if(num > 24) else num
    inv_embed = discord.Embed(
        title=str(f'{ctx.author}'),
        type="rich",
        description=f"You have {num} fish in your inventory. Here are the first {n}"
    )
    i = 0
    while (i < len(users[f'{ctx.author.id}']['inv'])):
        fish = users[f'{ctx.author.id}']['inv'][f'{i}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") == users[f'{ctx.author.id}']["pos"]
        p = fish["prepBonus"]
        prp = " not" if (p == 0) else ""
        inv_embed.add_field(name=f'Slot {i+1}', value=f'A {rarityAr[r-1]} that is worth {await value(r,q,f,p)} perles and has{prp} been prepared.')
        i += 1
    await ctx.channel.send(embed = inv_embed)

@bot.command()
async def checkFish(ctx, slot:int):
    if (slot > 0 and slot <= len(users[f'{ctx.author.id}']['inv'])):
        fish = users[f'{ctx.author.id}']['inv'][f'{slot-1}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") == users[f'{ctx.author.id}']["pos"]
        p = fish["prepBonus"]
        prp = " not" if (p == 0) else ""
        await ctx.channel.send(f'A {rarityAr[r-1]} that is worth {await value(r,q,f,p)} perles and has{prp} been prepared.')
    else:
        await ctx.channel.send('Invalid inventory slot')

@bot.command(aliases=['sell'])
async def cook(ctx, slot:int):
    if (slot <= len(users[f'{ctx.author.id}']['inv'])):
        fish = users[f'{ctx.author.id}']['inv'][f'{slot-1}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") == users[f'{ctx.author.id}']["pos"]
        p = fish["prepBonus"]
        users[f'{ctx.author.id}']["money"] += await value(r,q,f,p)
        j = 0
        newInv = {}
        for i in range(len(users[f'{ctx.author.id}']['inv'])):
            if (i != slot-1):
                newInv[f'{j}'] = users[f'{ctx.author.id}']['inv'][f'{i}']
                j += 1
        users[f'{ctx.author.id}']['inv'] = newInv
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
        moneys = users[f'{ctx.author.id}']["money"]
        await ctx.channel.send(f'You have sold your fish for {await value(r,q,f,p)} perles. You now have {moneys} perles!')
    else:
        await ctx.channel.send('Invalid inventory slot')

@bot.command(aliases=['market'])
async def markerakrkea(ctx): #pulls up an embedded that displays market slots and fish
    market_embed = discord.Embed (title = "The Net, for fish", type = 'rich')
    page = ""
    for i in range(10):
       marketSlot = random.randint(0,99999)
       marketFish = market.get(f"slot{marketSlot}")
       prep = "prepared" if (marketFish.get("prepBonus") > 0) else "Not prepared"
       page += f'**Slot**: {marketSlot}, Origin: {marketFish.get("from")}, Quality: {await qualify(marketFish.get("quality"))}, Type: {rarityAr[marketFish.get("rarity")-1]}. {prep}. \n'
    market_embed.add_field(name="The one stop shop for bass and cod! (and other things maybe)", value = f'{page}', inline = False)
    market_embed.set_thumbnail(url="https://i.etsystatic.com/15020412/r/il/455abc/2328156575/il_1588xN.2328156575_4m7l.jpg")
    await ctx.send(embed = market_embed)

#@bot.command()
#async def store(ctx):
#    store_embed = discord.Embed (title = "Jerry's Bait Shop (You know the place)", type = "rich")
#    fishEq = equipment.get("fishEq")
#    rods = fishEq.get("fishRods")
#    boats = fishEq.get("boats")
#    cookEq = equipment.get("cookEq")
#    rodso = ""
#    boatso = ""
#    cooko = ""
#    for i in range(3):
#        rod = rods.get(f'{i+1}')
#        rodso += f'{}/n'
#    for i in range(3):
#        boatso += boats.get(f'{i+1}')
#    for i in range (2):
#        cooko += cookEq.get(f'{i+1}')
#    store_embed.add_field(name="Fishing Equipment")
#    store_embed.add_field(name="Cooking Equipment")

        

@bot.command()
async def buy(ctx, marketSlot:int):
    marketFish = market.get(f'slot{marketSlot}')
    q = marketFish.get("quality")
    r = marketFish.get("rarity")
    f = marketFish.get("from") == users[f'{ctx.author.id}']["pos"]
    p = marketFish["prepBonus"]
    cost = await value(r,q,f,p)
    if (users[f'{ctx.author.id}']["money"] >= cost):
        users[f'{ctx.author.id}']["money"] -= cost
        moneys = users[f'{ctx.author.id}']["money"]
        userInv = users[f'{ctx.author.id}']['inv'] 
        users[f'{ctx.author.id}']["inv"][f'{len(userInv)}'] = marketFish
        marketFish = await pullFish(users[f'{ctx.author.id}']['pos'])
        await ctx.send(f"You bought the fish for {cost} perles! You now have {moneys} perles. :label:")
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
        with open('market.json', 'w') as outfile:
            json.dump(market, outfile)
    else:
        await ctx.send("You do not have enough perles to make this transaction! :chart_with_downwards_trend:")   
    

@bot.command(aliases=['pearles', 'perles', 'pearls', 'coins', 'moneys', 'moneyz', 'cash', 'dollars', 'fish blood', 'a'])
async def money(ctx):
    moneys = users[f'{ctx.author.id}']["money"]
    await ctx.send(f"You currently have {moneys} pearles!")

#@bot.event
async def on_message(message):
    if (message.content[0:2]=="--"):
        if (users.get('{}'.format(message.author.id))==None):
            createUser(message.author.id)
        userInfo = users.get('{}'.format(message.author.id))
        
        if (message.content[2:] == 'fish'):
            fish = await pullFish(userInfo["pos"])
            print(fish)

        if (message.content[2:] == 'createMarket'):
            if (True):
                market = {}
            i = 0
            while i < 100000:
                marketFish = await pullFish(-1)
                market['slot{}'.format(i)] = marketFish
                i += 1
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)





bot.run(TOKEN)