from discord.ext import commands
import discord
import asyncio
import json
import random
from BD.connect_bd import connectBD

class reaction_single(commands.Cog):
    @commands.command()
    async def ablush (self,ctx):
        await ctx.message.delete()
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
        price = int(date['ablushPrice'])
        reaction = date['ablushGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))
        embed=discord.Embed(title="Анимация",description="<@!{}> смущаться ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def angry (self,ctx):
        await ctx.message.delete()
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
        price = int(date['angryPrice'])
        reaction = date['angryGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))

        embed=discord.Embed(title="Анимация",description="<@!{}> злится ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()
    
    @commands.command()
    async def cry (self,ctx):
        await ctx.message.delete()
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
        price = int(date['cryPrice'])
        reaction = date['cryGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))

        embed=discord.Embed(title="Анимация",description="<@!{}> грустит ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()
    
    @commands.command()
    async def happy (self,ctx):
        await ctx.message.delete()
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
        price = int(date['happyPrice'])
        reaction = date['happyGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))

        embed=discord.Embed(title="Анимация",description="<@!{}> радуеться ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()

    @commands.command()
    async def roar (self,ctx):
        await ctx.message.delete()
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
        price = int(date['roarPrice'])
        reaction = date['roarGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))

        embed=discord.Embed(title="Анимация",description="<@!{}> рычит ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()
    
    @commands.command()
    async def smoke (self,ctx):
        await ctx.message.delete()
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
        price = int(date['smokePrice'])
        reaction = date['smokeGifs']

        if balance < price:
            myBD.commit()
            helpmessage = await ctx.send("Чтоб вызвать данную реакцию вам нужно {} 🍭".format(price))
            await asyncio.sleep(10)
            await helpmessage.delete()
            return 0

        bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-price,ctx.author.id))

        embed=discord.Embed(title="Анимация",description="<@!{}> закурил ".format(ctx.author.id),color=0xff8080)
        embed.set_image(url = "{}".format(reaction[random.randint(0,len(reaction)-1)]))
        embed.set_footer(text="Вызвал {} | С вас сняли {}🍭".format(ctx.author.name,price))

        await ctx.send(embed=embed)

        myBD.commit()