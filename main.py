import discord
import os
import requests
from keep_alive import keep_alive

client = discord.Client()


@client.event
async def on_ready():
    print(f"bot is logged in on {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith("hello"):
        await message.channel.send(
            f"hello {message.author}\nI am here to help with gathering all the github repos that you searched...")

        await message.channel.send("Enter the keyword")

        async def echo(ctx):
            await ctx.message.delete()
            embed = discord.Embed(
                title="Enter the keyword of the repository",
                description="this request will terminate in 60sec"
            )
            sent = await ctx.send(embed=embed)

            try:
                key_word = await client.wait_for(
                    "message",
                    timeout=60

                )
                if key_word:
                    await sent.delete()
                    await key_word.delete()
                    await ctx.send(key_word.content)
            except asyncio.TimeoutError:
                await sent.delete()
                await ctx.send("cancelling due to timeout", delete_after=10)

        key_word = await client.wait_for('message', timeout=15)
        api_url = f"https://api.github.com/search/repositories?q={key_word.content}&1"
        response = requests.get(api_url)
        data = response.json()
        for repo in data["items"]:
            await message.channel.send(repo["html_url"])


keep_alive()
client.run(os.getenv("TOKEN"))