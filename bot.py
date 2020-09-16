import discord
from discord.ext import commands, menus, tasks
import logging
import random
import json
import os
import string
from datetime import datetime, timedelta


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
    await ctx.send(embed=discord.Embed(color=discord.Color.green(), title = "выберите канал где вы хотите проводить раздачу, к примеру #раздачи")) #select channel for giveaway,for example #giveaway
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg1 = await bot.wait_for('message', check = check, timeout=30.0)

        channel_converter = discord.ext.commands.TextChannelConverter()
        try:
            channel = await channel_converter.convert(ctx, msg1.content)
        except commands.BadArgument:
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "Такого канала не существует,пробуйте заново")) #this channel does not exist,please select another channel

    except asyncio.TimeoutError:
        await ctx.send("таймоут, напишите команду еще раз") # time out, try again
    if not channel.permissions_for(ctx.guild.me).send_messages or  not channel.permissions_for(ctx.guild.me).add_reactions:
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), description = f"У меня нет права отправлять сообщение и(или) добавлять реакции(емози) в канале {channel}")) #bot don't have permissions to send channel or/and add reactions in #channel
    await ctx.send(embed=discord.Embed(color=discord.Color.green(), description = f"ок, канал {channel.mention} выбран для раздачи,сколько победителей хотите?(Напишите число)")) #ok, channel {channel.mention} is selected for giveaway, how many winners do you want? (write number) 
    try:
        msg2 = await bot.wait_for('message', check = check, timeout=30.0)
        try:
            winerscount = int(msg2.content)
        except ValueError:
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "Вы не указали число, начните все заново")) #You didn't specify a number, write command again

    except asyncio.TimeoutError:
        await ctx.send("таймоут, напишите команду еще раз") # time out,try again

    await ctx.send(embed=discord.Embed(color=discord.Color.green(), title = "Укажите время для giveaway, можете указать к примеру: 20 часов, 4 дня, 5 минут (все через пробел)")) #Specify the time for giveaway, you can specify for example: 20 hours, 4 days, 5 minutes (all separated by a space)
    try:
        since = await bot.wait_for('message', check = check, timeout=30.0)

    except asyncio.TimeoutError:
        await ctx.send("таймоут, напишите команду еще раз") # time out,try again


    seconds = ("s", "sec", "secs", 'second', "seconds", "c", "сек", "секунда", 'секунду', "секунды", "секунд")
    minutes= ("min", "mins", "minute", "minutes", "мин", "минута", "минуту", 'минуты', 'минут')
    hours= ("h", "hour", "hours", "ч", 'час', 'часа', "часов")
    days = ("d", "day", "days", "д", 'день', 'дня', 'дней')
    weeks = ("w", "week", "weeks", "н", 'нед', 'неделя', "недели", "недель", "неделю")
    months = ("mo", "mos", "month", "months", "мес", "месяц", "месяца", 'месяцев')
    rawsince = since.content
    try:
        time = int(since.content.split(" ")[0])
    except ValueError:
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "вы не указали единицу времени к примеру секунд,минут. Напишите команду заново")) #you have not specified a unit of time, for example seconds, minutes. write command again
    since = since.content.split(" ")[1]
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
        return await ctx.send(embed=discord.Embed(color=discord.Color.red(), title = "вы не указали единицу времени к примеру секунд,минут. Напишите команду заново")) #you have not specified a unit of time, for example seconds, minutes. write command again
    await ctx.send("Укажите приз какой хотите разыграть")
    try:
        msg4 = await bot.wait_for('message', check = check, timeout=30.0)


    except asyncio.TimeoutError:
        await ctx.send("таймоут, напишите команду еще раз") #time out,try again
    await ctx.send(embed = discord.Embed(color=discord.Color.green(), description = f"Приз: {msg4.content}\nколичество победителей: {winerscount}\nканал: {channel.mention}\nчерез {rawsince} ")) # prize -  msg4.content winners count- winnerscount. channel- channel, giveaway after - rawsince 

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title=f"🎉 Новая раздача🎉\n`{msg4.content}`",timestamp = futuredate, description="Добавьте реакцию 🎉 что бы участвовать" ) #Add reaction 🎉 to participate
    embed1.set_footer(text=f"раздача закончится") #when giveaway over
    msg = await channel.send(embed=embed1)
    await msg.add_reaction("🎉")
    await asyncio.sleep(timewait)
    message = await channel.fetch_message(msg.id)
    for reaction in message.reactions:
        if str(reaction.emoji) == "🎉":
            users = await reaction.users().flatten()
            if len(users) == 1:
                return await msg.edit(embed=discord.Embed(title="победителей нет")) # no winners

    winners = random.sample([user for user in users if not user.bot], k=winerscount)
    await message.clear_reactions()
    emozi='<a:hypertada:677073826265300992>'
    winnerstosend = "\n".join([winner.mention for winner in winners])
    await msg.edit(embed=discord.Embed(title=f"{emozi} победитель {emozi}", description=f"выиграл(и)\n{winnerstosend}",color=discord.Color.blue()).add_field(name=f"приз", value=f"`{msg4.content}`", inline=False)) # winner
bot.run(os.environ["TESTBOT"])
