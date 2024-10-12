import discord
from discord.ext import commands

class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_notify(self, ctx, activity, user):
        await ctx.send(f"Notifications set for {activity} to {user}")
