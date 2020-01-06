import discord
from discord.ext import tasks, commands
import asyncio

bot = commands.Bot(command_prefix='!@')

# client token
token = 'NjYxNDI3NzQ3Njg3NzU5ODcy.Xg2bCQ.CLYlN2rpT364WzRkVbDPFD3jT60'

# count_down_audio_name
count_down_audio_file = '01.wav'

# guild 北美统战 id : 654524404318994476

# 排队大厅 channel id : 661422450948440124
queue_channel_id = 661422450948440124

# tank role id : 661406475444289538
tank_role_id = 661406475444289538
# off tank role id : 662124111811706904
offtank_role_id = 662124111811706904
# healer role id : 661406525566353475
healer_role_id = 661406525566353475
# dps role id : 661406567131775046
dps_role_id = 661406567131775046

# tank count : 4
# healer count : 6
# overall count : 40
tank_req_floor = 4
healer_req_floor = 6
player_req_floor = 26

# queue count down interval values
current_idle_times = 0
daemon_interval = 5
min_idle_times = 2
max_idle_times = 2 # 180s
video_length = 25

audio_source = discord.FFmpegPCMAudio(count_down_audio_file)

async def queue_daemon():
    global current_idle_times
    while not bot.is_closed():
        if current_idle_times > max_idle_times or await check_players_role():
            current_idle_times = 0
            await play_count_down()
        else:
            current_idle_times += 1
            print('more waiting', current_idle_times)
        await asyncio.sleep(daemon_interval)


async def check_players_role():
    await bot.wait_until_ready()
    queue_channel = bot.get_channel(queue_channel_id)
    members = queue_channel.members
    if len(members) > player_req_floor:
        tank_count = 0
        healer_count = 0
        for member in members:
            for role in member.roles:
                if role.id == tank_role_id:
                    tank_count += 1
                    break
                elif role.id == offtank_role_id:
                    tank_count += 1
                    break
                elif role.id == healer_role_id:
                    healer_count += 1
                    break

        if tank_count >= tank_req_floor and healer_count >= healer_req_floor:
            print('players role composition satisfied')
            return True
    print('players role composition not meet')
    return False


async def play_count_down():
    print('playing count down audio')
    queue_channel = bot.get_channel(queue_channel_id)

    voice_channel = await queue_channel.connect()
    

    voice_channel.play(audio_source, after=None)
    await asyncio.sleep(video_length)
    await voice_channel.disconnect()

bot.loop.create_task(queue_daemon())
bot.run(token)
