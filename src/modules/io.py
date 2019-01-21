import asyncio
from discord import Embed


class IO(object):

    def __init__(self):
        pass

    async def io_message(self, destintation, content):
        await self.send_typing(destintation)
        await asyncio.sleep(0.5)
        await self.send_message(destintation, content)
        return

    async def io_embed(self, destintation, embed):
        await self.send_typing(destintation)
        await asyncio.sleep(0.5)
        await self.send_message(destintation, embed=embed)

    async def create_embed(self, embed_title, embed_url, embed_description, embed_color, author_name, author_url, author_icon_url, thumbnail_url, footer_text=""):
        embed = Embed(title=embed_title, url=embed_url, description=embed_description, color=embed_color)
        embed.set_author(name=author_name, url=author_url, icon_url=author_icon_url)
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text=footer_text)
        return embed

    async def add_field(self, embed, name, value, inline=True):
        embed.add_field(name="Hello", value="World", inline=True)
        return embed
