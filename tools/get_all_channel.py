import discord
import json


token = "NjYxNDI2OTY5NzkwOTA2Mzkw.Xg_GZg.7rNhVbgO-EwMVhZjOXNB26z99ds"

client = discord.Client()

channel_list = []


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for channel in client.get_all_channels():
        print("%s: %s" % (channel.name, channel.id))
        c = {}
        c['id'] = channel.id
        c['name'] = channel.name
        c['guild'] = channel.guild.id
        c['category_id'] = channel.category_id
        c['type'] = channel.type
        channel_list.append(c)

    with open('channel.json', 'w') as gp:
        json.dump(channel_list, gp)

    client.close()


client.run(token)