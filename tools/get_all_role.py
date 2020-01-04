import discord
import json


token = "NjYxNDI2OTY5NzkwOTA2Mzkw.Xg_GZg.7rNhVbgO-EwMVhZjOXNB26z99ds"

client = discord.Client()

role_list = []


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    t = client.guilds[0]

    for role in t.roles:
        print("%s: %s" % (role.name, role.id))
        r = {}
        r['id'] = role.id
        r['name'] = role.name
        # r['guild'] = channel.guild.id
        # r['category_id'] = channel.category_id
        # r['type'] = channel.type
        role_list.append(r)

    with open('role.json', 'w') as gp:
        json.dump(role_list, gp)

    await client.close()


client.run(token)