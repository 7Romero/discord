from discord.ext import commands
import discord
import asyncio
import json
import random
from BD.connect_bd import connectBD

def findid(message):
    message = message.replace("<","")
    message = message.replace("@","")
    message = message.replace("!","")
    message = message.replace(">","")
    message = message.replace("&","")
    return int(message)


class reaction_pair(commands.Cog):
    @commands.command()
    async def bite (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой bite! Я тебе помогу:"
                                    "```/bite [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['bitePrice'])
        reaction = date['biteGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> укусил <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def hug (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой hug! Я тебе помогу:"
                                    "```/hug [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['hugPrice'])
        reaction = date['hugGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> обнял <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()    

    @commands.command()
    async def kiss (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой kiss! Я тебе помогу:"
                                    "```/kiss [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['kissPrice'])
        reaction = date['kissGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> поцеловал <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def lick (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой lick! Я тебе помогу:"
                                    "```/lick [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['lickPrice'])
        reaction = date['lickGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> облизал <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()
    
    @commands.command()
    async def pet (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой pet! Я тебе помогу:"
                                    "```/pet [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['petPrice'])
        reaction = date['petGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> погладил <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def seduce (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой seduce! Я тебе помогу:"
                                    "```/seduce [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['seducePrice'])
        reaction = date['seduceGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> соблазняет <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()    
    
    @commands.command()
    async def sex (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой sex! Я тебе помогу:"
                                    "```/sex [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['sexPrice'])
        reaction = date['sexGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> занялся грязным делом с <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def slap (self,ctx,arg1 = None):
        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой slap! Я тебе помогу:"
                                    "```/slap [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        filename = "command\\reaction\\REACTconfig.json"
        myfile = open(filename,mode = 'r')
        date = json.load(myfile)
        myfile.close()
        # loading a date from json file

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])
        price = int(date['slapPrice'])
        reaction = date['slapGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        memeber = ctx.guild.get_member(findid(arg1))

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> ударил <@!{}> ".format(ctx.author.id,memeber.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()    
    