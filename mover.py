import re
import discord

from discord.ext import commands

av_re = re.compile("奥山-(?P<av_id>\d{3})")

token = "NjYxNDI2OTY5NzkwOTA2Mzkw.Xg_GZg.7rNhVbgO-EwMVhZjOXNB26z99ds"
bot = commands.Bot(command_prefix='!')
channels_dict = {}
queue_channel = None
jump_channel_id = 663470242269495326


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


    for channel in bot.get_all_channels():
        channel_name = channel.name

        if channel.name == '排队大厅':
            global queue_channel
            queue_channel = channel
            print("Add Channel: 排队大厅")

        else:
            match_av = av_re.match(channel.name)
            if match_av:
                channel_id = int(match_av.group('av_id'))
                channels_dict[channel_id] = channel
                print("Add Channel: %s" % channel_id)


@bot.command()
async def av(ctx, number: int):
    # print(ctx.channel)
    if ctx.channel.id == jump_channel_id:
        user_voice = ctx.author.voice
        target_channel = channels_dict.get(number, None)
        # print(ctx, number, target_channel)
        if target_channel and user_voice is not None:
            await ctx.author.move_to(target_channel)

    await ctx.message.delete()


@bot.command()
async def q(ctx):
    if ctx.channel.id == jump_channel_id and ctx.author.voice is not None:
        await ctx.author.move_to(queue_channel)
    await ctx.message.delete()


bot.run(token)
