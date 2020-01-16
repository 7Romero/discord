from discord.ext import commands
import discord
import asyncio
import mysql.connector
from BD.connect_bd import connectBD

def findid(message):
    message = message.replace("<","")
    message = message.replace("@","")
    message = message.replace("!","")
    message = message.replace(">","")
    message = message.replace("&","")
    return int(message)

def Getting_big_str(*arg1):
    message = ""
    for i in range(len(arg1[0])):
        message += str(arg1[0][i]) + " "
    return message

class Users(commands.Cog):
    @commands.command()
    async def stats(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0
            
        await ctx.message.delete()
        try:
            if not arg1:
                member = ctx.author
            else:
                member = ctx.guild.get_member(findid(arg1))

            mybd = connectBD()
            bdcursor = mybd.cursor()

            bdcursor.execute("SELECT balance,box,chat_message,voice_online,couple,instagram,AboutMe FROM Users WHERE id = {}".format(member.id))
            listinfo = bdcursor.fetchall()

            mybd.commit()

            if not listinfo:
                return 0

            embed=discord.Embed(color=0xff8080)
            embed.set_author(name = "Статистика,{}".format(member.name), icon_url = member.avatar_url)
            embed.set_thumbnail(url = member.avatar_url)
           # embed.add_field(name="Имя:", value="```{}```".format(member.name), inline=False)
            embed.add_field(name="💰 Баланс:", value="```{}🍭```".format(listinfo[0][0]), inline=True)
            embed.add_field(name="🎁 Коробок:", value="```{}```".format(listinfo[0][1]), inline=True)
            embed.add_field(name="✉️ Сообщений:", value="```{} ```".format(listinfo[0][2]), inline=True)
            embed.add_field(name="⏲️ Голосовой онлайн:", value="```{} ч```".format(int(listinfo[0][3]) // 60), inline=True)
            if listinfo[0][4] == "Одинок":
                embed.add_field(name="💙 Пара:", value="```{} ```".format(listinfo[0][4]), inline=True)
            else:
                mayer = ctx.guild.get_member(findid(listinfo[0][4]))
                embed.add_field(name="💙 Пара:", value="```{} ```".format(mayer), inline=True)
            embed.add_field(name="💻 Instagram", value="```{} ```".format(listinfo[0][5]), inline=True)
            embed.add_field(name="💁 О себе:", value="```{} ```".format(listinfo[0][6]), inline=False)
            embed.set_footer(text="Вызвал {}".format(ctx.author))
            await ctx.send(embed=embed)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
    
    @commands.command()
    async def status(self,ctx,*arg1):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой set_status! Я тебе помогу:"
                                    "```/set_status [Текст]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        message = Getting_big_str(arg1)
        if len(message) > 50:
            helpmessage = await ctx.channel.send("Привет,{} твоя характеристика больше чем 50 символов. Попытайся уложиться именно в 50")
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        
        try:
            mybd = connectBD()
            bdcursor = mybd.cursor()
            print(message)

            bdcursor.execute("UPDATE Users set AboutMe = '{}' WHERE id = {}".format(message,ctx.author.id))

            mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
    @commands.command()
    async def instagram(self,ctx,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой instagram! Я тебе помогу:"
                                    "```/instagram [Ссылка]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        if len(arg1) > 50:
            helpmessage = await ctx.channel.send("Привет,{} твоя ссылка больше чем 50 символов. Попытайся уложиться именно в 50")
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0
        
        try:
            mybd = connectBD()
            bdcursor = mybd.cursor()

            bdcursor.execute("UPDATE Users set instagram = '{}' WHERE id = {}".format(arg1,ctx.author.id))

            mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def avatar(self,ctx,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        try:
            if arg1:
                member = ctx.guild.get_member(findid(arg1))
            else:
                member = ctx.guild.get_member(ctx.author.id)
            embed = discord.Embed(title = 'Avatar: {}'.format(member),color = 53380)
            embed.set_image(url = member.avatar_url)
            await ctx.send(embed = embed)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def shop(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        embed=discord.Embed(title="Магазин ролей.", description="Ниже вы представлены роли который можно будет купить за 🍭\nЦена за данные роли 10.000🍭",color=0x8080ff)
        embed.add_field(name = "Столб №1:" ,value="1) <@&{}>  .\n"
                                "2) <@&{}> .\n"
                                "3) <@&{}> .\n"
                                "4) <@&{}> .\n"
                                "5) <@&{}> .\n"
                                "6) <@&{}> .\n"
                                "7) <@&{}> .\n"
                                "8) <@&{}> .".format(658962593091944459,658962591628132362,658962583100850177,658962580554907669,658962595021193256,658962578822922252,658962576234905600,658962601711239178), inline=False)
        embed.add_field(name = "Столб №2: " ,value="9) <@&{}> .\n"
                                "10) <@&{}> .\n"
                                "11) <@&{}> .\n"
                                "12) <@&{}> .\n"
                                "13) <@&{}> .\n"
                                "14) <@&{}> .\n"
                                "15) <@&{}> .\n"
                                "16) <@&{}> .".format(658962599127547915,658962596917018655,658962573764591616,658962570446635011,658962551303831564,658962548346978306,658962545494982666,658962249284714497), inline=False)
        embed.set_footer(text="Чтоб купить роль используйте команду /buy [Номер]")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def buy(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой instagram! Я тебе помогу:"
                                    "```/instagram [Ссылка]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        myBD = connectBD()
        bdcursor = myBD.cursor()

        try:
            listrole = (658962593091944459,658962591628132362,658962583100850177,658962580554907669,658962595021193256,658962578822922252,658962576234905600,658962601711239178,658962599127547915,658962596917018655,658962573764591616,658962570446635011,658962551303831564,658962548346978306,658962545494982666,658962249284714497)
            role = ctx.guild.get_role(listrole[int(arg1) - 1])

            bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
            select = bdcursor.fetchall()
            balance = int(select[0][0])

            if balance < 10000:
                helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя не хватает 🍭 чтоб купить роль.Приходи когда соберешь.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            sql = "INSERT INTO Roles VALUES(%s,%s,%s)"
            val = (ctx.author.id,ctx.author.name,role.id)
            bdcursor.execute(sql,val)

            bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance-10000,ctx.author.id))

            await ctx.author.add_roles(role)

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
        myBD.commit()