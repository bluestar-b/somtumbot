import discord
import time
from discord.ext import commands
from discord.commands import slash_command
import requests
import os


def fetch_player_info(player_id):
    api_host = os.getenv("API_HOST")
    url = f"{api_host}/get_player_info?id={player_id}&scope=info"
    print(url)
    try:
        info = requests.get(url)
        return info.json()
    except requests.RequestException as e:
        print(f"Error fetching player info: {e}")
        return None


class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
    @slash_command(name="whois", description="Check player information")
    async def whois(self, ctx, user_id: int):
        player_info = fetch_player_info(user_id)
        embed = discord.Embed(title="Player information")
        embed.set_image(url=f"{os.getenv('AVATAR_HOST')}/{user_id}")
        print(f"{os.getenv('AVATAR_HOST')}/{user_id}.png")
        embed.add_field(name="User ID", value=player_info['player']['info']['id'], inline=False)
        embed.add_field(name="User Name", value=player_info['player']['info']['name'], inline=False)
        embed.add_field(name="Creation Date", value=f"<t:{player_info['player']['info']['creation_time']}:F>", inline=False)
    
        embed.add_field(name="Profile Link", value=f'{os.getenv("HOST")}/u/{user_id}', inline=False)
        
        embed.set_thumbnail(url=f"{os.getenv('FLAGS_HOST')}/{player_info['player']['info']['country'].upper()}.png")
        
        await ctx.respond(embed=embed)
        
        
        
    @slash_command(name="uptime", description="Check the bot's uptime.")
    async def uptime(self, ctx):
        current_time = time.time()
        uptime_seconds = round(current_time - self.start_time)
        uptime_string = self.format_seconds(uptime_seconds)
        
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"The bot has been running for: {uptime_string}",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed)

    def format_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def setup(bot):
    bot.add_cog(utility(bot))
