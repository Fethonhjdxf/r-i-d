import discord
from discord.ext import commands

class UserManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_user_add(self, ctx, username):
        await ctx.send(f"User {username} added to access list")

    @commands.command()
    async def rclone_user_remove(self, ctx, username):
        await ctx.send(f"User {username} removed from access list")
