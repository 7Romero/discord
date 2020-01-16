import discord
from discord.ext.commands import Bot as Client
import asyncio
import Event.main as Events


class Tanjiro(Client):
    def __init__(self,bot_token=None,bot_prefix="/////////////////////////////////",bot_name="Tanjiro"):
        super().__init__(command_prefix=bot_prefix)

        if not bot_token:
            raise ValueError("You did not specify a bot token")

        self.bot_token = bot_token
        self.bot_name = bot_name

    def run(self, *args, **kwargs):
        print("\n\n=======================================================================================================\n")
        print("Hello,my name is {},and i boot for you.".format(self.bot_name))
        @self.listen()
        async def on_ready():
            print("\nI am ready!! ")
            await Events.calculated_online(self.get_guild(651865140375060496))

        @self.listen()
        async def on_member_join(member):
            await Events.NewMember(member)

        @self.listen()
        async def on_message(message):
            if message.guild == None:
                return 0
            await asyncio.sleep(3)
            if not message:
                return 0 
            await Events.add_message(message)

        @self.listen()
        async def on_voice_state_update(member,before,after):
            if after.channel:
                if after.channel.id == 655730901187166248: # Voice ID
                    channel = self.get_channel(655730862595244032) # Group Voice ID
                    newchannel = await channel.create_voice_channel(name = " | Канал #{}".format(member.discriminator))
                    await member.move_to(newchannel)
                    await newchannel.set_permissions(member, manage_channels = True,move_members = True)
                elif after.channel.id == 659331200732758026:
                    channel = self.get_channel(655843765843656728) # Group Voice ID
                    newchannel = await channel.create_voice_channel(name = " | Канал #{}".format(member.discriminator))
                    await member.move_to(newchannel)
                    await newchannel.set_permissions(member, manage_channels = True,move_members = True)
            if before.channel:
                if before.channel.id != 655730901187166248 and before.channel.category_id == 655730862595244032 and not before.channel.members: # Verifica daca canalul este din Voice Create si ne este canalul care creaza canalele
                    await before.channel.delete()
                elif before.channel.id != 659331200732758026 and before.channel.category_id == 655843765843656728 and not before.channel.members:
                    await before.channel.delete()
            else:
                pass
            
            info_online = 0 
            listchannels = member.guild.voice_channels # Lista de canale
            for channel in listchannels: # parcurge canalele 
                if len(channel.members) != 0:
                    info_online += len(channel.members)
            channel = discord.utils.get(member.guild.voice_channels, id = 655720130294186004)
            await channel.edit(name = "🐾 | Онлайн: {}".format(info_online))

        super().run(self.bot_token, *args, **kwargs)