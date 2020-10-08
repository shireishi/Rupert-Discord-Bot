import ast
import asyncio
import datetime
import getpass
import io
import json
import math
import os
import platform
import random
import sys
import threading
import time
import urllib
from operator import attrgetter, itemgetter
from random import choice
import discord
import youtube_dl
from colorthief import ColorThief
from discord.ext import commands, tasks
from discord.utils import get
from discord.voice_client import VoiceClient
from info import Info
from youtube_search import YoutubeSearch
from commandHandler import discordCommandHandler

token = ""

with open('token.token', 'r') as file:
    token += str(file.read())

prefix = '$'
I = Info()
rupertColor = 0xFF4500 #0xfa9e1e

bot = commands.Bot(command_prefix=prefix)
client = discord.Client()

dch = discordCommandHandler()

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'Videos/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

queueList = {}
qIds = []
list = []
sleepDuration = 0

try:
    bot.remove_command('help')

    def listtostring(s):
        str1 = " "
        return (str1.join(s))

    def argToId(args):
        listid = []
        for i in args:
            listid.append(i)

        if listid[2] == '!':
        
            listid[0] = ''
            listid[1] = ''
            listid[2] = ''
            listid[len(listid)-1] = ''
            userId = ''.join(listid)
            
        else:
            
            listid[0] = ''
            listid[1] = ''
            listid[len(listid)-1] = ''
            userId = ''.join(listid)

        return userId

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    def durtosec(duration):
        test = duration.split(":")
        min = int(test[0]) * 60
        return min + int(test[1])

    def personalColor(*userIds):

        if userIds:
            for userId in userIds:

                userObj = bot.get_user(int(userId))
                req = urllib.request.Request(userObj.avatar_url, headers={'User-Agent':'Magic Browser'}, origin_req_host=None, unverifiable=False, method=None)
                con = urllib.request.urlopen(req)
                color_thief = ColorThief(con)
                dominant_color = color_thief.get_color(quality = 20)

                log = []
                for i in range(len(dominant_color)):
                    log.append(dominant_color[i])
                    rgb_to_hex(dominant_color)
                    toReturn = int("0x{}".format(rgb_to_hex(dominant_color)), 0)
                    return toReturn
        else:
            print("An unknown error has occured.")


    class CommandErrorHandler(commands.Cog):
        """
        https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
        """
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_command_error(self, ctx, error):
            embed = discord.Embed(
                title = "Error",
                description = "You encountered an error :\n{}".format(error),
                color = 0xff0000
            )
            await ctx.send(embed = embed)

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=1):
            super().__init__(source, volume)

            self.data = data

            self.title = data.get('title')
            self.url = data.get('url')

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]

            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    def setup():
        # bot.add_cog(CommandErrorHandler(bot))
        dch.new_command(name = "Resume", description = "Resumes the paused audio on music mode.")
        dch.new_command(name = "Stop", description = "Stops the entire audio track currently playing in music mode.")
        dch.new_command(name = "Join", description = "Invites Rupert to join the user's voice channel.")
        dch.new_command(name = "Leave", description = "Tells Rupert to leave the current voice channel.")
        dch.new_command(name = "Play", description = "Plays the first result on youtube of the parameters your provide or skips to the next song if no search terms are provided.")
        dch.new_command(name = "Skip", description = "Skips to the next song in the queue.")
        dch.new_command(name = "Pause", description = "Pauses the currently playing audio.")
        dch.new_command(name = "Clearq", description = "Clears the queue of any and all songs.")
        dch.new_command(name = "Queue", description = "Displays the queue.")
        dch.new_command(name = "Ping", description = "Pings Rupert's main server then displays the response time.")
        dch.new_command(name = "Ava", description = "Displays the avatar of the current user if no mention is provided, however, if added, a mention will display that users profile picture.")
        dch.new_command(name = "Hello", description = "Displays a simple greeting.")
        dch.new_command(name = "Info", description = "Displays guild information.")
        dch.new_command(name = "Clear", description = "Has the ability to clear entire channels with the term `all`, if no numerical value is provided.")
        dch.new_command(name = "Help", description = "Displays this screen. **Doi**")
        dch.new_command(name = "Announce", description = "Announces a message within an embed.")
        dch.new_command(name = "Age", description = "Displays the date an account was created.")
        dch.new_command(name = "Rep", description = "Displays reputation value.")
        dch.new_command(name = "Boop", description = "Boops the mentioned user.")
        dch.new_command(name = "Smack", description = "Smacks the mentioned user.")
        dch.new_command(name = "Leaderboard", description = "Displays the users with the highest reputation.")
        dch.new_command(name = "Goodbye", description = "Simple farewell.")
        dch.new_command(name = "Hug", description = "Hugs the mentioned user.")
        dch.new_command(name = "Kiss", description = "Kisses the mentioned user.")
        dch.new_command(name = "Rupertinfo", description = "Displays information about Rupert.")
        dch.new_command(name = "Shoot", description = "Shoots the mentioned user.")
        dch.new_command(name = "Creator", description = "Displays information on the creator of Rupert.")
        dch.new_command(name = "Compliment", description = "Something to make your day a little better.")


    @bot.command()
    async def resume(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.resume()

    @bot.command()
    async def stop(ctx):
        global sleepDuration
        sleepDuration = 0
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.stop()
        await voice_channel.disconnect()

    
    @bot.command()
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return
    
        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

    @bot.command()
    async def debug(ctx):
        await ctx.send(qIds)

    @bot.command()
    async def play(ctx, *args):
        if not ctx.message.author.voice:
            await join(ctx)
        #local variables
        global queueList
        global sleepDuration

        server = ctx.message.guild
        voiceChannel = server.voice_client

        if args and ctx.message.author.voice:

            keywords = listtostring(args)
            results = ast.literal_eval(str(YoutubeSearch(keywords, max_results=1).to_dict()))
            # print(results)
            test = results
            # print(test[0])
            queueList[test[0]['id']] = {}
            queueList[test[0]['id']]['id'] = test[0]['id']
            queue = queueList[test[0]['id']]
            queue['id'] = test[0]['id']
            vidId = queueList[test[0]['id']]['id']
            qIds.append(vidId)
            queue['thumbnail_url'] = test[0]['thumbnails'][0]
            queue['title'] = test[0]['title']
            queue['url'] = "https://www.youtube.com/watch?v={}".format(vidId)
            queue['duration'] = test[0]['duration']
            print(sleepDuration)

            try: 
                async with ctx.typing():
                    player = await YTDLSource.from_url(str(queueList[test[0]['id']]['url']), loop=client.loop)
                    await ctx.send("`{}` added to the queue!".format(test[0]['title']))
                    voiceChannel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    nowPlaying = discord.Embed(
                        title = "Now playing",
                        description = "Now playing **{}**".format(queueList[qIds[0]]['title']),
                        color = rupertColor
                    )
                    nowPlaying.add_field(name = "Duration", value = queue['duration'], inline = True)
                    nowPlaying.add_field(name = "ID", value = queue['id'], inline = True)
                    nowPlaying.set_thumbnail(url=queueList[qIds[0]]['thumbnail_url'])

                    await ctx.send(embed = nowPlaying)
                sleepDuration = int(durtosec(str(queue['duration'])))
                del(qIds[0])
                await asyncio.sleep(sleepDuration)
                if qIds:
                    await play(ctx)
                else:
                    await ctx.send("The queue has been depleted.")
            except:
                pass

        else:
            voiceChannel.stop()
            if qIds:
                async with ctx.typing():
                    player = await YTDLSource.from_url(queueList[qIds[0]]['url'], loop=client.loop)
                    voiceChannel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    nowPlaying = discord.Embed(
                        title = "Now playing",
                        description = "Now playing **{}**".format(queueList[qIds[0]]['title']),
                        color = rupertColor
                    )
                    nowPlaying.add_field(name = "Duration", value = queueList[qIds[0]]['duration'], inline = True)
                    nowPlaying.add_field(name = "ID", value = queueList[qIds[0]]['id'], inline = True)
                    nowPlaying.set_thumbnail(url=queueList[qIds[0]]['thumbnail_url'])
                    await ctx.send(embed = nowPlaying)
                sleepDuration = 0
                sleepDuration = int(durtosec(str(queueList[qIds[0]]['duration'])))
                del(qIds[0])
                await asyncio.sleep(sleepDuration)
                if qIds:
                    await play(ctx)
                else:
                    await ctx.send("The queue has been depleted.")
            else:
                await ctx.send("Please add a song to the queue.")
                

    @bot.command()
    async def pause(ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.pause()

    @bot.command()
    async def skip(ctx):
        await play(ctx)

    @bot.command()
    async def clearq(ctx):
        global queueList
        qIds = []
        await ctx.send("Cleared the queue.")

    @bot.command()
    async def queue(ctx):
        global list
        if qIds:
            for i in qIds:
                list.append(queueList[i]['title'])
            await ctx.send('Your queue is:\n`{}`!'.format("\n".join(list)))
        else:
            await ctx.send("Your queue is emtpy.")

    @bot.command()
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @bot.command()
    async def ping(ctx):
        await ctx.send("**PONG!** ({}ms)".format(round(client.latency * 1000)))

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for the prefix {}".format(prefix)))
        print("{} is running on a {} system by {}".format(__file__, platform.system(), getpass.getuser()))
        setup()

    @bot.command()
    async def ban (ctx, member:discord.User=None, reason =None):
        if ctx.message.author.guild_permissions.administrator:
            if member == None or member == ctx.message.author:
                await ctx.channel.send("You cannot ban yourself")
                return

            if reason == None:
                reason = "For being a jerk!"

            message = "You have been banned from {} for {}".format(ctx.guild.name, reason)
            await member.send(message)
            await member.send("https://tenor.com/view/real-thor-thor-fight-gif-7320950")
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"{member} is banned!")

    @bot.command()
    async def unban(ctx, *, member):
        if ctx.message.author.guild_permissions.administrator:
            banned_users = await ctx.guild.bans()
            
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.channel.send(f"Unbanned: {user.mention}")

    @bot.command()
    async def ava(ctx, *user):
        if user:
            
            for args in user:
                
                if args.startswith('<@!') and args.endswith('>'):
                    args = args[3:len(args)-1]
                elif args.startswith('<@') and args.endswith('>'):
                    args = args[2:len(args)-1]
                
                embed = discord.Embed(
                    title = "Avatar of {}".format(bot.get_user(int(args)).name),
                    description = "",
                    color = personalColor(args)
                )
                embed.set_image(url=bot.get_user(int(args)).avatar_url)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = "Avatar of {}".format(ctx.author.name),
                description = "",
                color = personalColor(ctx.author.id)
            )
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            
    @bot.command()
    async def hello(ctx):
        print("{0.author.name} used the hello command.".format(ctx))
        await ctx.send("Hello, {0.author.mention}!".format(ctx))

    @bot.command()
    async def info(ctx):
        print("{0.author.name} used the info command.".format(ctx))
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(

            title = name + "'s\n Server Information : ",
            color=rupertColor

            )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

    @bot.command()
    async def tts(ctx):
        print("{0.author.name} used the developer tts command.".format(ctx))
        await ctx.send("hehe haha uh oh stinky", tts=True, delete_after=0.01)

    @bot.command()
    async def clear(ctx, *args):
        if ctx.message.author.guild_permissions.administrator:
            
            for i in args:
                if i in ['all', 'All'] and ctx.message.author.id == 230895739784396800:
                    await ctx.channel.purge(limit=None)
                    #    time.sleep(1)
                    await ctx.send("All messages were deleted.", delete_after=0.5)
                    
                elif args:
                    amount = int(i)
                    await ctx.channel.purge(limit=amount+1)
                    # time.sleep(1)
                    await ctx.send("{} messages were cleared.".format(amount), delete_after=0.5)
            time.sleep(0.5)
            print("{0.author} cleared the {0.channel} channel.".format(ctx))
        else:
            await ctx.send(embed = discord.Embed(
                title="Error",
                description="Sorry but it appears you do not have the permissions to run that command. Contact the developer with the {}report command or a server administrator.".format(prefix),
                color=0xff0000
            ))  

    @bot.command()
    async def help(ctx, *args):
        commDict = dch.ret_comm()

        embed = discord.Embed(
            title = "Help Menu",
            color = rupertColor
        )
        for i in dch.dict_keys(dch.ret_comm()):
            embed.add_field(name=i, value=commDict[i], inline=False)
        await ctx.message.author.send(embed = embed)
                    
    @bot.command()
    async def report(ctx, *args, **kwargs):
        print("{0.author.name} used the report command.".format(ctx))
        await ctx.send("Report has been uploaded.")
        with open("Logs/reported.txt", "a") as file:
            file.write("\n" + str(args) + "\n")
            
    @bot.command()
    async def database(ctx):
        log = []
        with open('Logs/reputation.log', 'r') as file:
            dict = ast.literal_eval(file.read())
            for i in dict:
                log.append("{} : {}\n".format(dict[i]['name'], dict[i]['rep']))
            
        await ctx.send("".join(log))
        
    @bot.command()
    async def announce(ctx, *args):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.message.delete()
            log = []
            
            if args:
                
                for arg in args:
                    log.append(arg)
                msg = listtostring(log)
                embed=discord.Embed(
                    title="Announcement", 
                    description="@everyone This information may pretain to you, therefore you should read it in it's entirety.", 
                    color=0xff0000)
                
                embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                embed.add_field(name="From {}:".format(ctx.author.name), value=msg, inline=True)
                embed.set_footer(text="{}".format(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                    
            else:
                await ctx.send("Please provide the information for the announcment")    

    @bot.command()
    async def test(ctx, *args):
        sleepDuration = 15
        await asyncio.sleep(sleepDuration)
        await announce(ctx, "yes")
                    
    @bot.command()
    async def age(ctx, *args):
        
        if ctx.message.author.guild_permissions.administrator:
            
            if args:
                for Id in args:
                    # print(Id)
                    edit = str(Id)
                
                    listid = list(edit)
                    if listid[2] == '!':
                    
                        listid[0] = ''
                        listid[1] = ''
                        listid[2] = ''
                        listid[len(listid)-1] = ''
                        userId = ''.join(listid)
                        
                    else:
                        
                        listid[0] = ''
                        listid[1] = ''
                        listid[len(listid)-1] = ''
                        userId = ''.join(listid)
            else:
                userId = ctx.author.id
                
            cli = ctx.message.guild.get_member(int(userId))
            
            embed=discord.Embed(
                title="Age of User",
                description="The date {} was created at is >> {}".format(cli.mention, cli.created_at),
                color=rupertColor)
            
            embed.set_thumbnail(url=cli.avatar_url)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed = discord.Embed(
                title="Error",
                description="Sorry but it appears you do not have the permissions to run that command. Contact the developer with the {}report command or a server administrator.".format(prefix),
                color=0xff0000
            ))    

    @bot.command()
    async def rep(ctx, *arg):
        await ctx.trigger_typing()
        if arg: #tests if there was a user mention
            for args in arg:
                
                userId = argToId(args) #converts the mention to an actual user id

                with open('Logs/reputation.log', 'r') as file:
                    
                    #definition of variables
                    dict = ast.literal_eval(file.read())
                    userObj = bot.get_user(int(userId))
                    serverId = ctx.guild.id
                    rep = dict[str(serverId)][str(userId)]
                    persCol = personalColor(userId)

                    embed = discord.Embed(
                        title = "Reputation value of {}".format(ctx.guild.get_member(int(userId)).display_name),
                        description = "{}'s reputation is:\n>> {} <<".format(userObj.mention, rep),
                        color = persCol
                    )
                    
                    if int(rep) == 0:
                        level = 0
                    elif rep < 150:
                        level = 0
                    else:
                        level = math.floor(rep/150)

                    dict = dict[str(ctx.guild.id)]
                    sort = sorted(dict, key=lambda x: dict[x], reverse=True)
                    
                    embed.set_thumbnail(url=userObj.avatar_url)
                    embed.add_field(name="Level", value="Level {} nerd".format(level), inline=True)
                    embed.add_field(name = "Rank", value="{}".format(int(sort.index(userId))+1), inline = True)
                    await ctx.send(embed = embed)

        else:
            with open('Logs/reputation.log', 'r') as file:
                dict = ast.literal_eval(file.read())
                userId = ctx.author.id
                serverId = ctx.guild.id
                rep = dict[str(serverId)][str(userId)]

                embed = discord.Embed(
                    title = "Reputation Value of {}".format(ctx.author.display_name),
                    description = "{}'s reputation:\n>> {} <<".format(ctx.author.mention, rep),
                    color = personalColor(userId)
                )
                
                if int(rep) == 0:
                    level = 0
                elif rep < 150:
                    level = 0
                else:
                    level = math.floor(rep/150)

                dict = dict[str(ctx.guild.id)]
                sort = sorted(dict, key=lambda x: dict[x], reverse=True)
                
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name="Level", value="Level {} nerd".format(level))
                embed.add_field(name = "Rank", value="{}".format(int(sort.index(str(ctx.author.id))+1)), inline = True)
                await ctx.send(embed = embed)

    @bot.command()
    async def example(ctx):

        embed1 = discord.Embed(
            title="This is an example",
            description = "This is the example with the majority color from your profile picture.",
            color = personalColor(ctx)
        )
        embed2 = discord.Embed(
            title = "This is an example",
            description = "This is the normal color.",
            color = rupertColor
        )
        embed1.set_thumbnail(url = ctx.author.avatar_url)
        embed2.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed = embed1)
        await ctx.send(embed = embed2)

    @bot.command()
    async def boop(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " booped " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")
                
    @bot.command()
    async def smack(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " smacked " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")
            
    @bot.command()
    async def readreports(ctx):
        
        with open('Logs/reported.txt', 'r') as file:
            await ctx.send(file.read())
            
    @bot.command()
    async def leaderboard(ctx):
        with open('Logs/reputation.log', 'r') as file:
            dict = ast.literal_eval(file.read())
            dict = dict[str(ctx.guild.id)]
            sort = sorted(dict, key=lambda x: dict[x], reverse=True) #lambda x: (dict[str(ctx.guild.id)][x])
            # st = sort[0]
            # nd = sort[1]
            # rd = sort[2]
            if ctx.message.guild.get_member(int(sort[0])):
                st = ctx.message.guild.get_member(int(sort[0]))
            else:
                st = bot.get_user(int(sort[0]))
                
            if ctx.message.guild.get_member(int(sort[1])):
                nd = ctx.message.guild.get_member(int(sort[1]))
            else:
                nd = bot.get_user(int(sort[1]))
                
            if ctx.message.guild.get_member(int(sort[2])):
                rd = ctx.message.guild.get_member(int(sort[2]))
            else:
                rd = bot.get_user(int(sort[2]))
            
            if st != 'Error':
                embed1 = discord.Embed(
                    title="1st Place is",
                    description="{}\nWith a reputation of **{}**".format(st.mention, dict[sort[0]]),
                    color=0xDAA520
                )
            else:
                embed1 = discord.Embed(
                    title="1st Place is",
                    description="{}\nWith a reputation of **{}**".format(st.name, dict[sort[0]]),
                    color=0xDAA520
                )
            if nd != 'Error':
                embed2 = discord.Embed(
                    title="2nd Place is",
                    description="{}\nWith a reputation of **{}**".format(nd.mention, dict[sort[1]]),
                    color=0xC0C0C0
                )
            else:
                embed2 = discord.Embed(
                    title="2nd Place is",
                    description="{}\nWith a reputation of **{}**".format(nd.name, dict[sort[1]]),
                    color=0xC0C0C0
                )
            if rd != 'Error':
                embed3 = discord.Embed(
                    title="3rd Place is",
                    description="{}\nWith a reputation of **{}**".format(rd.mention, dict[sort[2]]),
                    color=0xCD7F32
                )
            else:
                embed3 = discord.Embed(
                    title="3rd Place is",
                    description="{}\nWith a reputation of **{}**".format(rd.name, dict[sort[2]]),
                    color=0xCD7F32
                )
                # embed1.add_field(name="1st Place : ", value=st.mention, inline=False)
            embed1.set_thumbnail(url=st.avatar_url)
            # embed2.add_field(name="2nd Place : ", value=nd.mention, inline=False)
            embed2.set_thumbnail(url=nd.avatar_url)
            # embed3.add_field(name="3rd Place : ", value=rd.mention, inline=False)
            embed3.set_thumbnail(url=rd.avatar_url)
            
            # await ctx.send(embed=embed)
            await ctx.send(embed=embed1)
            await ctx.send(embed=embed2)
            await ctx.send(embed=embed3)

    @bot.command()
    async def goodbye(ctx):
        await ctx.send("Goodbye, {}".format(ctx.message.author.mention))
        
    @bot.command()
    async def hug(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " hugged " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")
                       
    @bot.command()
    async def kiss(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " kissed " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")
        
    @bot.command()
    async def say(ctx, *description):
        await ctx.message.delete()
        log = []
        if ctx.message.author.id == 230895739784396800 or ctx.message.author.id == 259063263604506634:
            if description:
                for i in range(len(description)):

                    log.append(description[i])

                desc = listtostring(log)
            await ctx.send(desc)
        else:
            await ctx.send("Wait.. You're not Elly...")
            
    @bot.command()
    async def nice(ctx, *val):
        if ctx.message.author.guild_permissions.administrator:
            if val:
                for i in val:
                    for j in range(int(i)):
                        time.sleep(0.1)
                        await ctx.send("nice")
            else:
                for i in range(5):
                    time.sleep(0.1)
                    await ctx.send("nice")
        else:
            embed = discord.Embed(
                title="Error",
                description="You do not have the permission to use that command.",
                color=0xff0000
            )
            await ctx.send(embed = embed)
            
    @bot.command()
    async def shutdown(ctx):
            if ctx.message.author.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Smooth Shutdown Completed",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                quit()
            else:
                await ctx.send("Ye nah m8")
            
    @bot.command()
    async def rupertinfo(ctx):
        embed = discord.Embed(
            title="Rupert Info",
            description="The Rupert Reputation Bot is a discord bot coded in Python 3.8.5 designed to keep track of user activity and plays music. Use `help` for more information.",
            color=rupertColor
        )
        embed.add_field(name="Creator", value=ctx.message.guild.get_member(230895739784396800).mention, inline=False)
        embed.set_thumbnail(url=ctx.message.guild.get_member(746504617507946705).avatar_url)
        
        await ctx.send(embed=embed)
            
    @bot.command()
    async def shoot(ctx, name):
        await ctx.message.delete()
        if name:
            if "746504617507946705" in name:
                await ctx.send(ctx.author.mention + " shot " + name)
                time.sleep(1)
                await ctx.send("Oof I've been shot!")
            elif name[0] == '<':
                await ctx.send(ctx.author.mention + " shot " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")

    @bot.command()
    async def creator(ctx):
        embed=discord.Embed(title="Elara Jade Instagram", description="The creator of the Rupert Reputation Bot.", url="https://www.instagram.com/eelly.babyy/", icon_url="https://instagram.fdsm1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/118418251_133125831817344_3804973025633608966_n.jpg?_nc_ht=instagram.fdsm1-1.fna.fbcdn.net&_nc_ohc=U4Fks8ohmhgAX9q2a7e&oh=c4cb9cdc6124ae7f0e9b689e57071737&oe=5F7BB1A0", color=0xa088f6)
        embed.set_author(name="Elara Jade GitHub", url="https://github.com/shireishi", icon_url="https://avatars0.githubusercontent.com/u/63125641?s=460&u=b13add0e2a2f533ed91b1b57015677f8db15ccb2&v=4")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/745309902154498099/751281921174011934/IMG_20200830_113504_232.png")
        embed.add_field(name="Discord", value=bot.get_user(230895739784396800).mention, inline=False)
        await ctx.send(embed=embed)

    @client.event
    async def on_ready():
        print("Client has logged on as {}.".format(client.user))

    @bot.command()
    async def emojilist(ctx):
        for emoji in ctx.guild.emojis:
            await ctx.send("{0.id} : {0}\n".format(emoji))
            print(discord.Emoji)

    @client.event
    async def on_message(message):

        if message:
            with open("Logs/chat_log.txt", "a") as file:
                file.write("{2} >> {0} : {1}\n".format(message.author, message.content, message.channel))

            print("\033[1;32;40m{0.guild}\033[0;0;0m >> {0.channel} >> \033[1;32;47m{0.author}\033[0;0;0m: \033[1;33;40m{0.content}\033[0;0;0m".format(message))

            if message.author == client.user:
                return
           
            if message.author.guild_permissions.administrator == False and message.content.lower() == '@everyone':
                await message.delete()


            if 'depress' in message.content or 'Depress' in message.content:
                await message.add_reaction(':pog:752983087809560607')

            with open('Logs/reputation.log', 'r') as file:
                dict = ast.literal_eval(file.read())   

                if str(message.guild.id) not in dict:
                    dict[str(message.guild.id)] = {}
                    with open('Logs/reputation.log', 'w') as file:
                        file.write(str(dict))

                if str(message.author.id) in dict[str(message.guild.id)]:
                    dict[str(message.guild.id)][str(message.author.id)] += (random.randint(0, 10))
                    with open('Logs/reputation.log', 'w') as edit:
                        edit.write(str(dict))
                else:
                    running = True
                    while running:
                        dict[str(message.guild.id)][str(message.author.id)] = (random.randint(0, 10))
                        with open('Logs/reputation.log', 'w') as edit:
                            edit.write(str(dict))
                        running = False
   
                            

                        
            if message.content == "$reboot":
                if message.author.id == 230895739784396800:
                    await message.channel.send("Rebooting Rupert Bot....")
                    os.system('cd /home/elara/Desktop/Coding  Projects/Discord-Bot/')
                    os.system('clear')
                    os.system('python3 rupert.py')
                else:
                    await message.channel.send("Wait you're not my creator..")
            # if message.content == "rupert will you date me?":

    @bot.command()
    async def reboot(ctx):
        
        if ctx.author.id == 230895739784396800:
            await ctx.send("Rebooting Rupert Bot....")
            os.system('cd /home/elara/Desktop/Coding  Projects/Discord-Bot/')
            os.system('clear')
            os.system('python3 rupert.py')
        else:
            await ctx.send("Wait you're not my creator..")

    @bot.command()
    async def countdown(ctx):
        
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        seconds = now.second
        
        birthday = datetime.datetime(2020, 9, 8, hour=0, minute=17) - datetime.datetime.today()
        
        await ctx.message.delete()
        
        desc = "It is currently {}:{}:{}MST and there is {} remaining until September 8th, 2020 12:17AM.".format(hour, minute, seconds, birthday)
        
        embed = discord.Embed(
            title="Countdown to Elara's Birthday",
            description=desc,
            color = 0xFF55BB
        )
        
        await ctx.send(embed=embed)

    @bot.command()
    async def userinfo(ctx, *args):
        if ctx.message.author.guild_permissions.administrator:
            if args:
                for arg in args:
                    
                    if arg.startswith('<@!') and arg.endswith('>'):
                        userId = arg[3:len(arg)-1]
                    elif arg.startswith('<@') and arg.endswith('>'):
                        userId = arg[2:len(arg)-1]
                    
                    user = bot.get_user(int(userId))
                    name = user.name
                    mention = user.mention
                    avatarUrl = user.avatar_url
                    description = user.created_at
                    
                    
            else:
                name = ctx.author.name
                mention = ctx.author.mention
                avatarUrl = ctx.author.avatar_url
                description = ctx.author.created_at
                
            embed = discord.Embed(
                title = name,
                description = "Created >> {}\n{}".format(description, mention),
                color = rupertColor
            )
            embed.set_image(url=avatarUrl)
            await ctx.send(embed=embed)

    @bot.command()
    async def compliment(ctx):
        compliments = ["Nice hair.",
            "I like your shirt.",
            "You have a cool music taste.",
            "I am proud of you.",
            "You have a beautiful smile.",
            "You have excellent ideas!",
            "You are very kind.",
            "You make me happy.",
            "It’s a lovely day, and you always make it lovelier.",
            "I like your clothing style!",
            "You’re a splendid person.",
            "If there’s somebody you love, they love you just as much. And if they don’t, I’m always here for you.",
            "You’ve done a good job today, even if it was minimal."]

        await ctx.send(compliments[random.randint(0, len(compliments)-1)])

    # bot.run(token)
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token))
    loop.create_task(client.start(token))
    loop.run_forever()

    #https://stackoverflow.com/questions/62102897/certifacte-verify-failed-certificate-has-expired-ssl-c1108/62104752#62104752?newreg=c7d8fae3b0264f3892ac0036b22f3466
except KeyboardInterrupt:
    print("{} has been forcefully closed.".format(__file__))
