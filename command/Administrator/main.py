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
    return int(message)

def Getting_big_str(*arg1):
    message = ""
    for i in range(len(arg1[0])):
        message += str(arg1[0][i]) + " "
    return message

class Administrator(commands.Cog):
    @commands.command()             ## cls command
    async def cls(self,ctx,arg1=None,arg2= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0
        
        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_cls FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой cls! Я тебе помогу:"
                                    "```/cls [Сколько собщений нужно удалить] [link - если нужно удалить сообщение конкретного человека(Не обезательно)]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try: 
            async for message in ctx.channel.history(limit=int(arg1)):
                if not arg2:
                    await message.delete()
                else:
                    if message.author.id == findid(arg2):
                        await message.delete()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()

    @commands.command()
    async def mute(self,ctx,typee = None,arg1=None,arg2=None,*arg3):  
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами :(")
            return 0

        await ctx.message.delete() 

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_mute FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not typee or not arg1 or not arg2 or not arg3:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой mute! Я тебе помогу:"
                                    "```/mute [chat/voice] [@user] [Время(В минутах)] [Причина.]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            arg3 = Getting_big_str(arg3)
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> ты что садист?? Зачем ты хочешь себя наказать?".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            if typee == "chat":
                role = discord.utils.get(member.guild.roles, id=656102229543223296)
            elif typee == "voice":
                role = discord.utils.get(member.guild.roles, id=656101665283506236)
            else:
                raise ValueError()
            await member.add_roles(role)
            time = int(arg2) * 60
            # embed который приходит в dm
            embed=discord.Embed(title="Модерация: Mute {}".format(typee), description="Привет, {} вы были наказаны модератором {}".format(member.name,ctx.author))
            embed.add_field(name="Причина:", value="Вы были наказаны по причине: {}".format(arg3), inline=True)
            embed.add_field(name="Время:", value="Вы были наказаны на: {} минут".format(arg2), inline=True)
            embed.add_field(name="Help", value="Если вы думаете что наказание выдано неверно вы можете вызвать куратора и рассказать ему свою проблему и вместе попытаться её решить.", inline=False)
            embed.set_footer(text="Не нужно больше нарушать. Спасибо что вы снами)")
            await member.send(embed=embed)
            # embed end
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(655847919504850954)
            embed=discord.Embed(title="Logger Модерация: Muted {}".format(typee), description="Модератор {} наказал игрока {} на {} минут по причине {}".format(ctx.author,member,arg2,arg3))
            await logchannel.send(embed=embed)
            #embed end
            await asyncio.sleep(time)
            if member.id:
                await member.remove_roles(role)

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        

    @commands.command()
    async def kick(self,ctx,arg1=None,*arg2):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_kick FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой kick! Я тебе помогу:"
                                    "```/kick [@user] [Причина.]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            arg2 = Getting_big_str(arg2)
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> ты что садист?? Зачем ты хочешь себя наказать?".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            # embed say message id md
            embed=discord.Embed(title="Модерация: Kick", description="Привет, {} вы были наказаны модератором {}".format(member.name,ctx.author))
            embed.add_field(name="Причина", value="Вы были наказаны по причине: {}".format(arg2), inline=False)
            embed.add_field(name="Help", value="Если вы думаете что наказание выдано неверно вы можете вызвать куратора и рассказать ему свою проблему и вместе попытаться её решить.", inline=True)
            embed.set_footer(text="Не нужно больше нарушать. Спасибо что вы снами)")
            # embed end 
            await member.send(embed=embed)
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(656413374296489994)
            embed=discord.Embed(title="Logger Модерация: Kick", description="Модератор {} наказал игрока {} по причине {}".format(ctx.author,member,arg2))
            await logchannel.send(embed=embed)
            #embed end
            await member.kick()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
    
    @commands.command()
    async def ban(self,ctx,arg1=None,*arg2):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_ban FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой ban! Я тебе помогу:"
                                    "```/ban [@user] [Причина]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            arg2 = Getting_big_str(arg2)
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> ты что садист?? Зачем ты хочешь себя наказать?".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            # embed say message id md
            embed=discord.Embed(title="Модерация: Ban", description="Привет, {} вы были наказаны модератором {}".format(member.name,ctx.author))
            embed.add_field(name="Причина", value="Вы были наказаны по причине: {}".format(arg2), inline=False)
            embed.add_field(name="Help", value="Если вы думаете что наказание выдано неверно вы можете написать куратора и рассказать ему свою проблему и вместе попытаться её решить.", inline=True)
            embed.set_footer(text="Не нужно больше нарушать. Спасибо что вы снами)")
            # embed end 
            await member.send(embed=embed)
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(656424405609480192)
            embed=discord.Embed(title="Logger Модерация: Ban", description="Модератор {} наказал игрока {} по причине {}".format(ctx.author,member,arg2))
            await logchannel.send(embed=embed)
            #embed end
            await ctx.guild.ban(member,delete_message_days=1)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command() ## add проверку если человек в голосовом канале
    async def antiafk(self,ctx,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_antiafk FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой antiafk! Я тебе помогу:"
                                    "```/antiafk [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> ты что садист?? Зачем ты хочешь себя наказать?".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            if not member.voice:
                helpmessage = await ctx.send("<@{}> Человек сейчас не находиться в голосовом канале!!".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
            # embed say message id md
            embed=discord.Embed(title="Модерация: Anti Afk", description="Привет, {} модератором {} применил на вас Anti Afk".format(member,ctx.author))
            embed.add_field(name="Почему?", value="Наверное он хочет у вас что-то спросить.", inline=False)
            embed.add_field(name="Help", value="Если вы заметили как модератор превышает свой полномочие можете вызвать куратора и он поможет.", inline=True)
            embed.set_footer(text="Спасибо что вы снами)")
            # embed end 
            await member.send(embed=embed)
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(656444441325862942)
            embed=discord.Embed(title="Logger Модерация: Anti Afk", description="Модератор {} применил Anti Afk на {}".format(ctx.author,member))
            await logchannel.send(embed=embed)
            #embed end
            ListAntiAfk = (656437983515246612,656438031460466689,656438081272152066,656438100741980160,656438125802946570,ctx.author.voice.channel.id)
            for channel in ListAntiAfk:
                channel = ctx.guild.get_channel(channel)
                await member.move_to(channel)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def goto(self,ctx,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_goto FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой goto! Я тебе помогу:"
                                    "```/goto [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> мне кажеться что ты что-то принял! Ты точно не наркоман?!".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            if not member.voice:
                helpmessage = await ctx.send("<@{}> Человек сейчас не находиться в голосовом канале!!".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
            if not ctx.author.voice:
                helpmessage = await ctx.send("<@{}> Сначала нужно зайти в голосовой канал!!".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
            await ctx.author.move_to(member.voice.channel)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
    @commands.command()
    async def gethere(self,ctx,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_gethere FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой gethere! Я тебе помогу:"
                                    "```/gethere [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> мне кажеться что ты что-то принял! Ты точно не наркоман?!".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            if not member.voice:
                helpmessage = await ctx.send("<@{}> Человек сейчас не находиться в голосовом канале!!".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
            if not ctx.author.voice:
                helpmessage = await ctx.send("<@{}> Сначала нужно зайти в голосовой канал!!".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                return 0
            await member.move_to(ctx.author.voice.channel)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
    
    @commands.command()
    async def unmute(self,ctx,typee= None,arg1= None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_mute FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        await ctx.message.delete() 
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой unmute! Я тебе помогу:"
                                    "```/unmute [chat/voice] [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if typee == "chat":
                role = discord.utils.get(member.guild.roles, id=656102229543223296)
            elif typee == "voice":
                role = discord.utils.get(member.guild.roles, id=656101665283506236)
            else:
                raise ValueError()
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(655847919504850954)
            embed=discord.Embed(title="Logger Модерация: UnMuted {}".format(typee), description="Модератор {} размутил игрока {}.".format(ctx.author,member))
            await logchannel.send(embed=embed)
            #embed end
            await member.remove_roles(role)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def warn(self,ctx,arg1=None,*arg2):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_warn FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой warn! Я тебе помогу:"
                                    "```/warn [@user] [Причина]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            arg2 = Getting_big_str(arg2)
            member = ctx.guild.get_member(findid(arg1))
            if not member:
                raise ValueError
            if member.id == ctx.author.id:
                Error_message = await ctx.send("<@!{}> ты что садист?? Зачем ты хочешь себя наказать?".format(ctx.author.id))
                await asyncio.sleep(5)
                await Error_message.delete()
                return 0 
            myBD = connectBD()
            bdcursor = myBD.cursor()
            sql = "SELECT warn FROM Users WHERE id = {}".format(member.id)
            bdcursor.execute(sql)
            resultat = bdcursor.fetchall()
            warn = int(resultat[0][0]) + 1
            # embed say message id md
            embed=discord.Embed(title="Модерация: Warn", description="Привет, {} вы получили warn от модератором {}".format(member.name,ctx.author))
            embed.add_field(name="Причина", value="Вы были наказаны по причине: {}.".format(arg2), inline=False)
            embed.add_field(name="Дополнительно", value="На данный момент у вас {} варнов.".format(warn), inline=False)
            embed.add_field(name="Help", value="Если вы думаете что наказание выдано неверно вы можете написать куратора и рассказать ему свою проблему и вместе попытаться её решить.", inline=True)
            embed.set_footer(text="Если вы получите 5 варнов вам выдадут роль Toxic")
            # embed end 
            await member.send(embed=embed)
            #embed который отправляется в owners log
            logchannel = ctx.guild.get_channel(657222614904995862)
            embed=discord.Embed(title="Logger Модерация: Warn", description="Модератор {} выдал warn игроку {} по причине {}. На данный момент у него {} варнов".format(ctx.author,member,arg2,warn))
            await logchannel.send(embed=embed)
            #embed end
            sql = "UPDATE Users set warn = {} WHERE id = {}".format(warn,member.id)
            bdcursor.execute(sql)
            if warn >= 5:
                role = discord.utils.get(member.guild.roles, id=657236785839079474)
                await member.add_roles(role)
            myBD.commit()

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def hide(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_hide FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой hide! Я тебе помогу:"
                                    "```/hide [on/off]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            if arg1 == 'on':
                listroles = ctx.author.roles
                for role in listroles:
                    if role.id != 656100483399942146 and role.id != 651865140375060496 and role.id !=655771685047369768:
                        await ctx.author.remove_roles(role)
            else:
                mybd = connectBD()
                bdcursor = mybd.cursor()
                
                sql = "SELECT roles_id FROM Roles WHERE id = {}".format(ctx.author.id)
                bdcursor.execute(sql)
                myresult = bdcursor.fetchall()
                for i in range(len(myresult)):
                    ctx.guild.get_role(myresult[i][0])
                    role = ctx.guild.get_role(int(myresult[i][0]))
                    if not role:
                        sql = "DELETE FROM Roles WHERE roles_id = {}".format(myresult[i][0])
                        bdcursor.execute(sql) 
                    else:
                        await ctx.author.add_roles(role)
                mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
    
    
    @commands.command()
    async def clear(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        
        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_clear FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0
        if select[0][0] == 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, у тебя нет прав,если думаешь что это ошибка то напиши основателю.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        mybd.commit()

        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой clear! Я тебе помогу:"
                                    "```/clear [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            
            mybd = connectBD()
            bdcursor = mybd.cursor()

            sql = "DELETE FROM Users WHERE id = {}".format(member.id)
            bdcursor.execute(sql)

            sql = "DELETE FROM roles WHERE id = {}".format(member.id)
            bdcursor.execute(sql)

            mybd.commit()

            embed=discord.Embed(title="ВАЖНО", description="Ваш аккаунт был удалён!!")
            embed.add_field(name="Информация", value="Администратор удалил ваш аккаунт и кикнул вас из группы. ", inline=False)
            embed.add_field(name="Почему?", value="Удаление аккаунта происходит очень редко и если вас обнулили значит вы очень грубо нарушили правила.", inline=True)
            embed.set_footer(text="Вы можете попробовать узнать причину у основателя.")

            await member.send(embed=embed)

            await member.kick()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()