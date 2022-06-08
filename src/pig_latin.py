def requirements():
    return ["re"]


def main(client, re):
    import discord

    @client.command()
    async def eng2pig(ctx, *, data):
        output = ""
        for i in data.split(" "):
            a = str(i)
            a = a.lower()
            a = a + a[0] + "ay"
            a = list(a)
            a.remove(a[0])

            a = "".join(a)
            output += f"{a} "
        await ctx.send(
            embed=discord.Embed(
                title="igpay atinlay",
                description=str(output),
                color=discord.Color(value=re[8]),
            )
        )

    @client.command()
    async def pig2eng(ctx, *, data):
        output = ""
        for i in data.split(" "):
            b = i.lower()
            for _ in range(1, 3):
                b = b[:-1]

            b = b[len(b) - 1] + b[:-1]
            output += f"{b} "
        await ctx.send(
            embed=discord.Embed(
                title="English Again",
                description=str(output),
                color=discord.Color(value=re[8]),
            )
        )
