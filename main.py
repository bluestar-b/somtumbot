
import os
import discord
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    
    print(f"🚀 {bot.user.name} is online!")
    print(f"🔧 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} servers")
    print(f"🤖 Running on Pycord v{discord.__version__}")
 

for filename in os.listdir('./cogs'):
    if filename.endswith('_cog.py'):
        module = f'cogs.{filename[:-3]}'
        print(f"📑 Module {module} loaded!")
        bot.load_extension(module)
        
 
if __name__ == '__main__':
    bot.run(os.getenv("BOT_TOKEN"))