from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="clear", description="指定要刪除幾則訊息")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_msg(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message("重新輸入數量", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"deleted {len(deleted)} messages", ephemeral=True)

    @app_commands.command(name="kick", description="踢人")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_member(self, interaction: discord.Interaction, member: discord.Member):
        await member.kick()
        await interaction.response.send_message(f"踢掉 {member.mention}了", ephemeral=True)

    
    @app_commands.command(name="unban", description="讓他說話")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_member(self, interaction: discord.Interaction, user: discord.User, reason: str = "沒理由"):
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f" **{user}**回來了", ephemeral=True)
    
    @app_commands.command(name="ban", description="叫他閉嘴")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_member(self, interaction: discord.Interaction, member: discord.Member, reason: str = "沒理由"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"已禁言 **{member}**", ephemeral=True)

   

    @app_commands.command(name="untimeout", description="取消禁言")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout_member(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"恭喜 {member.mention}重獲言論自由。", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(Moderation(bot))

app = Flask('')

@app.route('/')
def home():
    return "上線了"

def run_flask():
  
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

async def main():
   
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
 
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
  	asyncio.run(main())
