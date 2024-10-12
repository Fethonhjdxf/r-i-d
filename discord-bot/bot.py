import discord
from discord.ext import commands
from commands import navigation, system, rclone, upload, share, backup, watch, stats, health_check, user_management, logging, notify, search, sync
from commands.status.status_tracking_part1 import Status

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.add_cog(Status(bot))
bot.add_cog(navigation.Navigation(bot))
bot.add_cog(system.System(bot))
bot.add_cog(rclone.Rclone(bot))
bot.add_cog(upload.Upload(bot))
bot.add_cog(share.Share(bot))
bot.add_cog(backup.Backup(bot))
bot.add_cog(watch.Watch(bot))
bot.add_cog(stats.Stats(bot))
bot.add_cog(health_check.HealthCheck(bot))
bot.add_cog(user_management.UserManagement(bot))
bot.add_cog(logging.Logging(bot))
bot.add_cog(notify.Notify(bot))
bot.add_cog(search.Search(bot))
bot.add_cog(sync.Sync(bot))

bot.run('YOUR_DISCORD_BOT_TOKEN')
