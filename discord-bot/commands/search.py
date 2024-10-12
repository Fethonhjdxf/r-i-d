import discord
from discord.ext import commands
import subprocess

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_sessions = {}

    @commands.command()
    async def rclone_search(self, ctx, keyword):
        remotes = subprocess.run(['rclone', 'listremotes'], capture_output=True, text=True).stdout.split('\n')
        results = []

        for remote in remotes:
            if remote.strip():
                search_result = subprocess.run(['rclone', 'lsf', '--filter', f'*{keyword}*', f'{remote}:'], capture_output=True, text=True).stdout
                if search_result.strip():
                    results.append((remote, search_result.split('\n')))

        if results:
            msg = await ctx.send(self.format_page(results, 0))
            await msg.add_reaction('⏮️')
            await msg.add_reaction('⏭️')
            for idx, (remote, _) in enumerate(results):
                await msg.add_reaction(f'🌐{idx+1}')
            self.search_sessions[msg.id] = {'results': results, 'page': 0}
        else:
            await ctx.send("No matching files found.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        session = self.search_sessions.get(reaction.message.id)
        if session:
            if reaction.emoji == '⏮️':
                session['page'] = max(0, session['page'] - 1)
            elif reaction.emoji == '⏭️':
                session['page'] = min(len(session['results']) - 1, session['page'] + 1)
            else:
                for idx, (remote, _) in enumerate(session['results']):
                    if reaction.emoji == f'🌐{idx+1}':
                        await reaction.message.edit(content=self.format_detailed_results(remote, session['results'][idx][1]))

            await reaction.message.edit(content=self.format_page(session['results'], session['page']))

    def format_page(self, results, page):
        content = []
        for remote, files in results:
            if len(files) > page * 10:
                content.append(f"**Results for {remote}:**")
                content.extend(files[page * 10:(page + 1) * 10])
        return "\n".join(content) + f"\n\nPage {page + 1}/{len(results)}\n⏮️ ⏭️"

    def format_detailed_results(self, remote, files):
        content = [f"**Detailed results for {remote}:**"]
        content.extend(files)
        return "\n".join(content) + f"\n\n⏮️ ⏭️"
