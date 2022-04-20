import disnake
from disnake.ext import commands
import requests
import pathlib
import zipfile
import os
import asyncio

token = 'Discloud Token'

class Owner(commands.Cog, name = "Owner"):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(help = 'Logs do bot', aliases = ['log'])
    @commands.is_owner()
    async def logs(self, ctx):
        async with ctx.typing():
            
            re = requests.get("https://discloud.app/api/v2/app/bot_id/logs", headers={"api-token": token}).json()
            res = re['logs'][:1018]
            li = re['link']

            oEmbed = disnake.Embed(title = 'Log:', color = 0xffb354, description = f'[Link do log]({li})')
            oEmbed.set_author(name = 'Pão Bot', icon_url = 'Bot avatar')
            oEmbed.add_field(name ='\u200b', value = f'```{res}```', inline=False)
            oEmbed.set_thumbnail(url = 'https://cdn-icons-png.flaticon.com/512/2125/2125009.png')

            await ctx.reply(embed = oEmbed)

    @commands.command(help = 'Reinicia o bot(*Apenas o dono do bot pode utilizar este comando*)', aliases = ['reiniciar', 'r'])
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.reply('Reiniciando <a:digitando:931267989033082901>')
        result = requests.post("https://discloud.app/api/v2/app/bot_id/restart", headers={"api-token": token}).json()

    @commands.command(help = 'Faz o backup do bot e envia em zip', aliases = ['b','bk'])
    @commands.is_owner()
    async def backup(self, ctx):

        dire = pathlib.Path('./')
        with zipfile.ZipFile('backup.zip', mode = 'w') as archive:
            for file_path in dire.rglob('*'):
                archive.write(file_path, arcname=file_path.relative_to(dire))
        await ctx.author.send(file = disnake.File(r'backup.zip'))
        os.remove('backup.zip')
        await ctx.message.add_reaction('✅')
        




    @commands.Cog.listener()
    async def on_ready(self):
        print('Owner carregado!')


def setup(bot):
    bot.add_cog(Owner(bot))