import discord
import psutil
import emoji
import asyncio
from discord.ext import commands
from discord_slash import cog_ext

from External_functions import cembed, extract_color
from stuff import re, dev_users, ydl_op, req, dev_channel, load_from_file, deleted_message, prefix_dict, censor, \
    g_req


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color_message = None
        self.color_temp = extract_color(re[8])

    @commands.command()
    async def set_sessionid(ctx, sessionid):
        re[9] = sessionid
        await ctx.send(
            embed=discord.Embed(description="SessionID set", color=discord.Color(re[8]))
        )

    @commands.command(aliases=["cw"])
    async def clear_webhooks(self, ctx):
        webhooks = await ctx.channel.webhooks()
        print(webhooks)
        for webhook in webhooks:
            try:
                await webhook.delete()
            except Exception as e:
                print(e)

    @commands.command()
    async def show_webhooks(self, ctx):
        webhooks = await ctx.channel.webhooks()
        await ctx.send(str(webhooks))

    @commands.command()
    async def set_quality(self, ctx, number):
        if str(ctx.author.id) in dev_users:
            ydl_op["preferredquality"] = str(number)
            await ctx.send(
                embed=discord.Embed(
                    title="Done",
                    description="Bitrate set to " + number,
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You cant set the bitrate of the voice, only devs are allowed to do that",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=["color", "||"])
    async def theme_color(self, ctx, *, tup1=""):
        try:
            print(str(extract_color(re[8])))
            self.color_temp = extract_color(re[8])
            await ctx.send(f"Setting color {self.color_temp}")
            req()
            print("Theme color", str(ctx.author))
            if re[8] < 1000:
                re[8] = 1670655


            tup = [int(i) for i in tup1.replace("(", "").replace(")", "").split(",")] if tup1 != "" else ()
            if len(tup) < 3:
                self.color_message = await ctx.send(
                    embed=discord.Embed(
                        title="Color Init",
                        description="You must have three values in the form of tuple",
                        color=discord.Color(value=re[8]),
                    )
                )
                await self.color_message.add_reaction(emoji.emojize(":red_triangle_pointed_up:"))
                await self.color_message.add_reaction(
                    emoji.emojize(":red_triangle_pointed_down:")
                )
                await self.color_message.add_reaction(
                    discord.utils.get(self.bot.emojis, name="green_up")
                )
                await self.color_message.add_reaction(
                    discord.utils.get(self.bot.emojis, name="green_down")
                )
                await self.color_message.add_reaction(
                    discord.utils.get(self.bot.emojis, name="blue_up")
                )
                await self.color_message.add_reaction(
                    discord.utils.get(self.bot.emojis, name="blue_down")
                )
            else:
                self.color_temp = str(extract_color(re[8]))
                re[8] = discord.Color.from_rgb(*tup).value
                embed = discord.Embed(
                    title="New Color",
                    description=str(tup),
                    color=discord.Color(value=re[8]),
                )
                await self.color_message.edit(embed=embed)
            
            emos = [
                discord.utils.get(self.bot.emojis, name="blue_down"),
                discord.utils.get(self.bot.emojis, name="blue_up"),
                discord.utils.get(self.bot.emojis, name="green_down"),
                discord.utils.get(self.bot.emojis, name="green_up"),
                emoji.emojize(":red_triangle_pointed_up:"),
                emoji.emojize(":red_triangle_pointed_down:")
            ]

            while True:
                tt = list(self.color_temp)
                try:
                    def check(reaction,user):             
                        return reaction.emoji in emos and reaction.message == self.color_message
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=720,check = check)
                    if reaction.emoji == emos[0]:
                        self.color_temp = tt[2]-25
                        re[8] = discord.Color(*self.color_temp).value
                    if reaction.emoji == emos[1]:
                        self.color_temp = tt[2]+25
                        re[8] = discord.Color(*self.color_temp).value
                    if reaction.emoji == emos[2]:
                        self.color_temp = tt[1]-25
                        re[8] = discord.Color(*self.color_temp).value
                    embed=cembed(
                        title="New Color",
                        description=str(self.color_temp),
                        color=re[8]
                        )
                    await self.color_message.edit()
                        
                except asyncio.TimeoutError:
                    for i in emos:
                        await self.color_message.remove_reaction(i)
        except Exception as e:
            await self.bot.get_channel(dev_channel).send(
                embed=discord.Embed(
                    title="Error in Theme_Color",
                    description=str(e),
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=["$$"])
    async def recover(self, ctx):
        print("Recover", str(ctx.author))
        if str(ctx.author.id) in dev_users:
            try:
                load_from_file(".recover.txt")
                await ctx.send(embed=cembed(description="Recovery Done", color=re[8]))
            except Exception as e:
                channel = self.bot.get_channel(dev_channel)
                await channel.send(
                    embed=discord.Embed(
                        title="Recovery failed",
                        description=str(e),
                        color=discord.Color(value=re[8]),
                    )
                )
        else:
            await ctx.send(
                embed=cembed(title="Permissions Denied",
                             description="You cannot use this command, its only for developers",
                             color=re[8], thumbnail=self.bot.user.avatar_url_as(format="png")))
            await self.bot.get_channel(dev_channel).send(
                embed=cembed(description=f"{ctx.author.name} from {ctx.guild.name} tried to use Recover command"))

    @commands.command()
    async def load(self, ctx):
        print("Load", str(ctx.author))
        req()
        try:
            cpu_per = str(int(psutil.cpu_percent()))
            cpu_freq = (
                    str(int(psutil.cpu_freq().current)) + "/" + str(int(psutil.cpu_freq().max))
            )
            ram = str(psutil.virtual_memory().percent)
            swap = str(psutil.swap_memory().percent)
            usage = f"""
            CPU Percentage: {cpu_per}
            CPU Frequency : {cpu_freq}
            RAM usage: {ram}
            Swap usage: {swap}
            """
            embed = discord.Embed(
                title="Current load",
                description=usage,
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))
            await ctx.send(embed=embed)
        except Exception as e:
            channel = self.bot.get_channel(dev_channel)
            embed = discord.Embed(
                title="Load failed",
                description=str(e),
                color=discord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))
            await channel.send(embed=embed)

    @cog_ext.cog_slash(name="color", description="Change color theme", guild_ids=[822445271019421746])
    async def color_slash(self, ctx, rgb_color=""):
        await ctx.defer()
        await self.theme_color(ctx, tup1=rgb_color)

    @commands.command()
    async def snipe(self, ctx, number=0):
        if (
                ctx.author.guild_permissions.administrator
                or ctx.author.guild_permissions.manage_messages
                or ctx.guild.id not in [841026124174983188, 822445271019421746]
        ):
            if int(number) > 10:
                await ctx.send(
                    embed=cembed(
                        description="Cannot snipe more than 10 messages",
                        picture="https://images.news18.com/ibnlive/uploads/2015/08/Chandler-2.gif",
                        color=re[8],
                    )
                )
                return
            message = deleted_message.get(ctx.channel.id, [("Empty", "Nothing to snipe here")])[::-1]
            for i in message:
                number -= 1
                if len(i) < 3:
                    await ctx.send(
                        embed=discord.Embed(
                            description="**" + i[0] + ":**\n" + i[1],
                            color=discord.Color(value=re[8]),
                        )
                    )
                else:
                    await ctx.send("**" + i[0] + ":**")
                    await ctx.send(embed=i[1])
                if number <= 0:
                    break
        else:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description="Sorry guys, only admins can snipe now",
                    color=re[8],
                    thumbnail=self.bot.user.avatar_url_as(format="png"),
                )
            )

    @cog_ext.cog_slash(name="Snipe", description="Get the last few deleted messages")
    async def snipe_slash(self, ctx, number=0):
        req()
        await ctx.defer()
        await self.snipe(ctx, int(number))

    @commands.command()
    async def set_prefix(self, ctx, pref):
        if ctx.author.guild_permissions.administrator:
            prefix_dict[ctx.guild.id] = pref
            await ctx.send(
                embed=cembed(title="Done", description=f"Prefix set as {pref}", color=re[8])
            )
        else:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin",
                    color=re[8],
                )
            )

    @commands.command()
    async def remove_prefix(self, ctx):
        if ctx.author.guild_permissions.administrator:
            if prefix_dict.get(ctx.guild.id, False):
                prefix_dict.pop(ctx.guild.id)
            await ctx.send(
                embed=cembed(title="Done", description=f"Prefix removed", color=re[8])
            )
        else:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description="You cannot change the prefix, you need to be an admin",
                    color=re[8],
                )
            )

    @commands.command(aliases=["*"])
    async def change_nickname(self, ctx, member: discord.Member, *, nickname):
        if (
                ctx.author.guild_permissions.change_nickname
                or ctx.author.id == 432801163126243328
        ):
            await member.edit(nick=nickname)
            await ctx.send(
                embed=discord.Embed(
                    title="Nickname Changed",
                    description=(
                            "Nickname changed to "
                            + member.mention
                            + " by "
                            + ctx.author.mention
                    ),
                    color=discord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Permissions Denied",
                    description="You dont have permission to change others nickname",
                    color=discord.Color(value=re[8]),
                )
            )

    @commands.command(aliases=["hi"])
    async def check(self, ctx):
        req()
        print("check")
        em = discord.Embed(
            title="Online",
            description=f"Hi, <@{ctx.author.id}>\nLatency: {int(self.bot.latency * 1000)}",
            color=discord.Color(value=re[8]),
        )
        await ctx.send(embed=em)

    @cog_ext.cog_slash(name="check", description="Check if the bot is online")
    async def check_slash(self, ctx):
        req()
        await ctx.defer()
        await self.check(ctx)

    @commands.command(aliases=["cen"])
    async def add_censor(self, ctx, *, text):
        req()
        string = ""
        censor.append(text.lower())
        for i in range(0, len(text)):
            string = string + "-"
        em = discord.Embed(
            title="Added " + string + " to the list",
            decription="Done",
            color=discord.Color(value=re[8]),
        )
        await ctx.send(embed=em)

    @commands.command()
    async def get_req(self, ctx):
        req()
        number = g_req()
        em = discord.Embed(
            title="Requests", description=str(number), color=discord.Color(value=re[8])
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Utils(bot))
    
