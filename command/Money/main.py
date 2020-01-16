from discord.ext import commands
import discord
import asyncio
import mysql.connector
import datetime
import random
from BD.connect_bd import connectBD

def findid(message):
    message = message.replace("<","")
    message = message.replace("@","")
    message = message.replace("!","")
    message = message.replace(">","")
    message = message.replace("&","")
    return int(message)

class Money(commands.Cog):
    @commands.command()
    async def timecoin(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        today_time = datetime.datetime.now()

        myBD = connectBD()
        bdcursor = myBD.cursor()

        try:
            bdcursor.execute("SELECT time_coin FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            time = today_time - select[0][0]
            time_h = time.seconds // 3600

            if time_h >= 12 or time.days >= 1:
                await ctx.send("<@!{}> забирай свои 100 🍭 и проваливай, приходи через 12ч когда я снова буду в духе!".format(ctx.author.id))

                bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
                select = bdcursor.fetchall()
                balance = int(select[0][0]) + 100

                bdcursor.execute("UPDATE Users set balance = {},time_coin = '{}' WHERE id = {}".format(balance,today_time,ctx.author.id))
            elif time_h < 12:
                helpmessage = await ctx.send("Эй ты <@!{}> решил меня надурить?? Я знаю что выдавал тебе твой бонус недавно, приходи через {}ч.".format(ctx.author.id,12-time_h))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0
            else:
                raise ValueError
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        myBD.commit()

    @commands.command()
    async def give(self,ctx,arg1=None,arg2=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой give! Я тебе помогу:"
                                    "```/give [@user] [сумму]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        
        myBD = connectBD()
        bdcursor = myBD.cursor()

        try:
            member = ctx.guild.get_member(findid(arg1))
            money = int(arg2)

            if money <= 0:
                helpmessage = await ctx.send("<@!{}> сумма должна быть больше 0".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0
            elif money > 10000:
                helpmessage = await ctx.send("<@!{}> сумма должна быть не больше 10000".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            author_money = int(select[0][0])

            if author_money < money:
                helpmessage = await ctx.send("<@!{}> у вас нет столько 🍭".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(member.id))
            select = bdcursor.fetchall()
            member_money = int(select[0][0])

            author_money -= money
            member_money += money

            bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(author_money,ctx.author.id))
            bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(member_money,member.id))

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
        myBD.commit()

    @commands.command()
    async def give_box(self,ctx,arg1=None,arg2=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой give_box! Я тебе помогу:"
                                    "```/give_box [@user] [сколько]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        
        myBD = connectBD()
        bdcursor = myBD.cursor()

        try:
            member = ctx.guild.get_member(findid(arg1))
            box = int(arg2)

            if box <= 0:
                helpmessage = await ctx.send("<@!{}> вы не можете передать число коробок меньше 0".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0
            elif box > 1000:
                helpmessage = await ctx.send("<@!{}> вы не можете передать число коробок больше 1000".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            bdcursor.execute("SELECT box FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            author_box = int(select[0][0])

            if author_box < box:
                helpmessage = await ctx.send("<@!{}> у вас нет столько 🎁".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            bdcursor.execute("SELECT box FROM Users WHERE id = {}".format(member.id))
            select = bdcursor.fetchall()
            member_box = int(select[0][0])

            author_box -= box
            member_box += box

            bdcursor.execute("UPDATE Users set box = {} WHERE id = {}".format(author_box,ctx.author.id))
            bdcursor.execute("UPDATE Users set box = {} WHERE id = {}".format(member_box,member.id))

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
        myBD.commit()

    @commands.command()
    async def box_open(self,ctx,arg1 = None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой box_open! Я тебе помогу:"
                                    "```/box_open [сколько]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        myBD = connectBD()
        bdcursor = myBD.cursor()

        try:
            box = int(arg1)

            bdcursor.execute("SELECT box FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            author_box = int(select[0][0])

            bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            money = int(select[0][0])

            if box > author_box:
                helpmessage = await ctx.send("<@!{}> у вас нет столько коробок".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0
            
            balance_box = 0

            for i in range(box):
                balance_box += random.randrange(0,500)

            author_box -= box

            bdcursor.execute("UPDATE Users set balance = {},box = {} WHERE id = {}".format(money+balance_box,author_box,ctx.author.id))

            await ctx.send("<@!{}> поздравляю вы получили {}🍭 из {}🎁. На данный момент у вас {}🍭!!".format(ctx.author.id,balance_box,box,money+balance_box))

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        myBD.commit()

    @commands.command()
    async def top(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0
        
        await ctx.message.delete()
        myBD = connectBD()
        bdcursor = myBD.cursor()

        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой top! Я тебе помогу:"
                                    "```/top [message/voice/balance]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            myBD.commit()
            return 0

        if arg1 == "balance":
            bdcursor.execute("SELECT balance,id FROM Users ORDER BY balance DESC")
            select = bdcursor.fetchall()

            embed=discord.Embed(title="Топ 5 участников сервера по деньгам", description="Имя: <@!{}>       Баланс: {}\n"
                                                                                         "Имя: <@!{}>       Баланс: {}\n"
                                                                                         "Имя: <@!{}>       Баланс: {}\n"
                                                                                         "Имя: <@!{}>       Баланс: {}\n"
                                                                                         "Имя: <@!{}>       Баланс: {}".format(
                    select[0][1],select[0][0], select[1][1],select[1][0], select[2][1],select[2][0], select[3][1],select[3][0], select[4][1],select[4][0]), color=0xff80c0)
        elif arg1 == "voice":
            bdcursor.execute("SELECT voice_online,id FROM Users ORDER BY voice_online DESC")
            select = bdcursor.fetchall()

            embed=discord.Embed(title="Топ 5 участников сервера по онлайну", description="Имя: <@!{}>       Онлайн: {}\n"
                                                                                         "Имя: <@!{}>       Онлайн: {}\n"
                                                                                         "Имя: <@!{}>       Онлайн: {}\n"
                                                                                         "Имя: <@!{}>       Онлайн: {}\n"
                                                                                         "Имя: <@!{}>       Онлайн: {}".format(
                    select[0][1],select[0][0], select[1][1],select[1][0], select[2][1],select[2][0], select[3][1],select[3][0], select[4][1],select[4][0]), color=0xff80c0)
        elif arg1 == "message":
            bdcursor.execute("SELECT chat_message,id FROM Users ORDER BY chat_message DESC")
            select = bdcursor.fetchall()

            embed=discord.Embed(title="Топ 5 участников сервера по сообщениям", description="Имя: <@!{}>       Сообщений: {}\n"
                                                                                            "Имя: <@!{}>       Сообщений: {}\n"
                                                                                            "Имя: <@!{}>       Сообщений: {}\n"
                                                                                            "Имя: <@!{}>       Сообщений: {}\n"
                                                                                            "Имя: <@!{}>       Сообщений: {}".format(
                    select[0][1],select[0][0], select[1][1],select[1][0], select[2][1],select[2][0], select[3][1],select[3][0], select[4][1],select[4][0]), color=0xff80c0)

        else:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
            myBD.commit()
            return 0
        
        await ctx.send(embed=embed)

        myBD.commit() 