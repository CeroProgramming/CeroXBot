class Output(object):

    def __init__(self):
        pass

    async def io_message(self, content, destintation):
        self.send_typing(destintation)
        self.send_message(destintation, content)
        return

    async def io_embed(self, embed, destintation):
        self.send_typing(destintation)
        self.send_message(destintation, embed=embed)

    async def create_embed(self, title, url, description):
        embed = discord.Embed(title="Github CeroProgramming", url="https://github.com/", description="GitHub Profile URL", color=0xc200ff)
        embed.set_author(name="CeroProgramming", url="https://github.com/CeroProgramming",, icon_url="https://avatars3.githubusercontent.com/u/22818389?s=460&v=4")
        embed.set_thumbnail(url="https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.freepik.com%2Ffree-icon%2Fgithub-logo_318-53553.jpg&f=1")
        embed.set_footer(text="This is a footer")
        return embed

    async def add_field(self, embed, name, value, inline=True):
        embed.add_field(name="Hello", value="World", inline=True)
        return embed
