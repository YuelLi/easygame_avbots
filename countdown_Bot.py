import discord
from discord.ext import tasks, commands
import asyncio

#bot = commands.Bot(command_prefix='!@')

# client token
token = 'NjYxNDI3NzQ3Njg3NzU5ODcy.Xg2bCQ.CLYlN2rpT364WzRkVbDPFD3jT60'

# count_down_audio_name
count_down_audio_file = 'count_down.wav'

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
tank_req_floor = 1
healer_req_floor = 1
player_req_floor = 4

# queue count down interval values
current_idle_times = 0
daemon_interval = 5
MIN_IDLE_TIMES = 6
MAX_IDLE_TIMES = 24  # 120s



class CountDown(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.idle_times = 1
        self.queue_channel = None
        self.voice_client = None
        self.playing = False

        self.bg_task = self.loop.create_task(self.queue_daemon())

    async def queue_daemon(self):
        await self.wait_until_ready()
        while not self.is_closed():
            if self.playing:
                if not self.voice_client.is_playing():
                    await self.voice_client.disconnect()
                    self.voice_client = None
                    self.idle_times = 1
                    self.playing = False
            else:
                print("wait, %s" % self.idle_times)
                if self.idle_times > MIN_IDLE_TIMES:
                    await self.check_avqueue_status()

                self.idle_times += 1

            await asyncio.sleep(daemon_interval)

    async def check_avqueue_status(self):
        if self.idle_times > MAX_IDLE_TIMES:
            await self.play_count_down()
            return

        # check group config.
        self.queue_channel = self.get_channel(queue_channel_id)
        members = self.queue_channel.members

        if len(members) < player_req_floor:
            return

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

        print ("T: %d, H: %d, Total: %d" % (tank_count, healer_count, len(members)))
        if tank_count >= tank_req_floor and healer_count >= healer_req_floor:
            await self.play_count_down()

    async def play_count_down(self):
        print("Player countdown")
        self.voice_client = await self.queue_channel.connect()
        await self.voice_client.move_to(self.queue_channel)

        audio_source = discord.FFmpegPCMAudio(count_down_audio_file)
        self.voice_client.play(audio_source, after=None)

        self.playing = True


client = CountDown()
client.run(token)
