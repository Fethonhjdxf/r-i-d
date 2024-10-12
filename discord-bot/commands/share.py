import discord
from discord.ext import commands
import subprocess

class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_share(self, ctx, remote):
        result = subprocess.run(['rclone', 'link', remote], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Shareable link for {remote}:**\n{result.stdout}")
        else:
            await ctx.send(f"Error generating shareable link: {result.stderr}")
