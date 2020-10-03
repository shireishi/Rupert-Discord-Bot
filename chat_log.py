import discord
import asyncio
import ast
import os

token = 'NzQ2NTA0NjE3NTA3OTQ2NzA1.X0BSmg.FaTtgAhogjs2-KLZD6KaeFj7gcE'
client = discord.Client()

@client.event
async def on_ready():
    print("Logged on as {}.".format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return True

   
    if message:
        with open("chat_log.txt", "a") as file:
            file.write("{0} : {1}\n".format(message.author, message.content))
        print("{0.author}: {0.content}".format(message))

        with open("reputation.txt", 'r') as file:
            dict = ast.literal_eval(file.read())
            
            toAdd = {str(message.author.id):{'rep': 0, 'name':message.author.name}}
            
            if str(message.author.id) in dict:
                
                dict[str(message.author.id)]['rep'] += 1
                dict[str(message.author.id)]['name'] = str(message.author.display_name)

                with open('reputation.txt', 'w') as edit:
                    edit.write(str(dict))
            else:
                dict.update(toAdd)
                with open('reputation.txt', 'w') as edit:
                    edit.write(str(dict))

        if 'uwu' in message.content:
            print("Found an uwu")
            await message.delete()
            await message.channel.send("That is not allowed here")
        
        if message.content == "$reboot":
            if message.author.id == 230895739784396800:
                await message.channel.send("Rebooting Rupert Bot....")
                os.system('cd /home/elara/Desktop/Coding  Projects/Discord-Bot/')
                os.system('python3 bot.py')
            else:
                await message.channel.send("Wait you're not my creator..")
        # if message.content == "rupert will you date me?":
            # await message.channel.send("Of Course, {}!".format(message.author.mention))    
client.run(token)