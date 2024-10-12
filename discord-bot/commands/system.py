import discord
from discord.ext import commands
import psutil

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sysinfo(self, ctx):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        message = (
            f"**System Information**\n"
            f"**CPU Usage:** {cpu}%\n"
            f"**Memory Available:** {memory.available / (1024 ** 3):.2f} GB\n"
            f"**Memory Total:** {memory.total / (1024 ** 3):.2f} GB\n"
            f"**Disk Available:** {disk.free / (1024 ** 3):.2f} GB\n"
            f"**Disk Total:** {disk.total / (1024 ** 3):.2f} GB"
        )
        await ctx.send(message)
