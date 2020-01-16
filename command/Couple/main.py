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

class Marry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def couple(self,ctx,arg1=None):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0

        await ctx.message.delete()
        if not arg1:
            helpmessage = await ctx.channel.send("Привет <@{}>, я вижу что у тебя проблемы с командой couple! Я тебе помогу:"
                                    "```/couple [@link]```\n".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            return 0

        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT balance,couple FROM Users WHERE id = {}".format(ctx.author.id))
        info = bdcursor.fetchall()
        balance = int(info[0][0])
        if balance < 2500:
            helpmessage = await ctx.send("<@!{}> Свадьба это дорогая услуга, для нее тебе нужно 2500🍭".format(ctx.author.id))
            await asyncio.sleep(5)
            await helpmessage.delete()
            myBD.commit()
            return 0
        if info[0][1] != "Одинок":
            helpmessage = await ctx.send("Эй ты!! У тебя уже есть пара, сначала нужно разойтись! /divorce")
            await asyncio.sleep(5)
            await helpmessage.delete()
            myBD.commit()
            return 0
        try:
            member = ctx.guild.get_member(findid(arg1))

            if member.id == ctx.author.id:
                raise ValueError

            embed=discord.Embed(title="Предложение руки и сердца", description="Наконец-то <@!{}> собрал яйца в кулак и решил сделать предложение.".format(ctx.author.id), color=0x8080ff)
            embed.add_field(name="Кто же это?", value="<@!{}>,а ты знала, что <@!{}> тайно в тебя влюблён и предлагает тебе стать его второй половинкой, ты согласна?".format(member.id,ctx.author.id), inline=False)
            embed.set_footer(text="✅ - ДА или ❌ НЕТ")
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def check(reaction, user):
                if user == member and str(reaction.emoji) == '✅':
                    return True
                elif user == member and str(reaction.emoji) == '❌':
                    return True
            
            info = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(info[0]) == "✅":
                embed=discord.Embed(title= "Ура,поздравим наших молодожен",description="{} и {} теперь вместе!".format(member,ctx.author),color=0xff8080)
                embed.set_image(url = "https://thumbs.gfycat.com/TerrificHonoredAlbatross-size_restricted.gif")
                embed.set_footer(text="С вас сняли 2500🍭")
                await message.delete()
                await ctx.send(embed=embed)
                balance -= 2500

                bdcursor.execute("UPDATE Users set balance = {}, couple = {} WHERE id = {}".format(balance,member.id,ctx.author.id))
                
                bdcursor.execute("UPDATE Users set couple = {} WHERE id = {}".format(ctx.author.id,member.id))

                role = ctx.guild.get_role(658008634717896705)

                await member.add_roles(role)
                await ctx.author.add_roles(role)

                sql = "INSERT INTO Roles VALUES(%s,%s,%s)"
                val = (member.id,member.name,658008634717896705)
                bdcursor.execute(sql,val)

                val = (ctx.author.id,ctx.author.name,658008634717896705)
                bdcursor.execute(sql,val)

            elif str(info[0]) == "❌":
                embed=discord.Embed(title= "Все очень плохо.",description="<@!{}>, видимо у <@!{}> другие планы, и ты в них не входишь".format(ctx.author.id,member.id),color=0xff8080)
                embed.set_image(url = "http://s1.favim.com/orig/150923/anime-girl-gif-sad-anime-Favim.com-3345161.gif")
                await message.delete()
                await ctx.send(embed=embed)
            else:
                raise ValueError

        except ValueError:
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        except asyncio.TimeoutError:
            await message.delete()
            ErrorMessage = await ctx.send("<@!{}> время вышло, видно тебя продинамили!".format(ctx.author.id))
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
        myBD.commit()

    @commands.command()
    async def divorce(self,ctx):
        if ctx.message.guild == None:
            await ctx.send("Простите но хозяйн не позволяет мне общеться с незнакомцами вне гильдии :(")
            return 0
            
        await ctx.message.delete()
        myBD = connectBD()
        bdcursor = myBD.cursor()

        bdcursor.execute("SELECT couple FROM Users WHERE id = {}".format(ctx.author.id))
        info = bdcursor.fetchall()

        if info[0][0] == "Одинок":
            helpmessage = await ctx.send("Ты и так одинок с кем ты собрался разводится.")
            await asyncio.sleep(5)
            await helpmessage.delete()
            myBD.commit()
            return 0
        
        try:
            member = ctx.guild.get_member(findid(info[0][0]))

            bdcursor.execute("UPDATE Users set couple = 'Одинок' WHERE id = {}".format(ctx.author.id))
            bdcursor.execute("UPDATE Users set couple = 'Одинок' WHERE id = {}".format(member.id))

            role = ctx.guild.get_role(658008634717896705)

            await ctx.author.remove_roles(role)
            await member.remove_roles(role)

            bdcursor.execute("DELETE FROM Roles WHERE id = {} and roles_id = {}".format(member.id,658008634717896705))
            bdcursor.execute("DELETE FROM Roles WHERE id = {} and roles_id = {}".format(ctx.author.id,658008634717896705))

            embed=discord.Embed(title="Развод", description="{} больше не может терпеть {}, и решил, что пришло время развестись.".format(ctx.author,member.name))
            embed.set_footer(text="Мне очень жалко что ваш брак сломался.")
            embed.set_image(url = "https://www.animatedimages.org/data/media/1498/animated-sad-image-0019.gif")
            await ctx.send(embed=embed)
        except ValueError: 
            ErrorMessage =  await ctx.channel.send("Бип-Буп, что-то пошло не так!")
            await asyncio.sleep(5)
            await ErrorMessage.delete()
        
        myBD.commit()