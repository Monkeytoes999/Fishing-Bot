# Import statements
from importlib.resources import contents
from typing import Literal
import discord
from discord import app_commands, ui
import random
import json
import time
import math
import png

# Get user data
file = open('users.json',)
users = json.load(file)
mFile = open('market.json',)
market = json.load(mFile)
eqFile = open('equipment.json')
equipment = json.load(eqFile)
lcFile = open('locations.json')
locations = json.load(lcFile)
ldbFile = open('leaderboards.json')
leaderboards = json.load(ldbFile)

# Version number
beaver = "0.0.0.1"

# Fish data
rarityAr = ['common bass','common pike','common grunt','common\'t cod','common\'t marlin','common\'t tang','rare snapper','rare tetra','rare firefish', 'bonefish', 'common angelfish', 'common guppy', 'common\'t mudfish', 'common\'t trout', 'rare parrotfish', 'rare catfish', 'rubber ducky']
rarityGroups = ['common', 'common', 'common', 'commont', 'commont', 'commont', 'rare', 'rare', 'rare', 'event', 'common', 'common', 'commont', 'commont', 'rare', 'rare', 'novelty']
fishNames = ['bass', 'pike', 'grunt', 'cod', 'marlin', 'tang', 'snapper', 'tetra', 'firefish', 'bonefish', 'angelfish', 'guppy', 'mudfish', 'trout', 'parrotfish', 'catfish', 'rubber ducky']
fishWeights = [12, 2.1, .93, 18.5, 210, 1.32, 28, 0.0003, 0.0005, 7, 2, 0.0002, 0.015, 23, 45, 45, 0.011]
cfArS = [1, 2, 3, 11, 12]
ufArS = [4, 5, 6, 13, 14]
rfArS = [7, 8, 9, 15, 16]

# Value function
async def value(rarity, quality, foreign, prep):
    if rarity in cfArS:
        rarity = 1
    elif rarity in ufArS:
        rarity = 2
    elif rarity in rfArS:
        rarity = 3
    else:
        rarity = 4
    if (foreign):
        return round(3 + rarity*5 + quality*5 + prep)
    else:
        return round(rarity*5 + quality*5 + prep)

# Satisfaction function
async def satisfaction(r, q, p):
    if r in cfArS:
        r = 1
    elif r in ufArS:
        r = 2
    elif r in rfArS:
        r = 3
    else:
        r = 4
    return r+3*q+random.randint(0,2)+p*2

# Quality function
async def getRarityLevel(rarity):
    out = 0
    if rarity in cfArS:
        out = 1
    elif rarity in ufArS:
        out = 2
    elif rarity in rfArS:
        out = 3
    else:
        out = 4
    return out

# Prepare
async def prepare(ctx: discord.Interaction, slot:int=1):
    if (slot > len(users.get(f'{ctx.user.id}').get('inv'))):
        await ctx.response.send_message('Invalid inventory slot')
    elif (users[f'{ctx.user.id}']['inv'][f'{slot-1}']['prepBonus'] == 0):
        slot -= 1
        fish = users.get(f'{ctx.user.id}').get('inv').get(f'{slot}')
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.user.id}']["pos"]
        pr = getRarityLevel(r)
        oVal = await value(r, q, f, 0)
        skill = users.get(f'{ctx.user.id}').get(f'{"reputation"}')/100
        if (3**(pr - 1) < skill):
            skill = 3**(pr - 1)
        p = 0.1
        if (users[f'{ctx.user.id}']['equipment'].get('stove') != None):
            p += 2
        sS = ''
        if (users[f'{ctx.user.id}']['equipment']['seasoning'] > 0):
            p += 6
            sLeft = users[f'{ctx.user.id}']['equipment']['seasoning'] - 1
            users[f'{ctx.user.id}']['equipment']['seasoning'] = sLeft
            sS = f'\nYou used some basic seasoning, you have enough left for {sLeft} servings.'
        users[f'{ctx.user.id}']['inv'][f'{slot}']['prepBonus'] += (p+skill)
        nVal = await value(r,q,f,(p+skill))
        await ctx.response.send_message(f'{ctx.user.display_name}, you were able to increase the value of this fish by {nVal-oVal} perles! It is now worth {nVal} perles! :cook:{sS}')
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    else:
        await ctx.response.send_message('This fish has already been prepared!')

# Cook
async def cook(ctx: discord.Interaction, slot:int=1):
    if (slot <= len(users[f'{ctx.user.id}']['inv'])):
        fish = users[f'{ctx.user.id}']['inv'][f'{slot-1}']
        q = fish['quality']
        r = fish['rarity']
        f = fish['from'] != users[f'{ctx.user.id}']["pos"]
        p = fish['prepBonus']
        yum = await satisfaction(r,q,p)
        if yum > 12: yum = 12
        if yum < 3:
            users[f'{ctx.user.id}']['reputation'] -= 3-yum
            om = f'{ctx.user.display_name}, your customer hated your fish!'
        elif yum > 6:
            users[f'{ctx.user.id}']['reputation'] += yum-6
            om = f'{ctx.user.display_name}, your customer liked your fish!'
        else:
            om = f'{ctx.user.display_name}, your customer thought that your fish was alright'
        users[f'{ctx.user.id}']['money'] += await value(r,q,f,p)
        moneys = users[f'{ctx.user.id}']['money']
        i = 0
        j = 0
        newInv = {}
        while i < len(users[f'{ctx.user.id}']['inv']):
            if i != slot-1:
                newInv[f'{j}'] = users[f'{ctx.user.id}']['inv'][f'{i}']
                j += 1
            i += 1
        users[f'{ctx.user.id}']['inv'] = newInv
        await ctx.response.send_message(f'{om}\nYou have sold your fish for {await value(r,q,f,p)} perles. You now have {moneys} perles!')
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    else:
        await ctx.response.send_message('Invalid inventory slot')