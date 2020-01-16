from discord.ext import commands
import discord
import asyncio
import mysql.connector
import datetime
from BD.connect_bd import connectBD

def findid(message):
    message = message.replace("<","")
    message = message.replace("@","")
    message = message.replace("!","")
    message = message.replace(">","")
    message = message.replace("&","")
    return int(message)

class role(commands.Cog):
    @commands.command()
    async def buyrole(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой buyrole! Я тебе помогу:"
                                    "```/buyrole [На сколько дней]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        mybd = connectBD()
        bdcursor = mybd.cursor()

        try:
            bdcursor.execute("SELECT id FROM PrivateRole WHERE id = {}".format(ctx.author.id))
            if bdcursor.fetchall():
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя уже есть роли, ты не можешь купить еще 1.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

            money = 250 * int(arg1)

            bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            balance = int(select[0][0])

            if money > balance:
                helpmessage = await ctx.send("<@!{}> у тебя не хватает 🍭 чтоб купить роль".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

            time = datetime.datetime.today()
            days = int(arg1)
            time += datetime.timedelta(days)

            role = await ctx.guild.create_role()
            await ctx.author.add_roles(role)
            await role.edit(position=4)

            sql ="INSERT INTO PrivateRole VALUES(%s,%s,%s,%s)"
            val = (ctx.author.id,ctx.author.name,role.id,time)
            bdcursor.execute(sql,val)

            sql ="INSERT INTO Roles VALUES(%s,%s,%s)"
            val = (ctx.author.id,ctx.author.name,role.id)
            bdcursor.execute(sql,val)

            bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-money,ctx.author.id))

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()

    @commands.command()
    async def change_role(self,ctx,arg1=None,arg2=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.send("Привет <@{}>, я вижу что у тебя проблемы с командой change_role! Я тебе помогу:"
                                    "```/change_role [name/color/days] [Название/Цвет пример(000000)/На сколько] ```\n"
                                    "````name - Названия личной роли\ncolor - цвет личной роли\ndays - продлить роли````".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
    
        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT role_id FROM PrivateRole WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()

        if not select:
            helpmessage = await ctx.send("Привет <@{}>, у тебя нет личной роли чтоб её поменять, чтоб её создать используйте /buyrole".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            role = ctx.guild.get_role(findid(select[0][0]))

            if arg1 == "name":
                await role.edit(name=arg2)
            elif arg1 == "color":
                await role.edit(colour=discord.Colour(int(arg2)))
            elif arg1 == "days":
                bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
                select = bdcursor.fetchall()
                balance = int(select[0][0])

                bdcursor.execute("SELECT time FROM PrivateRole WHERE id = {}".format(ctx.author.id))
                select = bdcursor.fetchall()

                time = select[0][0]
                days = int(arg2)
                time += datetime.timedelta(days)
                balance -= days * 250

                bdcursor.execute("UPDATE PrivateRole set time = '{}' WHERE id = {}".format(time,ctx.author.id))
                bdcursor.execute("UPDATE Users set balance = '{}' WHERE id = {}".format(balance,ctx.author.id))
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        mybd.commit()
    
    @commands.command()
    async def dellrole(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT role_id FROM PrivateRole WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()

        if not select:
            helpmessage = await ctx.send("Привет <@{}>, у тебя нет личной роли чтоб её удалить, чтоб её создать используйте /buyrole".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            role = ctx.guild.get_role(findid(select[0][0]))
            await role.delete()

            bdcursor.execute("DELETE FROM PrivateRole WHERE id = {}".format(ctx.author.id)) 

            await ctx.send("<@!{}> ваша роль успешно была удалена!".format(ctx.author.id))
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()