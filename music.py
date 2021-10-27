from sys import executable
import discord
from discord.ext import commands
from discord.player import FFmpegPCMAudio
import youtube_dl
import asyncio


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Need to be in voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(60)
            while ctx.voice_client.is_playing():
                break
            else:
                await ctx.voice_client.disconnect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send("Need to be in voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        voice = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audiopath = info["formats"][0]["url"]
            voice.play(FFmpegPCMAudio(audiopath, **FFMPEG_OPTIONS))
        
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(60)
            while ctx.voice_client.is_playing():
                break
            else:
                await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resume")

    @commands.command()
    async def commands(self, ctx):
        await ctx.send("$join, $leave, $play {youtube link}, $pause, $resume")


def setup(bot):
    bot.add_cog(music(bot))
