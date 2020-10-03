import discord

rupertColor = 0xFF2507

class Info():
    def general(self, prefix):
        embed = discord.Embed(title='Help Menu', 
        description='This is the command list for this server.', 
        color=rupertColor)

        embed.set_author(name='Prefix is ( {} )'.format(prefix))
        
        embed.add_field(name='{}rep'.format(prefix), value='returns the reputation value.', inline=False)
        
        embed.add_field(name='{}hello'.format(prefix), value='Prints a greeting string.', inline=False)
        
        embed.add_field(name='{}info'.format(prefix), value='Provides the server information', inline=False)
        
        embed.add_field(name='{}color'.format(prefix), value='(WIP) Assigns the color values to use in events such as embedding.', inline=False)
        
        embed.add_field(name="{}hug".format(prefix), value="Interacts with the provided user.", inline=False)
        
        embed.add_field(name="{}boop".format(prefix), value="Interacts with the provided user.", inline=False)
        
        embed.add_field(name="{}smack".format(prefix), value="Interacts with the provided user.", inline=False)
        
        embed.add_field(name="{}shoot".format(prefix), value="Shoots the designated user.", inline=False)
        
        embed.add_field(name='{}help'.format(prefix), value='Provides this menu.', inline=False)
        
        embed.add_field(name='{}clear'.format(prefix), value="Clears the chat to a certain amount.", inline=False)
        
        embed.add_field(name='{}report'.format(prefix), value="Submits a bug report to the lead developer of the Rupert Reputation Bot.", inline=False)
        
        embed.add_field(name="{}leaderboard".format(prefix), value="Shows a leaderboard based on users reputation.", inline=False)
        
        embed.add_field(name="{}rupertinfo".format(prefix), value="Displays the information about Rupert.", inline=False)
        
        embed.add_field(name="{}creator".format(prefix), value="Displays information about the creator of Rupert.", inline=False)

        embed.add_field(name="{}ava".format(prefix), value="Avatar command which displays the avatar image of a user.", inline=False)

        embed.set_footer(text='Prefix is ( {} )'.format(prefix))
        return embed
        
    def color(self):
        embed = discord.Embed(
            title = "Color Command",
            description = "color [color name] i.e : red, green, blue, etc...",
            color = rupertColor
        )
        return embed
    
    def ava(self):
        embed = discord.Embed(
            title = "Avatar Command",
            description= "ava [user mention] or no argument provided",
            color = rupertColor
        )
        return embed
            
    def info(self):
        embed = discord.Embed(
            title="Info Command",
            description="info provides information about the current server.",
            color= rupertColor
        )
        return embed
    
    def rep(self):
        embed = discord.Embed(
            title='Reputation Command',
            description='rep provides the reputation value of the current user or you can mention the user for their value.\nrep [mention]',
            color= rupertColor
        )
        return embed
    
    def help(self):
        embed = discord.Embed(
            title="The Help Command",
            description="This command is used to find out the information or specific syntax of commands.\nhelp [command name / general]",
            color=rupertColor
        )
        return embed
    
    def clear(self):
        embed = discord.Embed(
            title="Clear Command",
            description="This command allows you to clear the chat either at a certain amount or the entire chat.\nclear [amount/all]",
            color=rupertColor
        )
        return embed
        
    def report(self):
        embed = discord.Embed(
            title="Report Command",
            description="This command is used to report bugs or issues to the developers for them to fix.\nreport [info]",
            color=rupertColor
        )
        return embed