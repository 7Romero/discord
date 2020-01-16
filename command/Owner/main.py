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

class Owner(commands.Cog):
    @commands.command()
    async def add_role(self,ctx,arg1=None,arg2=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        
        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой add_role! Я тебе помогу:"
                                    "```/add_role [@user] [@role]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            role = ctx.guild.get_role(findid(arg2))
            member = ctx.guild.get_member(findid(arg1))
            await member.add_roles(role)

            sql = "INSERT INTO Roles VALUES (%s,%s,%s)"
            val = (member.id,member.name,role.id) 
            bdcursor.execute(sql,val)

            mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def dell_role(self,ctx,arg1=None,arg2=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        if not arg1 or not arg2:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой dell_role! Я тебе помогу:"
                                    "```/dell_role [@user] [@role]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            role = ctx.guild.get_role(findid(arg2))
            member = ctx.guild.get_member(findid(arg1))
            await member.remove_roles(role)

            sql = "DELETE FROM Roles WHERE id = {} and roles_id = {}".format(member.id,role.id)
            bdcursor.execute(sql)

            mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def set(self,ctx,arg1=None,arg2=None,arg3=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        
        mybd = connectBD()
        bdcursor = mybd.cursor()

        bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        if not arg1 or not arg2 or not arg3:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой set! Я тебе помогу:"
                                    "```/set [@user] [balance | box | voice | chat | permision ] [Номер]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0
        
        try:
            member = ctx.guild.get_member(findid(arg1))

            if arg2 == 'balance':
                bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == 'box':
                bdcursor.execute("UPDATE Users set box = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == 'voice':
                bdcursor.execute("UPDATE Users set voice_online = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == 'chat':
                bdcursor.execute("UPDATE Users set chat_message = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == 'permision':
                bdcursor.execute("UPDATE Users set permision = {} WHERE id = {}".format(arg3,member.id))
            else:
                helpmessage = ctx.send("Ошибка в названией.")
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()

    @commands.command()
    async def create_akk(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой create_akk! Я тебе помогу:"
                                    "```/clear [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0
        try:
            member = ctx.guild.get_member(findid(arg1))
            time = datetime.datetime.today()

            sql = "INSERT INTO Users (id,name,couple,time_coin,instagram,AboutMe) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (member.id,member.name,"Одинок",time,"Нету:(","Аноним")
            bdcursor.execute(sql,val)
            
            sql = "INSERT INTO Mine (id,minetype1,minetype2,minetype3,minetype4,minetype5,minetype6) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (member.id,"0","0","0","0","0","0")
            bdcursor.execute(sql,val)

            mybd.commit()
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

    @commands.command()
    async def add_moder(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        
        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой add_moder! Я тебе помогу:"
                                    "```/add_moder [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))

            bdcursor.execute("SELECT id FROM Moderator WHERE id = {}".format(member.id))
            select = bdcursor.fetchall()
            if select:
                helpmessage = await ctx.channel.send("Привет <@{}>, данный человек уже модератор.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

            sql = "INSERT INTO Moderator (id,name) VALUES (%s,%s)"
            val = (member.id,member.name)
            bdcursor.execute(sql,val)

            embed=discord.Embed(title="Информация о модерации", description="Поздравляю вы были назначены модератором.", color=0x8080ff)
            embed.add_field(name="Важно:", value="Вы были назначены на пост 'Модератора' администратором {}.\n"
                                                "Больше информаций вы можете прочитать в каналах администраций\n".format(ctx.author.name), inline=False)
            embed.add_field(name="Команды:", value="Команды можно посмотреть '/ahelp'", inline=False)
            embed.set_footer(text="Мы рады что вы стали новым членом нашей команды.")
            await member.send(embed=embed)

            role = ctx.guild.get_role(655856459044618256)
            sql = "INSERT INTO Roles VALUES(%s,%s,%s)"
            val = (member.id,role.name,role.id)
            bdcursor.execute(sql,val)
            await member.add_roles(role)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()

    @commands.command()
    async def del_moder(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        
        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой dell_moder! Я тебе помогу:"
                                    "```/add_moder [@user]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))

            bdcursor.execute("SELECT id FROM Moderator WHERE id = {}".format(member.id))
            select = bdcursor.fetchall()
            if not select:
                helpmessage = await ctx.channel.send("Привет <@{}>, данный человек не модератор.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

            bdcursor.execute("DELETE FROM Moderator WHERE id = {}".format(member.id))

            embed=discord.Embed(title="Информация о модерации", description="Вы были удалены из списка модераторов сервера.", color=0x8080ff)
            embed.add_field(name="Важно:", value="Вас снял с поста 'Модератора' администратором {}.\n"
                                                "Больше информаций вы можете узнать у администраций\n".format(ctx.author.name), inline=False)
            embed.set_footer(text="Я буду по тебе скучать.")
            await member.send(embed=embed)


        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        rolelist = (655856526686158848,655771819210571807,655856459044618256)

        for i in range(3):
            bdcursor.execute("DELETE FROM Roles WHERE id = {}".format(rolelist[i]))
            role = ctx.guild.get_role(rolelist[i])
            await member.remove_roles(role)

        mybd.commit()

    @commands.command()
    async def set_moder(self,ctx,arg1=None,arg2=None,arg3=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        
        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        if not arg1 or not arg2 or not arg3:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой set_moder! Я тебе помогу:"
                                    "```/set_moder [@user] [mute | gethere | goto | kick | ban | disconect | warn | antiafk | hide | clear | owner ] [1 / 0] ```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            mybd.commit()
            return 0

        try:
            member = ctx.guild.get_member(findid(arg1))
            bdcursor.execute("SELECT id FROM Moderator WHERE id = {}".format(member.id))
            if not bdcursor.fetchall():
                helpmessage = await ctx.channel.send("Привет <@{}>, данный участник не модератор.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                mybd.commit()
                return 0

            if arg2 == "mute":
                bdcursor.execute("UPDATE Moderator set permision_mute = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "gethere":
                bdcursor.execute("UPDATE Moderator set permision_gethere = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "goto":
                bdcursor.execute("UPDATE Moderator set permision_goto = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "kick":
                bdcursor.execute("UPDATE Moderator set permision_kick = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "ban":
                bdcursor.execute("UPDATE Moderator set permision_ban = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "disconect":
                bdcursor.execute("UPDATE Moderator set permision_disconect = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "warn":
                bdcursor.execute("UPDATE Moderator set permision_warn = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "antiafk":
                bdcursor.execute("UPDATE Moderator set permision_antiafk = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "hide":
                bdcursor.execute("UPDATE Moderator set permision_hide = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "clear":
                bdcursor.execute("UPDATE Moderator set permision_clear = {} WHERE id = {}".format(arg3,member.id))
            elif arg2 == "owner":
                bdcursor.execute("UPDATE Moderator set permision_owner = {} WHERE id = {}".format(arg3,member.id))

            embed=discord.Embed(title="Информация о модерации", description="Ваш аккаунта был модифицирован.", color=0x8080ff)
            embed.add_field(name="Важно:", value="Ваш аккаунт был модифицирован администратором {}.\n"
                                                "Больше информаций вы можете узнать у него\n".format(ctx.author.name), inline=False)
            embed.set_footer(text="Мы рады что вы дальше помогаете нам следить за сервером.")
            await member.send(embed=embed)

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        mybd.commit()
    @commands.command()
    async def say(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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
        await ctx.send(arg1)
    
    @commands.command()
    async def welcome(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        embed=discord.Embed(title="Данный сервер был создан для лампового общения. Устраивайся поудобнее.", description="<@&665879121129373707>", color=0x8080ff)
        embed.set_author(name="Бери плед, плотнее укутывайся и отправляйся изучать все уголки этого местечка.", icon_url="https://i.imgur.com/MSfmMa1.jpg")
        embed.set_image(url = "https://thumbs.gfycat.com/YellowWarlikeGrayling-size_restricted.gif")
        await ctx.send(embed = embed)

        embed=discord.Embed(title="Данный правила распространяется только для общих текстовых и голосовых каналов.", color=0x8080ff)
        embed.set_author(name="Общие текстовые и голосовые каналы сервера модерируются.", icon_url="https://i.imgur.com/MSfmMa1.jpg")
        embed.set_image(url = "https://thumbs.gfycat.com/FeminineNaturalArgentinehornedfrog-size_restricted.gif")
        embed.add_field(name="Мут на 5 минут выдаётся за:", value="→ За то, что человек часто ***перебивает*** других. \n\n"
                                                                "→ За ***выкрики, неоднозначный вбросв.***\n _Пример:_ || Ты - клоун, додик и т.д.||  \n\n"
                                                                "→ 3a преднамеренно ***'неудобные' фразы***, которые могут быть ***не оскорбительными***, но несут при этом ***вред пользователю.*** \n _Пример:_ || Спойлеры к фильмам, сериалам и т.д.||", inline=False)
        embed.add_field(name="Мут на 30 минут выдаётся за:", value="→ За ***оскорбление*** пользователя. \n\n"
                                                                    "→ За любые ***триггеры*** и ***провокации***, с целью ***вызвать*** агрессивную реакцию. \n\n"
                                                                    "→ За ***двукратное нарушение*** правил, наказанием которых является ***_мут на 5 минут._***", inline=False)
        embed.add_field(name="Мут на 60 минут выдаётся за:", value="→ За ***агитацию*** пользователей ***на действия***, которые ***противоречат*** регламенту сервера. \n\n"
                                                                    "→ За вербальную ***рекламу*** любых других ***дискорд серверов.*** _Пример:_ ||А вы были на СамыйЛучшийСерверПланеты?||  \n\n"
                                                                    "→ За публичное ***обсуждение*** действий администрации в негативном ключе, а также за ***создание*** 'Хейт культа' административного состава.", inline=False)
        embed.add_field(name="Бан выдаётся за:", value="→ За чрезмерную ***конфликтность.*** \n\n"
                                                        "→ За: 'Мне по||ху*|| на ваши правила'. \n\n"
                                                        "→ За ***деанон*** участников сервера и ***слив*** их ***личной информации.*** \n\n"
                                                        "→ За ***рассылки*** на сторонние ***discord-ресурсы***, независимо от того, было это сделано непосредственно на ***сервере*** или ***в личных сообщениях*** пользователя.", inline=False)
        embed.add_field(name="Важно:", value="→ За мут ***от 30 минут*** вы получаете ***warn***. \n\n"
                                              "→ Людям, ***получившим четвёртый варн***, выдаётся ***роль*** - <@&657236785839079474>. \n\n"
                                              "<@&665904227754967040>", inline=False)
        await ctx.send(embed = embed)



        embed=discord.Embed(title="Чтобы просмотреть все команды, пропиши /help и получи сообщение от нашего бота.", description="<@&665905009418043399>", color=0x8080ff)
        embed.set_author(name="Информация о возможности бота.", icon_url="https://i.imgur.com/MSfmMa1.jpg")
        embed.set_image(url = "https://data.whicdn.com/images/334484166/original.gif")
        await ctx.send(embed = embed)

    @commands.command()
    async def suggestions(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()

        mybd = connectBD()
        bdcursor = mybd.cursor()

        if ctx.author.id != ctx.guild.owner_id:
            bdcursor.execute("SELECT permision_owner FROM Moderator WHERE id = {}".format(ctx.author.id))
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

        embed=discord.Embed(title="Если у вас есть предложение как можно улучшить сервер вы можете описать их тут.", description="Если во время проведение времени на сервере у вас возникли идей как можно было улучшить сервер или нашли какой-то bug вы можете описать все здесь.", color=0x8080ff)
        embed.add_field(name="Форма подачи:", value="```Тип: Предложение/Баг\nХотите получить вознаграждение?: Да/Нет\nОписание: Text\n```", inline=False)
        embed.set_footer(text="Если ваши сообщение будут не по тебе вы рискуете получить роль Toxic")
        embed.set_image(url = "https://xakinfo.ru/wp-content/uploads/2019/01/3fYL8i6Q-n-155t3dn_4jDknYN0aCPtudyMf63Csj0WcqbLRuyEIHKcG7ADvf27.gif")
        await ctx.send(embed = embed)