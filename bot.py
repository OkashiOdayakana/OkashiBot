
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='%')
import requests
import json
import time
from bash import bash
import inspect
import asyncio
import aiohttp
import async_timeout
import os
ownerid = 120215873247117312

with open('config.json') as json_data:
    obj = json.load(json_data)
    token = obj["api_key"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



async def fetch(session, url):
    headers = {'content-type': 'application/json'}
    with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            return await response.text()


@bot.command(pass_context=True, hidden=True)
async def shell(ctx, *, code: str):
    if ctx.message.author.id != ownerid:
        await ctx.send("You cant run this mane lol", delete_after=5)
        return 1
    try:
        result = bash(code)
        await ctx.send("```bash\n{}```".format(result))
    except Exception as e:
        await ctx.send(e)


@bot.command(pass_context=True, hidden=True)
async def debug(ctx, *, code: str):
    if ctx.message.author.id != ownerid:
        await ctx.send("Pls dont try that", delete_after=5)
        return 1
    try:
        result = eval(code)
        if inspect.isawaitable(result):
            result = await result
        await ctx.send("```py\n{}```".format(result))
    except Exception as e:
        await ctx.send(e)


@bot.command(pass_context=True)
async def srvrs(ctx):
    """Lists amount of servers bot is in"""
    bot.app = await bot.application_info()
    owner = bot.app.owner
    guilds = 'guilds: ' + str(len(bot.guilds))
    users = 'users: ' + str(len(list(bot.get_all_members())))
    uniques = 'unique users: ' + \
        str(len(discord.utils._unique(bot.get_all_members())))
    await ctx.send(guilds)
    await ctx.send(users)
    await ctx.send(uniques)


@bot.command(pass_context=True)
async def gelbooru(ctx, tag,  page='1'):
    """Searchs gelbooru. Usage: gelbooru [tag]"""
    if not ctx.channel.is_nsfw():
        await ctx.send("Please run this command on an nsfw channel.", delete_after=5)
        return 1
    if not page or page == '' or page == ' ' or page == None:
        page = '1'
    print("https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={}&limit=1&json=1&pid={}".format(tag, page))
    async with aiohttp.ClientSession() as session:
        invoker = ctx.message.author
        try:
            post = await fetch(session, "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={}&limit=1&json=1&pid={}".format(tag, page))
        except Exception as e:
            await ctx.send("```{}```".format(e))
        try:
            obj = json.loads(post)
            url = obj[0]["file_url"]
            rating = obj[0]["rating"]
            tags_raw = obj[0]["tags"]
            tags = tags_raw[:140] + (tags_raw[140:] and '..')
        except Exception as e:
            await ctx.send("Tag not found.", delete_after=5)
            return 1
        embed = discord.Embed(
            title='Gelbooru', url='https://gelbooru.com', color=0x00fff)
        embed.add_field(name='Rating: ' + rating,
                        value='Tags: ' + tags, inline=True)
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        if int(page) > 1:
            await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await msg.add_reaction('\U0001F1FD')

        def check(reaction, user):
            return user == invoker and reaction.message.id == msg.id and (str(reaction.emoji) == '\U00002B05' or str(reaction.emoji) == '\U000027A1' or str(reaction.emoji) == '\U0001F1FD')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            return 1
        else:
            if str(reaction.emoji) == '\U00002B05':
                page = int(page)
                page -= 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(gelbooru, tag, page)
            elif str(reaction.emoji) == '\U000027A1':
                page = int(page)
                page += 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(gelbooru, tag, page)
            elif str(reaction.emoji) == '\U0001F1FD':
                await msg.delete()
                return


@bot.command(pass_context=True)
async def lolibooru(ctx, tag, page='1'):
    """Searches lolibooru. Usage: lolibooru [tags]"""
    if not ctx.channel.is_nsfw():
        await ctx.send("Please run this command on an nsfw channel.", delete_after=5)
        return 1
    if not page:
        page = 1
    async with aiohttp.ClientSession() as session:
        invoker = ctx.message.author
        post = await fetch(session, "https://lolibooru.moe/post/index.json?limit=1&tags={}&page={}".format(tag, page))
        obj = json.loads(post)
        try:
            url_raw = obj[0]["jpeg_url"]
            url = url_raw.replace(" ", "%20")
            rating = obj[0]["rating"]
            tags_raw = obj[0]["tags"]
            tags = tags_raw[:140] + (tags_raw[140:] and '..')
        except Exception as e:
            await ctx.send("Tag not found.", delete_after=5)
            return 1
        embed = discord.Embed(
            title="Lolibooru", url='https://lolibooru.moe', color=0x00fff)
        embed.add_field(name='Rating: ' + rating,
                        value='Tags: ' + tags, inline=True)
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        if int(page) > 1:
            await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await msg.add_reaction('\U0001F1FD')

        def check(reaction, user):
            return user == invoker and reaction.message.id == msg.id and (str(reaction.emoji) == '\U00002B05' or str(reaction.emoji) == '\U000027A1' or str(reaction.emoji) == '\U0001F1FD')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            return 1
        else:
            if str(reaction.emoji) == '\U00002B05':
                page = int(page)
                page -= 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(lolibooru, tag, page)
            elif str(reaction.emoji) == '\U000027A1':
                page = int(page)
                page += 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(lolibooru, tag, page)
            elif str(reaction.emoji) == '\U0001F1FD':
                await msg.delete()
                return


@bot.command(pass_context=True)
async def danbooru(ctx, tag, page='1'):
    """Searches danbooru. Usage: danbooru [tags]"""
    if not ctx.channel.is_nsfw():
        await ctx.send("Please run this command on an nsfw channel.", delete_after=5)
        return 1
    if not page:
        page = 1
    async with aiohttp.ClientSession() as session:
        try:
            invoker = ctx.message.author
            post = await fetch(session, "https://danbooru.donmai.us/posts.json?limit=1&json=1&tags={}&page={}".format(tag, page))
        except Exception as e:
            await ctx.send("```{}```".format(e))
        obj = json.loads(post)
        try:
            rating = obj[0]["rating"]
            tags_raw = obj[0]["tag_string"]
            tags = tags_raw[:500] + (tags_raw[500:] and '..')
        except Exception as e:
            await ctx.send("Tag not found", delete_after=5)
            return 1
        try:
            path = obj[0]["large_file_url"]
            url = "https://danbooru.donmai.us{}".format(path)
        except Exception as e:
            await ctx.send("That tag requires a Gold Account or smth. Srry mane", delete_after=5)
            return 1
        embed = discord.Embed(
            title="Danbooru", url='https://danbooru.donmai.us', color=0x00fff)
        embed.add_field(name='Rating: ' + rating,
                        value='Tags: ' + tags, inline=True)
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        
        if int(page) > 1:
            await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await msg.add_reaction('\U0001F1FD')

        def check(reaction, user):
            return user == invoker and reaction.message.id == msg.id and (str(reaction.emoji) == '\U00002B05' or str(reaction.emoji) == '\U000027A1' or str(reaction.emoji) == '\U0001F1FD')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            return 1
        else:
            if str(reaction.emoji) == '\U00002B05':
                page = int(page)
                page -= 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(danbooru, tag, page)
            elif str(reaction.emoji) == '\U000027A1':
                page = int(page)
                page += 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(danbooru, tag, page)
            elif str(reaction.emoji) == '\U0001F1FD':
                await msg.delete()
                return


@bot.command(pass_context=True)
async def safebooru(ctx, tag, page='1'):
    """Searches safebooru. Usage: safebooru [tags]"""
    async with aiohttp.ClientSession() as session:
        invoker = ctx.message.author
        post = await fetch(session, "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1&tags={}&pid={}&json=1".format(tag, page))
        obj = json.loads(post)
        directory = obj[0]['directory']
        file_name = obj[0]['image']
        url = 'https://safebooru.org/images/{}/{}'.format(directory, file_name)
        tags_raw = obj[0]['tags']
        rating = obj[0]['rating']
        tags = tags_raw[:200] + (tags_raw[200:] and '..')
        embed = discord.Embed(
            title="Safebooru", url='https://safebooru.org', color=0x00fff)
        embed.add_field(name='Rating: ' + rating,
                        value='Tags: ' + tags, inline=True)
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        if int(page) > 1:
            await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await msg.add_reaction('\U0001F1FD')

        def check(reaction, user):
            return user == invoker and reaction.message.id == msg.id and (str(reaction.emoji) == '\U00002B05' or str(reaction.emoji) == '\U000027A1' or str(reaction.emoji) == '\U0001F1FD')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            return 1
        else:
            if str(reaction.emoji) == '\U00002B05':
                page = int(page)
                page -= 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(safebooru, tag, page)
            elif str(reaction.emoji) == '\U000027A1':
                page = int(page)
                page += 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(safebooru, tag, page)
            elif str(reaction.emoji) == '\U0001F1FD':
                await msg.delete()
                return


@bot.command(pass_context=True)
async def konachan(ctx, tag, page='1'):
    """Searches konachan. Usage: konachan [tags]"""
    async with aiohttp.ClientSession() as session:
        invoker = ctx.message.author
        post = await fetch(session, "https://konachan.com/post.json?limit=1&tags={}&page={}".format(tag, page))
        obj = json.loads(post)
        url_raw = obj[0]['jpeg_url']
        url = 'https:{}'.format(url_raw)
        tags_raw = obj[0]["tags"]
        tags = tags_raw[:200] + (tags_raw[200:] and '..')
        rating = obj[0]['rating']
        embed = discord.Embed(
            title="Konachan", url='https://konachan.com', color=0x00fff)
        embed.add_field(name='Rating: ' + rating,
                        value='Tags: ' + tags, inline=True)
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        if int(page) > 1:
            await msg.add_reaction('\U00002B05')
        await msg.add_reaction('\U000027A1')
        await msg.add_reaction('\U0001F1FD')

        def check(reaction, user):
            return user == invoker and reaction.message.id == msg.id and (str(reaction.emoji) == '\U00002B05' or str(reaction.emoji) == '\U000027A1' or str(reaction.emoji) == '\U0001F1FD')
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            return 1
        else:
            if str(reaction.emoji) == '\U00002B05':
                page = int(page)
                page -= 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(konachan, tag, page)
            elif str(reaction.emoji) == '\U000027A1':
                page = int(page)
                page += 1
                page = str(page)
                await msg.delete()
                await ctx.invoke(konachan, tag, page)
            elif str(reaction.emoji) == '\U0001F1FD':
                await msg.delete()
                return


@bot.command(pass_context=True, hidden=True)
async def game(ctx, *, option):
    game = discord.Game(name=option)
    await bot.change_presence(game=game)


@bot.command(pass_context=True)
async def say(ctx, *, phrase):
    await ctx.send(phrase)


@bot.command(pass_context=True)
async def purgeme(ctx, limit):
    def is_me(m):
        return m.author == bot.user
    deleted = await ctx.channel.purge(limit=int(limit), check=is_me)
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))


@bot.command(pass_context=True)
async def quran(ctx):
    """Just like random Quran verses"""
    async with aiohttp.ClientSession() as session:
        post = await fetch(session, 'https://quranapi.azurewebsites.net/api/verse?lang=en')
        obj = json.loads(post)
        chapter = obj['ChapterName']
        text = obj['Text']
        embed = discord.Embed(title="Random Quran verse", color=0x981aff)
        embed.add_field(name="Chapter name: " + chapter, value=text)
        await ctx.send(embed=embed)
bot.run(token)
