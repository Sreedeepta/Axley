import discord, pymongo, asyncio

from discord.ext import commands

class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        db = self.bot.db()
        self.collection = db['prefix']
        self.emojis = self.bot.cool_emojis

    @commands.command(
        name='SetPrefix',
        aliases=[
            'Changeprefix',
            'Prefix'
        ],
        description="Set's the custom prefix of the guild"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def prefix(self, ctx: commands.Context, *, pre):

        data = self.collection.find_one({'_id': ctx.guild.id})

        if not data:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description='Are you sure you want to set the server prefix to `{}` ?'.format(pre)
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == '✅'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.message.add_reaction('❎')
                await message.remove_reaction('✅')
            else:
                self.collection.insert_one({'_id': ctx.guild.id, 'prefix': str(pre)})
                embed = discord.Embed(
                    color=discord.Color.magenta(),
                    description="{} Successfully changed the custom prefix of this server to `{}`".format(self.emojis['tick'], pre)
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description='Are you sure you want to update the server prefix to `{}` ?'.format(pre)
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == '✅'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.message.add_reaction('❎')
            else:
                self.collection.update_one({'_id': ctx.guild.id}, {'$set': {'prefix': str(pre)}})
                embed = discord.Embed(
                    color=discord.Color.magenta(),
                    description="{} Successfully changed the custom prefix of this server to `{}`".format(self.emojis['tick'], pre)
                )
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Prefix(bot))