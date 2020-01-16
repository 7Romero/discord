from discord.ext import commands
import discord
import asyncio
import mysql.connector
from BD.connect_bd import connectBD
import random
from decimal import Decimal # Библиотека которая фиксет float

def findid(message):
    message = message.replace("<","")
    message = message.replace("@","")
    message = message.replace("!","")
    message = message.replace(">","")
    message = message.replace("&","")
    return int(message)

class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crash(self,ctx,arg = None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if arg == None: # Проверка если игрок написал ставку
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой crash! Я тебе помогу:"
                                    "```/crash [Ставка]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
        select = bdcursor.fetchall()
        balance = int(select[0][0])

        try:

            arg = int(arg)

            if arg <= 0:
                helpmessage = await ctx.channel.send("Привет <@{}>, ставка должна быть больше 0.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            if arg > 500:
                helpmessage = await ctx.channel.send("Привет <@{}>, ставка должна быть меньше 500.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            if balance < arg:
                helpmessage = await ctx.channel.send("Привет <@{}>, тебе не хватает 🍭 чтоб сыграть.".format(ctx.author.id))
                await asyncio.sleep(5)
                await helpmessage.delete()
                myBD.commit()
                return 0

            bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance - int(arg),ctx.author.id))

            coef = Decimal("1.00") # var с основной info
            valute = 0
            embed=discord.Embed(title="Казино |  Игрок: {}".format(ctx.author)) # Делаем вид embed
            embed.add_field(name="Коэффициент", value="{}".format(coef), inline=True)
            embed.add_field(name="Прибыли", value="{} 🍭".format(valute), inline=True)
            embed.set_footer(text="Чтоб остановиться нажмите на реакцию")
            message = await ctx.send(embed=embed)
            await message.add_reaction("⛔")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '⛔'

            Crash = True
            while Crash == True:
                try:
                    await self.bot.wait_for('reaction_add', timeout=3.0, check=check)
                except asyncio.TimeoutError:
                    if random.randint(1,10) == 3:
                        Crash = False
                        embed.clear_fields()
                        embed=discord.Embed(title="Казино |  Игрок: {}".format(ctx.author),color=0xff0000)
                        embed.add_field(name="Коэффициент упал:", value="{}".format(coef), inline=True)
                        embed.add_field(name="Возможная прибыли:", value="{} 🍭".format(valute), inline=True)
                        embed.add_field(name="Теперь ваш баланс:",value="{}".format(balance-arg),inline=False)
                        embed.set_footer(text="Больше не нужно так сильно рисковать!")
                    else:
                        coef += Decimal("0.20")
                        valute = int(arg * coef)
                
                        embed.clear_fields()
                        embed.add_field(name="Коэффициент", value="{}".format(coef), inline=True)
                        embed.add_field(name="Прибыли", value="{} 🍭".format(valute), inline=True)
                else:
                    bdcursor.execute("SELECT balance FROM Users WHERE id = {}".format(ctx.author.id))
                    select = bdcursor.fetchall()
                    balance = int(select[0][0])


                    Crash = False
                    embed.clear_fields()
                    embed=discord.Embed(title="Казино |  Игрок: {}".format(ctx.author),color=0x00ff00)
                    embed.add_field(name="Коэффициент остоновлен:", value="{}".format(coef), inline=True)
                    embed.add_field(name="Вы выиграли:", value="{} 🍭".format(valute), inline=True)
                    embed.add_field(name="Теперь ваш баланс:",value="{}".format(balance+valute),inline=False)
                    embed.set_footer(text="Поздравляю тебя с победой")

                    bdcursor.execute("UPDATE Users set balance = {} WHERE id = {}".format(balance+valute,ctx.author.id))

                await message.edit(embed=embed)
        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()

        myBD.commit()