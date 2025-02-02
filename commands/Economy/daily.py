'''Claim your daily lacans'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, os, json, time
import discord
from mongoclient import DBClient
from discord.utils import get

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from discord.utils import get
from packages.nitrotype import Racer
import discord, random
import os
from cooldowns.withdraw import rateLimit, cooldown_add
import random
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def daily(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        #data = json.loads(requests.get('https://pointsdb.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)['data']
        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        channels = self.client.get_all_channels()
        channel = get(channels, id=803879362226946088)
        green =0x40AC7B
        red = 0xE84444
        orange = 0xF09F19


        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in data:
            user = d
            break
        embed = Embed('<a:success:800340618579935233>  Success!', 'You\'ve collected your daily **5** '+random_lacan+' succesfully!')
        try:
            old = user.copy()
            if ((round(time.time())-user['laststamp'] >= 75600)):
                user['points'] += 5
                user['laststamp'] = round(time.time())
                await dbclient.update_array(collection, old, user)
                #await embed.send(ctx)

                #Embed for lacan Log
                #embed1 = discord.Embed(title=f'{random_lacan}  Lacan Log', description=str(ctx.author), color= green)
                #embed1.add_field(name='__Won__', value=f'5')
                #embed1.add_field(name='__Command__', value='`n.daily`')
                #embed1.add_field(name='__Type__', value='*Claimed*')
                #embed1.add_field(name='__Total__', value=f'{total_points}')
                #embed1.add_field(name='__User ID__', value=f'`{ctx.author.id}`')
                #await channel.send(embed=embed1)
            else:
                import datetime
                timeleft = str(datetime.timedelta(seconds=75600-(round(time.time())-user['laststamp'])))
                embed = Embed('<a:error:800338727645216779>  Error!', 'You\'ve already collected your daily '+random_lacan+' today! Your next claim is available in **'+timeleft+'**.')

                #embed1 = embed=Embed(title='Lacan Log', description=f'{str(ctx.author)}', color=0xFF6347)
                #embed1.add_field(name=''+random_lacan+' Earned', value='5')
                #embed1.add_field(name='User ID', value=f'`{ctx.author.id}`')
                #await channel.send(embed=embed1)
                return await embed.send(ctx)
        except KeyError:
            if user['userid'] == str(ctx.author.id):
                user['points'] += 5
                user['laststamp'] = round(time.time())
                await dbclient.update_array(collection, old, user)
                embed = Embed('<a:success:800340618579935233>  Success!', 'You\'ve collected your daily succesfully!')
                #Embed for lacan Log
                #embed1 = discord.Embed(title=f'{random_lacan}  Lacan Log', description=str(ctx.author), color= green)
                #embed1.add_field(name='__Won__', value=f'5')
                #embed1.add_field(name='__Command__', value='`n.daily`')
                #embed1.add_field(name='__Type__', value='*Claimed*')
                #embed1.add_field(name='__Total__', value=f'{total_points}')
                #embed1.add_field(name='__User ID__', value=f'`{ctx.author.id}`')
                #await channel.send(embed=embed1)
            else:
                await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': 5, 'laststamp': round(time.time())})
        except UnboundLocalError:
          await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': 5, 'laststamp': round(time.time())})
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))