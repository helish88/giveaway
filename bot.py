import discord
from discord.ext import commands, menus, tasks
import logging
import random
import json
import os
import string
import datetime

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')





@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def test(ctx):
    await ctx.send("test ok")



bot.run(os.environ["TESTBOT"])
