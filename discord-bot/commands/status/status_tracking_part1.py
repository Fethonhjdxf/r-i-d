import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.operations = {}

    @commands.command()
    async def rclone_status(self, ctx):
        if self.operations:
            status_message = "**Current Operations:**\n"
            for idx, (op, details) in enumerate(self.operations.items(), start=1):
                status_message += f"{idx}. {details['description']} ({details['status']})\n"
            await ctx.send(status_message)
        else:
            await ctx.send("No ongoing operations.")

    def update_status(self, op_id, description, status):
        self.operations[op_id] = {'description': description, 'status': status}

    def remove_operation(self, op_id):
        if op_id in self.operations:
            del self.operations[op_id]
