import discord
from discord.ext import commands
import subprocess

class SyncPart1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_sync(self, ctx, source, destination):
        await ctx.send(f"**Starting two-way sync from {source} to {destination}...**")
        result = subprocess.run(['rclone', 'sync', source, destination], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Two-way sync from {source} to {destination} completed successfully!**")
        else:
            await ctx.send(f"Error syncing: {result.stderr}")

    @commands.command()
    async def rclone_oneway_sync(self, ctx, source, destination):
        await ctx.send(f"**Starting one-way sync from {source} to {destination}...**")
        result = subprocess.run(['rclone', 'copy', source, destination], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**One-way sync from {source} to {destination} completed successfully!**")
        else:
            await ctx.send(f"Error syncing: {result.stderr}")
