token = '' # Input your token here.


# Imports
import discord
import asyncio
import random
import re



# From imports
from discord.ext import commands
from datetime import datetime, timedelta
from colorama import Fore, Style


# Error Imports
from discord.ext.commands import MissingPermissions




intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '!' , case_insensitive = True , intents = intents)
bot.remove_command('help')


# Commands

# Giveaway Command
@bot.command(aliases = ['start' , 'g'])
@commands.has_permissions(manage_roles = True)
async def giveaway(ctx):
    await ctx.send("Select the channel, you would like the giveaway to be in.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg1 = await bot.wait_for('message', check = check, timeout=30.0)

        channel_converter = discord.ext.commands.TextChannelConverter()
        try:
            giveawaychannel = await channel_converter.convert(ctx, msg1.content)
        except commands.BadArgument:
            return await ctx.send("This channel doesn't exist, please try again.")

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")
        
        
    if not giveawaychannel.permissions_for(ctx.guild.me).send_messages or not giveawaychannel.permissions_for(
            ctx.guild.me).add_reactions:
        return await ctx.send(
            f"Bot does not have correct permissions to send in: {giveawaychannel}\n **Permissions needed:** ``Add reactions | Send messages.``")

    await ctx.send("How many winners to the giveaway would you like?")
    try:
        msg2 = await bot.wait_for('message', check = check, timeout=30.0)
        try:
            winerscount = int(msg2.content)
        except ValueError:
            return await ctx.send("You didn't specify a number of winners, please try again.")

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")

    await ctx.send("Select an amount of time for the giveaway.")
    try:
        since = await bot.wait_for('message', check = check, timeout=30.0)

    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again!")
        
    


    seconds = ("s", "sec", "secs", 'second', "seconds")
    minutes= ("m", "min", "mins", "minute", "minutes")
    hours= ("h", "hour", "hours")
    days = ("d", "day", "days")
    rawsince = since.content
    
    
    try:
        temp = re.compile("([0-9]+)([a-zA-Z]+)")
        if not temp.match(since.content):
            return await ctx.send("You did not specify a unit of time, please try again.")

        res = temp.match(since.content).groups()
        time = int(res[0])
        since = res[1]
        
    except ValueError:
        return await ctx.send("You did not specify a unit of time, please try again.")
        
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
        
        return await ctx.send("You did not specify a unit of time, please try again.")
        
    await ctx.send("What would you like the prize to be?")
    try:
        msg4 = await bot.wait_for('message', check = check, timeout=30.0)


    except asyncio.TimeoutError:
        await ctx.send("You took to long, please try again.")


    logembed = discord.Embed(title="Giveaway Logged",
                             description=f"**Prize:** ``{msg4.content}``\n**Winners:** ``{winerscount}``\n**Channel:** {giveawaychannel.mention}\n**Host:** {ctx.author.mention}",
                             color=discord.Color.red())
    logembed.set_thumbnail(url=ctx.author.avatar_url)

    guild = client.get_guild(796081913688883240)  # Put your guild ID here!
    logchannel = guild.get_channel(799722523054833664)  # Put your channel, you would like to send giveaway logs to.
    await logchannel.send(embed=logembed)

    futuredate = datetime.utcnow() + timedelta(seconds=timewait)
    embed1 = discord.Embed(color = discord.Color(random.randint(0x000000, 0xFFFFFF)), title=f"🎉GIVEAWAY🎉\n`{msg4.content}`",timestamp = futuredate, description=f'React with 🎉 to enter!\nHosted by: {ctx.author.mention}')
    
    embed1.set_footer(text=f"Giveaway will end")
    msg = await giveawaychannel.send(embed=embed1)
    await msg.add_reaction("🎉")
    await asyncio.sleep(timewait)
    message = await giveawaychannel.fetch_message(msg.id)
    for reaction in message.reactions:
        if str(reaction.emoji) == "🎉":
            users = await reaction.users().flatten()
            if len(users) == 1:
                return await msg.edit(embed=discord.Embed(title="Nobody has won the giveaway."))
                
    try:
        winners = random.sample([user for user in users if not user.bot], k=winerscount)
    except ValueError:
        return await giveawaychannel.send("not enough participants")
    
    winnerstosend = "\n".join([winner.mention for winner in winners])
    
    


    win = await msg.edit(embed = discord.Embed(title = "WINNER" , description = f"Congratulations {winnerstosend}, you have won **{msg4.content}**!" , color = discord.Color.blue()))
    
    print(Fore.GREEN + winnerstosend , Fore.WHITE + "has won: " , Fore.GREEN + msg4.content)
    print(Style.RESET_ALL)

    
    
# Reroll command, used for chosing a new random winner in the giveaway
@bot.command()
@commands.has_permissions(manage_guild = True)
async def reroll(ctx):
    async for message in ctx.channel.history(limit=100 , oldest_first = False):
        if message.author.id == bot.user.id and message.embeds:
            reroll = await ctx.fetch_message(message.id)
            users = await reroll.reactions[0].users().flatten()
            
            users.pop(users.index(bot.user))
            winner = random.choice(users)
            
            await ctx.send(f"The new winner is {winner.mention}")
            
            print(Fore.WHITE + 'The new winner is' , Fore.GREEN + winner) # Print's the winner to terminal | Optional
            print(Fore.WHITE + "The prize was: " , Fore.GREEN + msg4.content) # Prints the prize to the giveaway | Optional
            print(Style.RESET_ALL)

            
            break
    else:
        await ctx.send("No giveaways going on in this channel.")
        
# Upcoming commands.
        
        
# Pickwinner / Rigged Giveaway Command.
@bot.command(aliases = ['pick' , 'rig' , 'rigged'])
@commands.has_permissions(manage_guild = True)

async def pickwinner(ctx , user: discord.Member = None):
    
    await ctx.send("Who would you like to be the winner?")
    
@bot.command()
@commands.has_permissions(manage_roles = True)
async def g(ctx , winners , time , prize):
    await ctx.send(f"Giveaway for {prize}, has been started with {winners}, and time has been set to {time}.\nGiveaway started by: {ctx.author.mention}")
    
    
#
        
        
    

    
# Utility / Extra Commands.
@bot.command()
async def ping(ctx):
    ping = bot.latency
    await ctx.send(f"The bot's ping is: ``{round(ping * 1000)}ms``!")


    
    
    
# Command Error Events.
@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"ERROR: Hello {ctx.author}, it seems you have encountered an error.\nYou are missing the following permissions: ``Manage Roles``\nYou cannot create a giveaway without theese permissions.")
        print(Fore.WHITE + ctx.author , 'encountered an error:\n' , Fore.RED + 'Missing Permissions\n' , Fore.WHITE + "Command:" , Fore.GREEN + 'Giveaway [SIMPLE]')

@reroll.error
async def reroll_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"ERROR: Hello {ctx.author}, it seems you have encountered an error.\nYou are missing the following permissions: ``Manage Server``\nYou cannot reroll the giveaway without theese permissions.")
        print(Fore.WHITE + ctx.author , 'encountered an error:\n' , Fore.RED + 'Missing Permissions\n' , Fore.WHITE + "Command:" , Fore.GREEN + 'Reroll')



# Error messages for commands coming soon.


#@g.error
#async def g_error(ctx, error):
    #if isinstance(error, MissingPermissions):
        #await ctx.send(f"ERROR: Hello {ctx.author}, it seems you have encountered an error.\nYou are missing the following permissions: ``Manage Roles``\nYou cannot start a giveaway without theese permissions.")
        #print(Fore.WHITE + ctx.author , 'encountered an error:\n' , Fore.RED + 'Missing Permissions\n' , Fore.WHITE + "Command:" , Fore.GREEN + #'Giveaway [ADVANCED]')

#@pickwinner.error
#async def pickwinner_error(ctx, error):
    #await ctx.send(f"ERROR: Hello {ctx.author}, it seems you have encountered an error.\nYou are missing the following permissions: #``Manage Server``\nYou cannot pick the winner of the giveaway without theese permissions.")
#print(Fore.WHITE + ctx.author , 'encountered an error:\n' , Fore.RED + 'Missing Permissions\n' , Fore.WHITE + "Command:" , Fore.GREEN + 'Giveaway [ADVANCED]')


        
    
    
    
    

    







# Events
@bot.event
async def on_ready():

    print(Fore.RED + 'Logged in as')
    print(Fore.GREEN + bot.user.name)
    print(Style.RESET_ALL)
bot.run(token)
