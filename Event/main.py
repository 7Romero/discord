import mysql.connector
import discord
import datetime
import asyncio
from BD.connect_bd import connectBD

async def NewMember(member):
    myBD = connectBD()
    bdcursor = myBD.cursor()
    bdcursor.execute("SELECT * FROM Users WHERE id = {}".format(member.id))
    myresult = bdcursor.fetchall()
    if not myresult :
        time = datetime.datetime.today()

        sql = "INSERT INTO Users (id,name,couple,time_coin,instagram,AboutMe) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (member.id,member.name,"Одинок",time,"Нету:(","Аноним")
        bdcursor.execute(sql,val)
        # embed
        embed=discord.Embed(title="Приветствие.", description="Привет, видно ты тут первый раз. Я рад что ты выбрал наш сервер.", color=0x1de240)
        embed.add_field(name="Что нужно знать?", value="Если ты хочешь приятно проводить время на нашем сервере сначала прочитай правила чтоб понять что можно и что нельзя делать)", inline=False)
        embed.set_footer(text="Обращайся с людьми так как хочешь чтобы обращались с тобой :)")
        await member.send(embed=embed)

        role = member.guild.get_role(656100483399942146)
        await member.add_roles(role)

        sql = "INSERT INTO Roles VALUES (%s,%s,%s)"
        val = (member.id,member.name,role.id)
        bdcursor.execute(sql,val)

        sql = "INSERT INTO Mine (id,minetype1,minetype2,minetype3,minetype4,minetype5,minetype6) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (member.id,"0","0","0","0","0","0")
        bdcursor.execute(sql,val)
    else:
        embed=discord.Embed(title="Приветствие.", description="Вау-у-у это опять ты? Где ты пропадал? Тебя уже все ждут заходи быстрее!", color=0x1de240)
        embed.add_field(name="Ты же не первый раз тут?", value="Привет, мы тебя уже заждались не бойся я запомнил все твои достижения и сохранил их, у тебя остались те же данные.", inline=False)
        embed.set_footer(text="Обращайся с людьми так как хочешь чтобы обращались с тобой :)")
        await member.send(embed=embed)
        bdcursor.execute("SELECT roles_id FROM Roles WHERE id = {}".format(member.id))
        myresult = bdcursor.fetchall()

        for i in range(len(myresult)):
            member.guild.get_role(myresult[i][0])
            role = member.guild.get_role(int(myresult[i][0]))
            if not role:
                sql = "DELETE FROM Roles WHERE roles_id = {}".format(myresult[i][0])
                bdcursor.execute(sql) 
            else:
                await member.add_roles(role)
    myBD.commit()

async def add_message(message):
    myBD = connectBD()
    bdcursor = myBD.cursor()

    bdcursor.execute("SELECT chat_message FROM Users WHERE id = {}".format(message.author.id))
    select = bdcursor.fetchall()
    if not select:
        myBD.commit()
        await NewMember(message.author)
        return 0
    chat_message = int(select[0][0])
    chat_message += 1
    bdcursor.execute("UPDATE Users set chat_message = {} WHERE id = {}".format(chat_message,message.author.id))
    myBD.commit()

async def calculated_online(guild):
    myBD = connectBD()
    bdcursor = myBD.cursor()
    listchannel = guild.voice_channels
    for channel in listchannel:
        if channel.id != 665615705068011540:
            for member in channel.members:
                bdcursor.execute("SELECT voice_online FROM Users WHERE id = {}".format(member.id))
                select = bdcursor.fetchall()

                if not select:
                    myBD.commit()
                    await NewMember(member)
                else:
                    bdcursor.execute("UPDATE Users set voice_online = {} WHERE id = {}".format(int(select[0][0])+5,member.id))
                    bdcursor.execute("SELECT last_box_given,box FROM Users WHERE id = {}".format(member.id))
                    last_box = bdcursor.fetchall()
                    if (int(select[0][0])+5-int(last_box[0][0]))//60 >= 12:
                        bdcursor.execute("UPDATE Users set last_box_given = {},box = {} WHERE id = {}".format(int(select[0][0])+5,int(last_box[0][1])+1,member.id))
                    myBD.commit()


    today = datetime.date.today()
    myBD = connectBD()
    bdcursor = myBD.cursor()

    bdcursor.execute("SELECT id FROM PrivateRole WHERE time <= {}".format(today))
    select = bdcursor.fetchall()

    if select:
        for i in range(0,len(select[0])):
            role = guild.get_role(select[0][i])
            if role:
                await role.delete()
            
            bdcursor.execute("DELETE FROM PrivateRole WHERE id = {}".format(select[0][i]))
            myBD.commit()

    await asyncio.sleep(300)
    await calculated_online(guild)