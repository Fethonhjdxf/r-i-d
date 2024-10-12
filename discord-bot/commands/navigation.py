import os
import discord
from discord.ext import commands
import subprocess
import requests

navigation_sessions = {}

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

class Navigation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_ls(self, ctx, remote):
        result = subprocess.run(['rclone', 'lsf', remote], capture_output=True, text=True)
        if result.returncode == 0:
            message = f"**Listing for {remote}:**\n{result.stdout}"
            msg = await ctx.send(message)
            
            folder_mapping = {}
            path_mapping = {}
            for idx, line in enumerate(result.stdout.split('\n')):
                if line.endswith('/'):
                    emoji_folder = '📁'
                    emoji_path = f'🏷️{idx}'
                    folder_mapping[emoji_folder + str(idx)] = line.strip('/')
                    path_mapping[emoji_path + str(idx)] = f"{remote}{line.strip()}"
                    await msg.add_reaction(emoji_folder)
                    await msg.add_reaction(emoji_path)
                elif line:
                    emoji_path = f'🏷️{idx}'
                    emoji_download = f'📥{idx}'
                    path_mapping[emoji_path + str(idx)] = f"{remote}{line.strip()}"
                    await msg.add_reaction(emoji_path)
                    await msg.add_reaction(emoji_download)
            
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⏪')
            navigation_sessions[msg.id] = {
                'remote': remote,
                'msg': msg,
                'path': remote,
                'prev_path': None,
                'folder_mapping': folder_mapping,
                'path_mapping': path_mapping
            }
        else:
            await ctx.send(f"Error listing {remote}: {result.stderr}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        session = navigation_sessions.get(reaction.message.id)
        if session:
            if reaction.emoji == '⬆️':
                new_path = '/'.join(session['path'].split('/')[:-1])
                if not new_path:
                    new_path = session['remote']
                await self.update_listing(session, reaction, new_path)

            elif reaction.emoji == '⏪':
                new_path = session['prev_path'] if session['prev_path'] else session['path']
                await self.update_listing(session, reaction, new_path)

            elif reaction.emoji + str(reaction.count - 1) in session['folder_mapping']:
                new_path = f"{session['path']}/{session['folder_mapping'][reaction.emoji + str(reaction.count - 1)]}"
                await self.update_listing(session, reaction, new_path)

            elif reaction.emoji + str(reaction.count - 1) in session['path_mapping']:
                path = session['path_mapping'][reaction.emoji + str(reaction.count - 1)]
                self.send_webhook(path)

            elif '📥' in reaction.emoji:
                path = session['path_mapping'][reaction.emoji.replace('📥', '🏷️')]
                await self.send_download_link(ctx, path)

    async def update_listing(self, session, reaction, new_path):
        result = subprocess.run(['rclone', 'lsf', new_path], capture_output=True, text=True)
        if result.returncode == 0:
            message = f"**Listing for {new_path}:**\n{result.stdout}"
            await session['msg'].edit(content=message)
            session['prev_path'] = session['path']
            session['path'] = new_path
            
            await session['msg'].clear_reactions()
            folder_mapping = {}
            path_mapping = {}
            for idx, line in enumerate(result.stdout.split('\n')):
                if line.endswith('/'):
                    emoji_folder = '📁'
                    emoji_path = f'🏷️{idx}'
                    folder_mapping[emoji_folder + str(idx)] = line.strip('/')
                    path_mapping[emoji_path + str(idx)] = f"{new_path}{line.strip()}"
                    await session['msg'].add_reaction(emoji_folder)
                    await session['msg'].add_reaction(emoji_path)
                elif line:
                    emoji_path = f'🏷️{idx}'
                    emoji_download = f'📥{idx}'
                    path_mapping[emoji_path + str(idx)] = f"{new_path}{line.strip()}"
                    await session['msg'].add_reaction(emoji_path)
                    await session['msg'].add_reaction(emoji_download)
                    
            await session['msg'].add_reaction('⬆️')
            await session['msg'].add_reaction('⏪')
            session['folder_mapping'] = folder_mapping
            session['path_mapping'] = path_mapping
        else:
            await reaction.message.channel.send(f"Error listing {new_path}: {result.stderr}")

    async def send_download_link(self, ctx, path):
        result = subprocess.run(['rclone', 'link', path], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"Download link for {path}: {result.stdout.strip()}")
        else:
            await ctx.send(f"Error generating download link: {result.stderr}")

    def send_webhook(self, path):
        data = {
            "content": f"Path: {path}"
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"Failed to send webhook: {response.status_code}")
