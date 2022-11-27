from importlib.resources import contents
from typing import Literal
import discord
from discord import app_commands, ui
import random
import json
import time
import math
import png

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

beaver = "0.0.0.1"

async def prepare(ctx: discord.Interaction, slot:int=1):
    if (slot>len(users.get(f'{ctx.user.id}').get('inv'))):
        await ctx.response.send_message('Invalid inventory slot')
    elif (users[f'{ctx.user.id}']['inv'][f'{slot-1}']['prepBonus'] == 0):
        slot -= 1
        fish = users.get(f'{ctx.user.id}').get('inv').get(f'{slot}')
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.user.id}']["pos"]
        if r in cfArS:
            pr = 1
        elif r in ufArS:
            pr = 2
        elif r in rfArS:
            pr = 3
        else:
            pr = 4
        oVal = await value(r,q,f,0)
        skill = users.get(f'{ctx.user.id}').get(f'{"reputation"}')/100
        if (3**(pr-1) < skill): skill = 3**(pr-1)
        p = .1
        p += 2 if (users[f'{ctx.user.id}']['equipment'].get('stove') != None) else 0
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