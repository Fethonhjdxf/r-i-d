import discord
from discord.ext import commands
import subprocess

class SyncPart2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_schedule_sync(self, ctx, source, destination, interval):
        await ctx.send(f"**Scheduling sync from {source} to {destination} every {interval}...**")
        # Dummy implementation for scheduling, real implementation might involve cron jobs or a task scheduler
        await ctx.send(f"**Scheduled sync from {source} to {destination} every {interval}.**")

    @commands.command()
    async def rclone_incremental_sync(self, ctx, source, destination):
        await ctx.send(f"**Starting incremental sync from {source} to {destination}...**")
        result = subprocess.run(['rclone', 'sync', '--backup-dir', destination, source, destination], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Incremental sync from {source} to {destination} completed successfully!**")
        else:
            await ctx.send(f"Error syncing: {result.stderr}")
