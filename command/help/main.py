from discord.ext import commands
import discord
import asyncio
import datetime
from BD.connect_bd import connectBD

class helps(commands.Cog):
    @commands.command()
    async def ahelp(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0
        await ctx.message.delete()
        embed=discord.Embed(title="Команды Администраций", description="Ниже вы можете найти все команды который вам понадобиться чтоб модерировать сервер.", color=0x8080ff)
        embed.add_field(name="Стандартные:", value="Данный команды получает любой модератор.\nВАЖНО: Права на их использование могут быть изъяты\n```"
                                                    "/antiafk - использовать чтоб вывести участника из афк.\n"
                                                    "/cls - использовать чтоб очистить чат.\n"
                                                    "/gethere - использовать для телепортирование учасника к себе.\n"
                                                    "/goto - использовать для перехода в канал участника.\n"
                                                    "/mute - использовать чтоб забрать у участника права говорить.\n"
                                                    "/unmute - использовать чтоб вернуть права учаснику.\n"
                                                    "/warn - использовать чтоб выдавать предупреждение учаснику.\n"
                                                    "/hide - использовать чтоб убрать роли Модератора.(В это время команды можно использовать).```", inline=False)
        embed.add_field(name="Дополнительные:", value="Данный команды получает только ограниченный круг лиц по просьбе Куратора.\n```"
                                                    "/ban - используют чтоб заблокировать участника.\n"
                                                    "/kick - используют чтоб кикнуть участника.\n"
                                                    "/clear - используют чтоб обнулить участника.```", inline=False)
        embed.set_footer(text="Если у вас есть вопросы можете спросить у Куратора.")
        message = await ctx.send("<@!{}> ответ на твой запрос был отправлен в личный сообщения.".format(ctx.author.id))
        await ctx.author.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()
    
    @commands.command()
    async def ohelp(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        embed=discord.Embed(title="Команды Основателя", description="Ниже вы можете найти все команды который вам понадобиться как основатели сервера.", color=0x8080ff)
        embed.add_field(name="Список команд:", value="Не нужно забывать что все мы люди.\n```"
                                                    "/add_role - использовать чтоб добавить роль участнику.\n"
                                                    "/dell_role - использовать чтоб удалить роль участнику.\n"
                                                    "/set - использовать чтоб управлять BD.\n"
                                                    "/create_akk - создать аккаунт участнику.\n"
                                                    "/add_moder - добавить модератора.\n"
                                                    "del_moder - удалить модератора.\n"
                                                    "/set_moder - модифицировать аккаунт модератора.```", inline=False)
        message = await ctx.send("<@!{}> ответ на твой запрос был отправлен в личный сообщения.".format(ctx.author.id))
        await ctx.author.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command()
    async def help(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        embed=discord.Embed(title="Основный команды сервера.", description="Ниже вы можете найти все команды который вам понадобиться чтоб весело проводить время на нашем сервере.", color=0x8080ff)
        embed.add_field(name="Участник:", value="```/stats - использовать чтоб посмотреть статистику.\n"
                                                "/avatar - использовать чтоб отобразить аватар участника.\n"
                                                "/instagram - использовать чтоб изменить свой Instagram.\n"
                                                "/status - использовать чтоб изменить свой статус.```", inline=False)
        embed.add_field(name="Экономика:", value="```/box_open - использовать чтоб открывать коробки.\n"
                                                "/give - использовать чтоб передавать 🍭.\n"
                                                "/give_box - использовать чтоб передать коробки.\n"
                                                "/timecoin - использовать чтоб получить бонус.\n"
                                                "/top - изспользовать чтоб выводить топ участников. ```", inline=False)
        embed.add_field(name="Свадьба:", value="```/couple - использовать чтоб создать брак.\n"
                                                "/divorce - использовать чтоб покинуть брак.```", inline=False)
        embed.add_field(name="Личная роль:", value="```/buyrole - использовать чтоб создать роль.\n"
                                                "/change_role - использовать чтоб модефицировать роль.\n"
                                                "/dellrole - использовать чтоб удалить роль.```", inline=False)
        embed.add_field(name="Магазин ролей:", value="```/shop - использовать чтоб посмотреть магазин.\n"
                                                "/buy - использовать чтоб купить роль из магазина.```", inline=False)
        embed.add_field(name="Казино:", value="```/crash - использовать чтоб посмотреть больше информаций.```", inline=False) 
        embed.add_field(name="Парные реакции:", value="```/bite @user - укусить.\n"
                                                            "/hug @user - обнять\n"
                                                            "/kiss @user - поцеловать\n"
                                                            "/lick @user - облизать\n"
                                                            "/pet @user - погладить\n"
                                                            "/seduce @user - соблазнить\n"
                                                            "/sex @user - заняться любовью\n"
                                                            "/slap @user - ударить пользователя```", inline=True)            
        embed.add_field(name="Одиночные  реакции:", value="```/bite @user - укусить.\n"     
                                                            "/angry - злиться\n" 
                                                            "/cry - плакать\n" 
                                                            "/happy - радость\n" 
                                                            "/roar - боевой клич\n" 
                                                            "/smoke - закурить```", inline=True)    
        embed.set_footer(text="Спасибо что ты с нами мы тебя любим 💙")
              
        message = await ctx.send("<@!{}> ответ на твой запрос был отправлен в личный сообщения 💙".format(ctx.author.id))
        await ctx.author.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()