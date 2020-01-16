import discord
from discord.ext.commands import Bot as Client
from command.Administrator.main import Administrator
from command.Owner.main import Owner
from command.User.main import Users
from command.Couple.main import Marry
from command.Money.main import Money
from command.role.main import role
from command.help.main import helps
from command.Casino.main import Casino
from command.reaction.pair import reaction_pair
from command.reaction.single import reaction_single

class Shinobu(Client):
    def __init__(self,bot_token=None,bot_prefix="/",bot_name="Shinobu"):
        super().__init__(command_prefix=bot_prefix)

        if not bot_token:
            raise ValueError("You did not specify a bot token")

        self.bot_token = bot_token
        self.bot_prefix = bot_prefix
        self.bot_name = bot_name

    def run(self, *args, **kwargs):
        print("\n\n=======================================================================================================\n")
        print("Hello,my name is {},and i boot for you.".format(self.bot_name))
        @self.listen()
        async def on_ready():
            print("\nI am ready!! \n\n")

        self.remove_command("help")

        self.add_cog(Owner())
        self.add_cog(Administrator())
        self.add_cog(Users())
        self.add_cog(Marry(self))
        self.add_cog(Money())
        self.add_cog(role())
        self.add_cog(helps())
        self.add_cog(Casino(self))
        self.add_cog(reaction_pair())
        self.add_cog(reaction_single())

        super().run(self.bot_token, *args, **kwargs)