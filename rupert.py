from __future__ import print_function

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
import prawcore
from prawcore import NotFound
import basc_py4chan
import discord
import praw
import psutil
import youtube_dl
from colorthief import ColorThief
from commandHandler import discordCommandHandler
from discord.ext import commands, tasks
from discord.utils import get
from discord.voice_client import VoiceClient
from info import Info
from youtube_search import YoutubeSearch

# from pypresence import Presence

token = ""

reddit_color = 0xFF4500

four_chan = 0x90ee90

r = praw.Reddit(
        client_id="BbyiCURff-7dDQ",
        client_secret="_l2-lU__aFUVJfSSDq4v-yE_h4mRBQ",
        username="malthaelazrael",
        password="jasper0923",
        user_agent="web-scraper"
        )

with open('token.token', 'r') as file:
    token += str(file.read())

secret = ""

with open('secret.token', 'r') as file:
    secret += str(file.read())

client_id = '746504617507946705'

prefix = 'r!'
I = Info()
rupertColor = 0xFF4500 #0xfa9e1e

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
client = discord.Client()
dch = discordCommandHandler()
# RPC = Presence(client_id)

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
timestamp = 1598050970

try:
    bot.remove_command('help')

    def listtostring(s):
        str1 = "".join(s)
        for i in range(len(str1)):
            if " " == str1[i]:
                str[i] = ""

        return (str1)

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

    def to_list(data):
        temp_list = []
        for i in data:
            temp_list.append(i)
        return temp_list

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

    # async def my_coroutine():
    #     RPC.connect()
    #     print(RPC.update(state="Lookie Lookie", details="A test of qwertyquerty's Python Discord RPC wrapper, pypresence!"))

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

    async def upd():
        # while True :
            # value = datetime.datetime.fromtimestamp(timestamp)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for the prefix {}".format(prefix))) #f"Discord at {round(client.latency * 1000)}ms"
            # print(datetime.datetime.utcfromtimestamp(timestamp))
            # await asyncio.sleep(2)

    @bot.command()
    async def invite(ctx):
        await ctx.send(r"https://discord.com/api/oauth2/authorize?client_id=746504617507946705&permissions=8&redirect_uri=http%3A%2F%2Flocalhost%3A8080&scope=bot")

    def setup():
        # bot.add_cog(CommandErrorHandler(bot))
        # dch.new_command(name = "Resume", description = "Resumes the paused audio on music mode.")
        # dch.new_command(name = "Stop", description = "Stops the entire audio track currently playing in music mode.")
        # dch.new_command(name = "Join", description = "Invites Rupert to join the user's voice channel.")
        # dch.new_command(name = "Leave", description = "Tells Rupert to leave the current voice channel.")
        # dch.new_command(name = "Play", description = "Plays the first result on youtube of the parameters your provide or skips to the next song if no search terms are provided.")
        # dch.new_command(name = "Skip", description = "Skips to the next song in the queue.")
        # dch.new_command(name = "Pause", description = "Pauses the currently playing audio.")
        # dch.new_command(name = "Clearq", description = "Clears the queue of any and all songs.")
        # dch.new_command(name = "Queue", description = "Displays the queue.")
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
    async def poll( ctx, question, *options: str):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.message.delete()
            if len(options) <= 1:
                await ctx.send('You need more than one option to make a poll!')
                return
            if len(options) > 10:
                await ctx.send('You cannot make a poll for more than 10 things!')
                return


            if len(options) == 2 and options[0] in ['yes', 'Yes'] and options[1] in ['no', 'No']:
                reactions = ['✅', '❌']
                
                description = []
                for x, option in enumerate(options):
                    
                    description += '\n {} {}'.format(reactions[x], option)
                embed = discord.Embed(
                    title=question, 
                    description=''.join(description),
                    color=rupertColor
                    )
                embed.set_thumbnail(url=bot.get_user(746504617507946705).avatar_url)
                react_message = await ctx.send(embed=embed)
                for reaction in reactions:
                    await react_message.add_reaction(reaction)
                embed.set_footer(text='Poll ID: {}'.format(react_message.id))
                await react_message.edit(embed=embed)  

            else:
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

                description = []
                for x, option in enumerate(options):
                    
                    description += '\n {} {}'.format(reactions[x], option)
                embed = discord.Embed(
                    title=question, 
                    description=''.join(description),
                    color=rupertColor
                    )
                embed.set_thumbnail(url=bot.get_user(746504617507946705).avatar_url)
                react_message = await ctx.send(embed=embed)
                i = 0
                for reaction in reactions:
                    i+=1
                    await react_message.add_reaction(reaction)
                    if i == len(options):
                        break
                embed.set_footer(text='Poll ID: {}'.format(react_message.id))
                await react_message.edit(embed=embed)
                
                await asyncio.sleep(900)
                
                running = False
                while running:
                    desc = []
                    msg = await ctx.fetch_message(react_message.id)
                    reaction = msg.reactions
                    for i in range(len(reaction)):
                        if reaction and reaction[i].count > 1:
                            desc.append("Reaction >> {} : Ammount >> {}\n".format(reaction[i], reaction[i].count-1))
                    embedRes = discord.Embed(
                        title = "Results of '{}' ({})".format(question, react_message.id),
                        description = "".join(desc),
                        color = rupertColor
                    )
                    embedRes.set_footer(text="Results of Poll {}".format(react_message.id))
                    embedRes.set_thumbnail(url=bot.get_user(746504617507946705).avatar_url)
                    await ctx.send(embed=embedRes)
                    running = False
        else:
            await ctx.send(embed=errBed)
        return ctx, react_message, question
            
    @bot.command()
    async def results(ctx, pollid):
        descr = []
        msg = await ctx.fetch_message(pollid)
        reaction = msg.reactions
        for i in range(len(reaction)):
            if reaction and reaction[i].count > 1:
                descr.append("Reaction >> {} : Ammount >> {}\n".format(reaction[i], reaction[i].count-1))

        embedRes = discord.Embed(
            title = "Results of ({})".format(pollid),
            description = "".join(descr),
            color = rupertColor
        )
        embedRes.set_footer(text="Results of Poll {}".format(pollid))
        embedRes.set_thumbnail(url=bot.get_user(746504617507946705).avatar_url)
        await ctx.send(embed=embedRes)



    @bot.event
    async def on_member_join(member):
        guild = member.guild
        channel = discord.utils.get(guild.channels, name="general")
        await channel.send("Welcome, {}!".format(member.mention))

    @bot.event
    async def on_member_remove(member):
        guild = member.guild
        channel = discord.utils.get(guild.channels, name="general")
        await channel.send("Sad to see you go, {}..".format(member.name))

    @bot.command()
    async def stop(ctx):
        global sleepDuration
        sleepDuration = 0
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.stop()
        await voice_channel.disconnect()

    @bot.command()
    async def cum(ctx, *ment):
        await ctx.message.delete()
        if ment:
            for arg in ment:
                userId = argToId(arg)
                await ctx.send("{} came on {}".format(ctx.author.mention, bot.get_user(int(userId)).mention))
        else:
            await ctx.send("{} came **everywhere**!!".format(ctx.author.mention))

    # @bot.command()
    # async def join(ctx):
    #     if not ctx.message.author.voice:
    #         await ctx.send("You are not connected to a voice channel")
    #         return
    
    #     else:
    #         channel = ctx.message.author.voice.channel

    #     await channel.connect()

    # @bot.command()
    # async def debug(ctx):
    #     await ctx.send(qIds)

    # @bot.command()
    # async def play(ctx, *args):
    #     if not ctx.message.author.voice:
    #         await join(ctx)
    #     #local variables
    #     global queueList
    #     global sleepDuration

    #     server = ctx.message.guild
    #     voiceChannel = server.voice_client

    #     if args and ctx.message.author.voice:

    #         keywords = listtostring(args)
    #         results = ast.literal_eval(str(YoutubeSearch(keywords, max_results=1).to_dict()))
    #         # print(results)
    #         test = results
    #         # print(test[0])
    #         queueList[test[0]['id']] = {}
    #         queueList[test[0]['id']]['id'] = test[0]['id']
    #         queue = queueList[test[0]['id']]
    #         queue['id'] = test[0]['id']
    #         vidId = queueList[test[0]['id']]['id']
    #         qIds.append(vidId)
    #         queue['thumbnail_url'] = test[0]['thumbnails'][0]
    #         queue['title'] = test[0]['title']
    #         queue['url'] = "https://www.youtube.com/watch?v={}".format(vidId)
    #         queue['duration'] = test[0]['duration']
    #         print(sleepDuration)

    #         try: 
    #             async with ctx.typing():
    #                 player = await YTDLSource.from_url(str(queueList[test[0]['id']]['url']), loop=client.loop)
    #                 await ctx.send("`{}` added to the queue!".format(test[0]['title']))
    #                 voiceChannel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #                 nowPlaying = discord.Embed(
    #                     title = "Now playing",
    #                     description = "Now playing **{}**".format(queueList[qIds[0]]['title']),
    #                     color = rupertColor
    #                 )
    #                 nowPlaying.add_field(name = "Duration", value = queue['duration'], inline = True)
    #                 nowPlaying.add_field(name = "ID", value = queue['id'], inline = True)
    #                 nowPlaying.set_thumbnail(url=queueList[qIds[0]]['thumbnail_url'])

    #                 await ctx.send(embed = nowPlaying)
    #             sleepDuration = int(durtosec(str(queue['duration'])))
    #             del(qIds[0])
    #             await asyncio.sleep(sleepDuration)
    #             if qIds:
    #                 await play(ctx)
    #             else:
    #                 await ctx.send("The queue has been depleted.")
    #         except:
    #             pass

    #     else:
    #         voiceChannel.stop()
    #         if qIds:
    #             async with ctx.typing():
    #                 player = await YTDLSource.from_url(queueList[qIds[0]]['url'], loop=client.loop)
    #                 voiceChannel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #                 nowPlaying = discord.Embed(
    #                     title = "Now playing",
    #                     description = "Now playing **{}**".format(queueList[qIds[0]]['title']),
    #                     color = rupertColor
    #                 )
    #                 nowPlaying.add_field(name = "Duration", value = queueList[qIds[0]]['duration'], inline = True)
    #                 nowPlaying.add_field(name = "ID", value = queueList[qIds[0]]['id'], inline = True)
    #                 nowPlaying.set_thumbnail(url=queueList[qIds[0]]['thumbnail_url'])
    #                 await ctx.send(embed = nowPlaying)
    #             sleepDuration = 0
    #             sleepDuration = int(durtosec(str(queueList[qIds[0]]['duration'])))
    #             del(qIds[0])
    #             await asyncio.sleep(sleepDuration)
    #             if qIds:
    #                 await play(ctx)
    #             else:
    #                 await ctx.send("The queue has been depleted.")
    #         else:
    #             await ctx.send("Please add a song to the queue.")
                

    # @bot.command()
    # async def pause(ctx):
    #     server = ctx.message.guild
    #     voice_channel = server.voice_client

    #     voice_channel.pause()

    # @bot.command()
    # async def skip(ctx):
    #     await play(ctx)

    # @bot.command()
    # async def clearq(ctx):
    #     global queueList
    #     qIds = []
    #     await ctx.send("Cleared the queue.")

    # @bot.command()
    # async def queue(ctx):
    #     global list
    #     if qIds:
    #         for i in qIds:
    #             list.append(queueList[i]['title'])
    #         await ctx.send('Your queue is:\n`{}`!'.format("\n".join(list)))
    #     else:
    #         await ctx.send("Your queue is emtpy.")

    # @bot.command()
    # async def leave(ctx):
    #     voice_client = ctx.message.guild.voice_client
    #     await voice_client.disconnect()

    @bot.command()
    async def ping(ctx):
        await ctx.send("**PONG!** ({}ms)".format(round(client.latency * 1000)))

    @bot.event
    async def on_ready():
        print("{} is running on a {} system by {}".format(__file__, platform.system(), getpass.getuser()))
        setup()
        await upd()

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
        await ctx.send("```json\n{}\n".format(dict[str(ctx.guild.id)]))
        
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
                    description="This information may pertain to you, therefore you should read it in it's entirety.", 
                    color=0xff0000)
                
                embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                embed.add_field(name="From {}:".format(ctx.author.name), value=msg, inline=True)
                embed.set_footer(text="{}".format(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.send("@everyone")
                await ctx.send(embed=embed)
                    
            else:
                await ctx.send("Please provide the information for the announcment")    

    @bot.command()
    async def test(ctx, *args):
        embed = discord.Embed(
            title="Not important dont read me",
            color = 0xffffff
        )
        embed.set_image(url=bot.get_user(ctx.author.id).avatar_url)        
        await ctx.send(embed=embed)

                    
    @bot.command()
    async def age(ctx, *args):
        
        if ctx.message.author.guild_permissions.administrator:
            
            if args:
                for Id in args:
                    # print(Id)
                    edit = str(Id)
                
                    listid = to_list(edit)
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
    async def fuck(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " fucked " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")

    @bot.command()
    async def highfive(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " highfived " + name)
            else: 
                await ctx.send("Please provide a valid user mention.")

    @bot.command()
    async def smite(ctx, name):
        await ctx.message.delete()
        if name:
            if name[0] == '<': 
                await ctx.send(ctx.author.mention + " smote " + name)
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
            index = sorted(dict, key=lambda x: dict[x], reverse=True)

            color_list = ['501894', '0070C4', 'F7931E', 'A0B4C8', 'B46030']#'2AD4F8'
            title_list = ['Grand Champion', 'Diamond', 'Gold', 'Silver', 'Bronze']
            suffix_list = ['First', 'Second', 'Third', 'Fourth', 'Fifth',]

            for user in range(len(color_list)):
                print(index[user])
                userobj = bot.get_user(int(index[user]))
                embed = discord.Embed(
                    title = "{}".format(title_list[user]),
                    description = "{} place is {} with a reputation of : \n``{}``".format(suffix_list[user], userobj.mention, dict[index[user]]),
                    color = int('0x{}'.format(color_list[user]), 0)
                )
                embed.set_thumbnail(url=userobj.avatar_url)
                await ctx.send(embed = embed)
                # def comment():
        #     with open('Logs/reputation.log', 'r') as file:
        #         dict = ast.literal_eval(file.read())
        #         dict = dict[str(ctx.guild.id)]
        #         sort = sorted(dict, key=lambda x: dict[x], reverse=True) #lambda x: (dict[str(ctx.guild.id)][x])

        #         st = bot.get_user(int(sort[0]))

        #         print(sort[0])

        #         nd = bot.get_user(int(sort[1]))

        #         print(sort[1])

        #         rd = bot.get_user(int(sort[2]))

        #         print(sort[2])

        #         try:
        #             first_mention = st.mention
        #         except AttributeError:
        #             first_mention = st

        #         try:
        #             second_mention = nd.mention
        #         except AttributeError:
        #             second_mention = nd

        #         try:
        #             third_mention = rd.mention
        #         except AttributeError:
        #             third_mention = rd

        #         print(st)
        #         print(nd)
        #         print(rd)

        #         if st != 'Error':
        #             embed1 = discord.Embed(
        #                 title="1st Place is",
        #                 description="{}\nWith a reputation of **{}**".format(first_mention, dict[sort[0]]),
        #                 color=0xDAA520
        #             )
        #         else:
        #             embed1 = discord.Embed(
        #                 title="1st Place is",
        #                 description="{}\nWith a reputation of **{}**".format(first_mention, dict[sort[0]]),
        #                 color=0xDAA520
        #             )
        #         if nd != 'Error':
        #             embed2 = discord.Embed(
        #                 title="2nd Place is",
        #                 description="{}\nWith a reputation of **{}**".format(second_mention, dict[sort[1]]),
        #                 color=0xC0C0C0
        #             )
        #         else:
        #             embed2 = discord.Embed(
        #                 title="2nd Place is",
        #                 description="{}\nWith a reputation of **{}**".format(second_mention, dict[sort[1]]),
        #                 color=0xC0C0C0
        #             )
        #         if rd != 'Error':
        #             embed3 = discord.Embed(
        #                 title="3rd Place is",
        #                 description="{}\nWith a reputation of **{}**".format(third_mention, dict[sort[2]]),
        #                 color=0xCD7F32
        #             )
        #         else:
        #             embed3 = discord.Embed(
        #                 title="3rd Place is",
        #                 description="{}\nWith a reputation of **{}**".format(third_mention, dict[sort[2]]),
        #                 color=0xCD7F32
        #             )
        #             # embed1.add_field(name="1st Place : ", value=st.mention, inline=False)
        #         embed1.set_thumbnail(url=st.avatar_url)
        #         # embed2.add_field(name="2nd Place : ", value=nd.mention, inline=False)
        #         embed2.set_thumbnail(url=nd.avatar_url)
        #         # embed3.add_field(name="3rd Place : ", value=rd.mention, inline=False)
        #         embed3.set_thumbnail(url=rd.avatar_url)
                
        #         # await ctx.send(embed=embed)
        #         await ctx.send(embed=embed1)
        #         await ctx.send(embed=embed2)
        #         await ctx.send(embed=embed3)
        
            
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
                    if int(i) <= 20:
                        for j in range(int(i)):
                            time.sleep(0.1)
                            await ctx.send("nice")
                    else:
                        await ctx.send("Ye nah m8.")
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
            description="The Rupert Reputation Bot is a discord bot coded in Python 3.8.5 designed to keep track of user activity and interact with the environment. Use `{}help` for more information.".format(prefix),
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
            #\033[1;32;47m
            print("\033[1;32;40m{0.guild}\033[0;0;0m >> {0.channel} >> \033[1;32;40m{0.author}\033[0;0;0m: \033[1;33;40m{0.content}\033[0;0;0m".format(message))

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
        
        birthday = datetime.datetime(2021, 9, 8, hour=0, minute=17) - datetime.datetime.today()
        
        await ctx.message.delete()
        
        desc = "It is currently {}:{}:{}MST and there is {} remaining until September 8th, 2021 12:17AM.".format(hour, minute, seconds, birthday)
        
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

    @bot.command()
    async def ratehorny(ctx, *ment):
        if ment:
            for arg in ment:
                userId = argToId(arg)
                # print(userId)
                user = bot.get_user(int(userId))
                embed = discord.Embed(
                    title = "Horny Level",
                    description = "You are " + str(random.randint(0, 100)) + "%" + " horny, {}".format(user.mention),
                    color = rupertColor
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "Horny Level",
                description = "You are " + str(random.randint(0, 100)) + "%" + " horny, {}".format(ctx.author.mention),
                color = rupertColor
            )
            await ctx.send(embed = embed)

    @bot.command()
    async def setrep(ctx, amt, *ment):
        if ctx.author.id == 230895739784396800:
            if ment:
                for arg in ment:
                    user = bot.get_user(int(argToId(arg)))
                    with open('Logs/reputation.log', 'r') as file:
                        dict = ast.literal_eval(file.read())
                        user_val = dict[str(ctx.guild.id)]
                        try:
                            user_val[str(user.id)] = int(amt)
                            with open('Logs/reputation.log', 'w') as file2:
                                file2.write(str(dict))
                            await ctx.send("Reputation value for {} now set to {}".format(user.mention, amt))
                        except:
                            await ctx.send("Failed to convert provided value to a base 10 integer.")
            else:
                with open('Logs/reputation.log', 'r') as file:
                    dict = ast.literal_eval(file.read())
                    user_val = dict[str(ctx.guild.id)]
                    try :
                        user_val[str(ctx.author.id)] = int(amt)
                        with open('Logs/reputation.log', 'w') as file2:
                            file2.write(str(dict))
                        await ctx.send("Reputation value for {} now set to {}".format(ctx.author.mention, amt))

                    except :
                        await ctx.send("Failed to convert provided value to a base 10 integer.")
        else :
            await ctx.send("You do not have the permission to use this command.")
    

    @bot.command()
    async def rupertlength(ctx):
        with open('rupert.py', 'r') as file:
            await ctx.send("Rupert's main Python file is now {} characters in length.".format(len(file.read())))

    @bot.command()
    async def advice(ctx):
        advice = ["Never give up!", "Keep your friends close and your loved ones closer", "Sub to il-HOPE-li on youtube-", "Be kind to those around you.", "True intelligence is knowing you know nothing."]
        await ctx.send(advice[random.randint(0, len(advice)-1)])

    def sub_exists(sub):
        exists = True
        try:
            r.subreddits.search_by_name(sub, exact=True)
        except:
            exists = False
        return exists

    @bot.command()
    async def reddit(ctx, subreddit):
        await ctx.trigger_typing()
        red_list = {}
        string = ""
        i = 0
        NSFW = False

        subreddit_name = subreddit.split("/")[1]

        subred = r.subreddit(subreddit_name)
        
        sub_object = subred.new(limit=50)
        try:
            print(sub_object)
            if sub_exists(subreddit_name) == True:
                for post in sub_object:
                    
                    for values in post.comments:
                        for comment in values.body:
                            string += comment

                    if subred.over18:
                        NSFW = True

                    for post in sub_object:
                        red_list[i] = {"title":post.title,"description":string,"url":post.url}
                        i += 1

                    reddit = random.randint(0, len(red_list)-1)

                    print(red_list)
                    print(reddit)
                    print(red_list[reddit])

                    title = red_list[reddit]["title"]
                    url = red_list[reddit]["url"]
                    description = red_list[reddit]["description"]

                    print(dir(post))

                    if len(string) > 2000:
                        embed = discord.Embed(
                            title = "from {} >> {}".format(subreddit, title),
                            color=reddit_color
                        )
                        await ctx.send(embed=embed)
                        await ctx.send(string[0:2000])
                    else:    
                        if string:
                            if ctx.channel.is_nsfw():
                                if NSFW == True:
                                    embed = discord.Embed(
                                        title ="from {} >> {}".format(subreddit, title),
                                        description=string,
                                        color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                                elif NSFW == False:
                                    embed = discord.Embed(
                                        title ="from {} >> {}".format(subreddit, title),
                                        description=string,
                                        color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                            elif ctx.channel.is_nsfw() == False:
                                if NSFW == False:
                                    embed = discord.Embed(
                                        title ="from {} >> {}".format(subreddit, title),
                                        description=string,
                                        color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        title="You must run this command in an NSFW channel!",
                                        color= reddit_color
                                    )
                                    await ctx.send(embed=embed)
                        else:
                            if ctx.channel.is_nsfw():
                                if NSFW == False:
                                    embed = discord.Embed(
                                        title = "from {} >> {}".format(subreddit, title),
                                        color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                                elif NSFW == True:
                                    embed = discord.Embed(
                                    title = "from {} >> {}".format(subreddit, title),
                                    color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                            elif ctx.channel.is_nsfw() == False:
                                if NSFW == False:
                                    embed = discord.Embed(
                                        title = "from {} >> {}".format(subreddit, title),
                                        color=reddit_color
                                    )
                                    embed.set_image(url=str(url))
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    title="You must run this command in an NSFW channel!",
                                    color= reddit_color
                                )
                                await ctx.send(embed=embed)
                        return
            else:
                embed = discord.Embed(
                    title="That subreddit does not exist or an error has occurred.",
                    color=reddit_color
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                    title="That subreddit does not exist or an error has occurred.",
                    description=e,
                    color=reddit_color
                )
            await ctx.send(embed=embed)

    @bot.command()
    async def fourchan(ctx, board, *length):
        try:
            board = basc_py4chan.Board(str(board))
            all_thread_ids = board.get_all_thread_ids()
        except:
            embed = discord.Embed(
                title="Failed to find that 4chan thread or an error has occurred.",
                color=four_chan
            )
            await ctx.send(embed=embed)
            return
        for ID in range(len(all_thread_ids)):

            first_thread_id = all_thread_ids[ID]
            thread = board.get_thread(first_thread_id)
            topic = thread.topic

            if ID >= 3:
                break
            
            embed = discord.Embed(
                title = topic.subject,
                description = topic.text_comment,
                color = four_chan
            )
            for f in thread.file_objects():
                embed.set_image(url=f.file_url)
                print(f.file_url)
            await ctx.send(embed = embed)

    def test_die(dice):
        if int(dice) in [4, 6, 8, 10, 12, 20, 100]: return True
        else: return False

    # @bot.command()
    # async def roll(ctx, dice):
    #     dice_side_count = 0
    #     additive = 0
    #     if "+" in dice:
    #         split_dice = dice.split("d")
    #         split_dice = listtostring(split_dice).split("+")
    #         additive = int(split_dice[1])
    #         dice_side_count = int(split_dice[0])
    #         dice = random.randint(1, dice_side_count)
    #     elif "+" not in dice:
    #         split_dice = dice.split("d")
    #         dice_side_count = int(split_dice[1])
    #         print(dice_side_count)
    #         dice = random.randint(1, dice_side_count)
    #     await ctx.send(f'**D{dice_side_count}**: {dice}\n**Addition**: {additive}\n**Returned Value**: {dice + additive}')

    # @bot.command()
    # async def roll(ctx, value):
    #     value = value.lower()
    #     multiplier = 1
    #     temp_list = []
    #     summ = 0
    #     if "d" in value:
    #         if "+" not in value:
    #             if len(value) > 2:
    #                 val = int(value.index("d"))+1
    #                 rand_int = int(value[val:len(value)])
    #                 multiplier = int(value[0:val-1])
    #             else:
    #                 val = int(value.index("d"))+1
    #                 rand_int = int(value[val:len(value)])

    #             for i in range(multiplier):
    #                 to_add = random.randint(1, rand_int)
    #                 temp_list.append(to_add)

    #             if len(temp_list) >= 1:
    #                 for i in range(len(temp_list)):
    #                     summ += temp_list[i]
                
    #             await ctx.send(
    #                 f'**D{rand_int}**\n**Values to Add**: {temp_list}\n**Returned Value**: {summ}'
    #             )
            
    def remove_d(list):
        temp_list = []
        for item in list:
            if len(item) > 2:
                string1 = item.split("d")[0]
                string2 = item.split("d")[1]
                for i in range(int(string1)):
                    temp_list.append(int(string2))
            else:
                string = int(item.replace("d", " "))
                temp_list.append(string)

        return temp_list

    @bot.command()
    async def roll(ctx, value):
        if "+" in value:
            to_rand = []
            to_add = []
            list = value.split("+")
            for i in range(len(list)):
                if "d" in str(list[i]):
                    to_rand.append(list[i])
                else:
                    to_add.append(int(list[i]))

            print(f'To Randomize: {to_rand}\nTo Add: {to_add}')

            to_rand = remove_d(to_rand)

            print(to_rand)

            randomed = []
            for val in range(len(to_rand)):
                rand = random.randint(1, to_rand[val])
                randomed.append(rand)
            
            summ = 0
            for val in to_add:
                summ += val

            random_summ = 0
            for val in randomed:
                random_summ += val

            total_sum = random_summ + summ

            await ctx.send(f'**Equation**: {value}\n**To Randomize**: {to_rand}\n**Randomized Values**: {randomed}\n**To Add**: {to_add}\n***__Total Sum__***: {total_sum}')

        else:
            summ = 0
            list = value.split("d")
            if '' in list:
                list.remove('')
                randomed = random.randint(1, int(list[0]))
                amount = 1
                to_randomize = list[0]
                summ = randomed
            else:
                for i in range(int(list[0])):
                    ammount = list[0]
                    randomed = random.randint(1, int(list[1]))
                    to_randomize = list[1]
                    summ += randomed
            
            await ctx.send(f'**Equation**: {value}\n**To Randomize**: {to_randomize}\n**Randomized {ammount} times**\n***__Total Sum__***: {summ}')


    # bot.run(token)
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token))
    loop.create_task(client.start(token))
    # loop.run_until_complete(my_coroutine())
    loop.run_forever()

    #https://stackoverflow.com/questions/62102897/certifacte-verify-failed-certificate-has-expired-ssl-c1108/62104752#62104752?newreg=c7d8fae3b0264f3892ac0036b22f3466
except KeyboardInterrupt:
    print("{} has been forcefully closed.".format(__file__))
