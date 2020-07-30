import discord
from discord.ext import commands, menus, tasks
import logging
import random
import json
import os
import string
import datetime
import asyncio

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

@bot.command(aliases=["раздача"])
async def giveaway(ctx):
    await ctx.send("выберите канал где вы хотите проводить раздачу, к примеру #раздачи")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg1 = await bot.wait_for('message', check = check, timeout=30.0)

        channel_converter = discord.ext.commands.TextChannelConverter()
        try:
            channel = await channel_converter.convert(ctx, msg1.content)
        except commands.BadArgument:
            return await ctx.send("Такого канала не существует,пробуйте заново")
    except asyncio.TimeoutError:
        await member.send("таймоут, напишите команду еще раз")
    await ctx.send(f"ок, канал {channel.mention} выбран для раздачи,сколько победителей хотите?(Напишите число)")
    try:
        msg2 = await bot.wait_for('message', check = check, timeout=30.0)
        try:
            winerscount = int(msg2.content)
        except ValueError:
            return await ctx.send("Вы не указали число,начните все заново")

    except asyncio.TimeoutError:
        await member.send("таймоут, напишите команду еще раз")


    seconds = ("s", "sec", "secs", 'second', "seconds", "c", "сек", "секунда", 'секунду', "секунды", "секунд")
    minutes= ("min", "mins", "minute", "minutes", "мин", "минута", "минуту", 'минуты', 'минут')
    hours= ("h", "hour", "hours", "ч", 'час', 'часа', "часов")
    days = ("d", "day", "days", "д", 'день', 'дня', 'дней')
    weeks = ("w", "week", "weeks", "н", 'нед', 'неделя', "недели", "недель", "неделю")
    months = ("mo", "mos", "month", "months", "мес", "месяц", "месяца", 'месяцев')
    if since.lower() in seconds:
        timewait = time
    elif since.lower() in minutes:
        timewait = time*60
    elif since.lower() in hours:
        timewait = time*3600
    elif since.lower() in days:
        timewait = time*86400
    elif since.lower() in weeks:
        timewait = time*604800
    else:
        return await ctx.author.send("вы не указали единицу времени к примеру секунд,минут")


bot.run(os.environ["TESTBOT"])
