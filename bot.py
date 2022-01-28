import discord
from discord.ext import commands
import logging
import random
import os
import shutil
import pathlib
import bitmath
import mysql.connector
import time
from google.cloud import vision
import io
import datetime
from pytube import YouTube
from PIL import Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./neonhaze-d8a2d3ce3817.json"

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
print('Enabled Discord Loggin...')

description = '''A weird bot with some odd functions, nothing to see here.'''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

workpath = pathlib.Path().resolve()
print('Working Dir : ' + str(workpath))

def log(input, user):
    f = open('log.txt', 'a')
    timenow = datetime.datetime.now()
    tnow = timenow.strftime("%H:%M:%S")
    if str(user) == '':
        log_string = str(tnow) + ' : ' + input + '\n'
        f.write(log_string)
    else:
        log_string = tnow + ' : ' + input + ' by User ID ' + user + '\n'
        f.write(log_string)
    f.close()


def mysql_connector(sql, values):
    db = mysql.connector.connect(
        host='localhost',
        user='botboi',
        password='Duckquack123!!',
        database='image',
        ssl_disabled=True,
        connect_timeout=5
    )
    if values != '':
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchall()
        db.commit()
        db.close()
        log('Database Entry committed.', '')
    else:
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        log('Database Entry committed.', '')

    return result

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for your files."))

@bot.event
async def on_message(message: discord.Message):
    log('Received message', str(message.author.id))

    if message.content.startswith('?jpg'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
            return
        elif message.content != '?jpg':
            path = '/var/www/neonhaze/html/img/'
            path2 = '/var/www/neonhaze/html/jpg/'
            imgid = str(message.content).split(' ')[1]
            user = str(message.author.id)
            values = (user, imgid)
            result = mysql_connector("SELECT * FROM images WHERE USERID = %s AND IMGID = %s", values)
            if str(result) != '[]':
                impath = path + imgid
                im = Image.open(impath)
                xs, ys = im.size
                old_size = xs, ys
                embed = discord.Embed(title='NeonHaze moar JPG', value='Add more JPG to your image.')
                embed.add_field(value='Select you Level of JPG', name='Worse to Worst', inline=False)
                embed.add_field(value='1️⃣', name='JPG it', inline=False)
                embed.add_field(value='2️⃣', name='JPGGG it', inline=False)
                embed.add_field(value='3️⃣', name='Nuke it', inline=False)
                thumb = 'https://neonhaze.wtf/img/' + str(imgid)
                embed.set_thumbnail(url=thumb)
                jpgembed = await message.channel.send(embed=embed)
                await jpgembed.add_reaction('1️⃣')
                await jpgembed.add_reaction('2️⃣')
                await jpgembed.add_reaction('3️⃣')
                reaction, user = await bot.wait_for('reaction_add')
                while user == bot.user:
                    reaction, user = await bot.wait_for('reaction_add')

                if str(reaction.emoji) == '1️⃣':
                    xs = xs / 2
                    ys = ys / 2
                    ns = int(xs), int(ys)

                if str(reaction.emoji) == '2️⃣':
                    xs = xs / 4
                    ys = ys / 4
                    ns = int(xs), int(ys)

                if str(reaction.emoji) == '3️⃣':
                    xs = xs / 8
                    ys = ys / 8
                    ns = int(xs), int(ys)
            else:
                embed = discord.Embed(title='NeonHaze moar JPG', value='Add more JPG to yourimage.')
                embed.add_field(value='Do you Own the Image ?', name='uhh Ohhh', inline=False)
                await message.channel.send(embed=embed)
                return

            im = im.resize(ns, resample=0)
            save = str(workpath) + '/tmp.jpg'
            im.save(save, quality=0)
            im = Image.open(save)
            imgid = imgid.split('.')[0]
            webid = 'j' + imgid + '.jpg'
            newid = path2 + webid
            im = im.resize(old_size, resample=0)
            im.save(newid, quality=0)
            os.remove(save)
            embed = discord.Embed(title='NeonHaze moar JPG', value='Add more JPG to yourimage.')
            embed.add_field(value='Image is ready', name='https://neonhaze.wtf/jpg/' + webid, inline=False)
            thumb = 'https://neonhaze.wtf/jpg/' + webid
            embed.set_image(url=thumb)
            await jpgembed.edit(embed=embed)
        else:
            embed = discord.Embed(title='NeonHaze moar JPG', value='Add more JPG to yourimage.')
            embed.add_field(value='No image Selected', name='uhh Ohhh', inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('https://www.youtube.com/watch?') or \
            message.content.startswith('https://youtu.be'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
             return
        else:
            print('YT request')
            log('Received YT DOWNLOAD', str(message.author.id))
            user_string = str(message.author.id)
            await message.delete()
            embed = discord.Embed(title=f'NeonHaze Rehost',
                                  description=f'Please make a selection', color=discord.Color.orange())
            embed.add_field(value='1️⃣', name='Download MP4', inline=False)
            embed.add_field(value='2️⃣', name='Download MP3', inline=False)
            embed.add_field(value='3️⃣', name='Add to Website', inline=False)
            procem = await message.channel.send(embed=embed)
            await procem.add_reaction('1️⃣')
            await procem.add_reaction('2️⃣')
            await procem.add_reaction('3️⃣')
            print(str(message.content))
            link = str(message.content)
            log(link, str(message.author.id))
            try:
                yt = YouTube(link)
            except:
                embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                embed.add_field(name='Something went wrong.', value='Please check your link ' + str(link), inline=False)
                await message.channel.send(embed=embed)
                return
            vidname1 = yt.title
            vidname2 = ''.join(char for char in vidname1 if char.isalnum())
            thumb = yt.thumbnail_url
            try:
                reaction, user = await bot.wait_for('reaction_add')
                while user == bot.user:
                    reaction, user = await bot.wait_for('reaction_add')
                if str(reaction.emoji) == '1️⃣':
                    embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                    embed.add_field(name='Processing Video', value='Please wait...', inline=False)
                    embed.set_thumbnail(url=str(thumb))
                    await procem.edit(embed=embed)
                    stream = yt.streams.filter(file_extension='mp4')
                    ytvid = stream.get_highest_resolution()
                    save_path = '/var/www/neonhaze/html/vid'
                    try:
                        ytvid.download(output_path=save_path, filename=vidname2 + '.mp4')
                        print('Downloading video')
                    except:
                        embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                        embed.add_field(name='Something went wrong Downloading the Video.', value='Oops', inline=False)
                        message.channel.send(embed=embed)
                        return
                    print('Sending Video Embed.')
                    embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                    embed.add_field(name='Video is ready @ ', value='https://neonhaze.wtf/vid/' + vidname2 + '.mp4',
                                 inline=False)
                    embed.set_thumbnail(url=str(thumb))
                    await procem.edit(embed=embed)
                if str(reaction.emoji) == '2️⃣':
                    embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                    embed.add_field(name='Processing Video', value='Please wait...', inline=False)
                    embed.set_thumbnail(url=str(thumb))
                    await procem.edit(embed=embed)
                    stream = yt.streams.filter(only_audio=True)
                    ytvid = stream.get_audio_only()
                    save_path = '/var/www/neonhaze/html/aud'
                    try:
                        ytvid.download(output_path=save_path, filename=vidname2 + '.mp3')
                        print('Downloading audio')
                        print('Sending Video Embed.')
                        embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                        embed.add_field(name='Video is ready @ ', value='https://neonhaze.wtf/aud/' + vidname2 + '.mp3',
                                        inline=False)
                        embed.set_thumbnail(url=str(thumb))
                        await procem.edit(embed=embed)
                    except:
                        embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                        embed.add_field(name='Something went wrong Downloading the Video.', value='Oops', inline=False)
                        await message.channel.send(embed=embed)
                        return
                if str(reaction.emoji) == '3️⃣':
                    embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                    embed.add_field(name='Processing Video', value='Please wait...', inline=False)
                    embed.set_thumbnail(url=str(thumb))
                    await procem.edit(embed=embed)
                    stream = yt.streams.filter(file_extension='mp4')
                    ytvid = stream.get_highest_resolution()
                    webpath = '/var/www/neonhaze/html/img'
                    nname = random.randrange(0, 9999999, 6)
                    try:
                        ytvid.download(output_path=webpath, filename=str(nname) + '.mp4')
                        print('Downloading video')
                    except:
                        embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                        embed.add_field(name='Something went wrong Downloading the Video.', value='Oops', inline=False)
                        await message.channel.send(embed=embed)
                        return
                    val = str(nname) + '.mp4'
                    mysql_connector('INSERT INTO images (USERID, IMGID) VALUES (\'' + str(user_string) + '\',\'' + val
                                    + '\')', '')
                    mysql_connector('INSERT INTO users (userid, uploads) VALUES ('
                                    + user_string + ', 1) ON DUPLICATE KEY UPDATE uploads = uploads + 1', '')
                    print('Mysql DOne....')
                    embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                    embed.add_field(name='Video is ready @ ', value='https://neonhaze.wtf/img/' + str(nname) + '.mp4',
                                    inline=False)
                    embed.add_field(name='Added to website.', value='You can now find your meme on the website.')
                    embed.add_field(name="Delete Image", value='Delete your Video with (?imdel ' + str(nname) + '.mp4)',
                                    inline=False)
                    embed.set_thumbnail(url=str(thumb))
                    await procem.edit(embed=embed)

            except Exception:
                embed = discord.Embed(title='NeonHaze Rehost', description='YouTube Downloader')
                embed.add_field(name='Something went wrong.', value='IDK WTF MAN', inline=False)
                await message.channel.send(embed=embed)
                return

    if message.content.startswith('?top'):
        await message.delete()
        embed = discord.Embed(title='NeonHaze Rehost', description='Top Uploader\'s')
        top_5 = mysql_connector('SELECT userid, uploads FROM users ORDER BY uploads DESC LIMIT 5', '')
        x = 0
        for users in top_5:
            querry = str(users)
            querry = querry.strip('(\'\')')
            userid, uploads = querry.split(',')
            userid = userid.strip('\'')
            log('?top request', str(userid))
            mention = '<@!' + userid + '>'
            embed.add_field(name='#' + str(x+1), value=str(mention) + 'Uploads ' + str(uploads), inline=False)
            x += 1
        await message.channel.send(embed=embed)

    if message.content.startswith('?help'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        log('?help', str(userid))
        if guild.get_member(int(userid)) is None:
            embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Help',
                                  color=discord.Color.blue())
            embed.add_field(name='?help', value='Shows the Bot Help', inline=False)
            embed.add_field(name='?size', value='Get the amount of images on the server as well as the size.',
                            inline=False)
            embed.add_field(name='?meme', value='Grabs a random meme from the server.', inline=False)
            embed.add_field(name='?top', value='Shows Top 5 for uploader\'s.', inline=False)
            embed.set_image(url='https://neonhaze.wtf/neonhaze.gif')
            embed.set_footer(text='Want to help expand the meme collection ? Message _ConFuzion#4978 on Discord.')
            await message.channel.send(embed=embed)

        else:
            await message.delete()
            embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Help',
                                  color=discord.Color.blue())
            embed.set_image(url='https://neonhaze.wtf/neonhaze.gif')
            embed.add_field(name='?help', value='Shows the Bot Help', inline=False)
            embed.add_field(name='?imdel', value='Lets you delete and image you uploaded.', inline=False)
            embed.add_field(name='?size', value='Get the amount of images on the server as well as the size.',
                            inline=False)
            embed.add_field(name='?port', value='Lets you transfer ownership of a Image, ?port for more info.',
                            inline=False)
            embed.add_field(name='?id', value='Returns User ID of sender.', inline=False)
            embed.add_field(name='?meme', value='Grabs a random meme from the server.', inline=False)
            embed.add_field(name='?top', value='Shows Top 5 for uploader\'s.', inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('?meme'):
        print('Meme Request')
        log('?meme', str(message.author.id))
        count = 1
        path2 = '/var/www/neonhaze/html/img/'
        memec = 0
        rmeme = ''
        for ele in os.scandir(path2):
            count += 1
        randommeme = random.randrange(1, count)
        for ele in os.scandir(path2):
            if memec == randommeme:
                rmeme = path2 + str(ele)
                break
            if 'mp4' in rmeme:
                print('Skipping Video...')
                memec -= 1
            else:
                memec += 1
        await message.delete()
        embed = discord.Embed(title=f'NeonHaze Rehost', description=f'More at https://neonhaze.wtf',
                              color=discord.Color.gold())
        crmeme = rmeme.replace('/var/www/neonhaze/html/img/<DirEntry \'', '')
        crmemee = crmeme.replace('\'>', '')
        emimg = 'https://neonhaze.wtf/img/' + str(crmemee)
        print(str(emimg))
        embed.set_image(url=str(emimg))
        embed.set_footer(text='Want to help expand the meme collection ? Message _ConFuzion#4978 on Discord.')
        await message.channel.send(embed=embed)

    if message.content.startswith('?size'):
        guild = bot.get_guild(873015473829195816)
        print('Size request')
        log('?size', str(message.author.id))
        size = 0
        sizei = 0
        sizev = 0
        image = 0
        video = 0
        total = 0
        path2 = '/var/www/neonhaze/html/img/'
        for ele in os.scandir(path2):
            if 'mp4' in str(ele):
                video += 1
                total += 1
                size += os.path.getsize(ele)
                sizev += os.path.getsize(ele)
            else:
                size += os.path.getsize(ele)
                sizei += os.path.getsize(ele)
                image += 1
                total += 1

        human_prefix = bitmath.Byte(bytes=size).best_prefix()
        human_prefix = human_prefix.format("{value:.2f} {unit}")
        video_size = bitmath.Byte(bytes=sizev).best_prefix()
        video_size = video_size.format("{value:.2f} {unit}")
        image_size = bitmath.Byte(bytes=sizei).best_prefix()
        image_size = image_size.format("{value:.2f} {unit}")
        await message.delete()
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
            log('Off-server Request ?meme ', str(message.author.id))
            embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Files on the Server',
                                  color=discord.Color.dark_gold())
            embed.add_field(name='Total number of files', value=str(total), inline=False)
            embed.add_field(name='Total Size of Files', value=human_prefix, inline=False)
            await message.channel.send(embed=embed)
        else:
            log('Main Server ?size request', str(message.author.id))
            embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Files on the Server',
                                  color=discord.Color.dark_gold())
            embed.add_field(name='Total number of Images', value=str(image), inline=False)
            embed.add_field(name='Size of Image Files', value=image_size, inline=False)
            embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value=f'.', inline=False)
            embed.add_field(name='Total number of Videos', value=str(video), inline=False)
            embed.add_field(name='Size of Video Files', value=video_size, inline=False)
            embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value=f'.', inline=False)
            embed.add_field(name='Total Size of Files', value=human_prefix, inline=False)
            embed.add_field(name='Total number of files', value=str(total), inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('?imdel'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        log('?imdel', str(userid))
        if guild.get_member(int(userid)) is None:
            log('Off-server Rquest ?imdel ', str(userid))
            return
        else:
            await message.delete()
            imgdel = str(message.content)
            delid = imgdel.replace('?imdel ', '')
            user = str(message.author.id)
            log('File Deletion : File=' + str(delid), user)
            print('Deletion request from user : ' + str(message.author.id))
            print('Image DELETION ID :' + str(delid))
            values = (user, delid)
            result = mysql_connector("SELECT * FROM images WHERE USERID = %s AND IMGID = %s", values)
            if str(result) != '[]':
                path2 = '/var/www/neonhaze/html/img/' + str(delid)
                if os.path.exists(path2):
                    os.remove(path2)
                    mysql_connector("DELETE FROM images WHERE USERID = %s AND IMGID = %s", values)
                    mysql_connector('INSERT INTO users (userid, uploads) VALUES ('
                                    + user + ', 1) ON DUPLICATE KEY UPDATE uploads = uploads - 1', '')
                    log('File Deletion : Success (' + str(delid) + ')', user)
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'File Deleted.',
                                          color=discord.Color.green())
                    await message.channel.send(embed=embed)
                else:
                    values = (user, delid)
                    mysql_connector("DELETE FROM images WHERE USERID = %s AND IMGID = %s", values)
                    await message.delete()
                    log('File Deletion : Found File thats not on Server but in Mysql. (' + str(delid) + ')', user)
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Something went wrong.',
                                          color=discord.Color.blurple())
                    await message.channel.send(embed=embed)
                    print("Removed old entry that shouldn't have been in Database")
            else:
                embed = discord.Embed(title=f'NeonHaze Rehost',
                                      description=f'Unable to delete file, is filename correct, are you the owner ?',
                                      color=discord.Color.red())
                embed.add_field(title=f'Image ID', value=str(delid))
                await message.channel.send(embed=embed)
                log('File Deletion : Error Owner or File name wrong.', user)
                print('Not Owner/Wrong image name.')

    for attachment in message.attachments:
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
            return
        else:
            image_types = ['png', 'jpeg', 'gif', 'jpg', 'mp4', 'webm']
            pic = ['png', 'jpeg', 'gif', 'jpg']
            log('Image upload', str(userid))
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                ext = os.path.splitext(attachment.filename)[1]
                nname = random.randrange(0, 9999999, 6)
                name = (str(nname) + ext)
                await attachment.save(str(path) + '/tmp/' + str(name))
                log('Saved image to tmp folder :' + name, '')
                await message.delete()
                embed = discord.Embed(title=f'NeonHaze Rehost',
                                      description=f'Processing Image', color=discord.Color.orange())
                procem = await message.channel.send(embed=embed)
                proct = time.time()
                # Google safe search (Gore/Porn)
                ext = str(ext).replace('.', '')
                if ext not in pic:
                    vid = True
                    gore = 'no'
                    nsfw = 'no'
                elif ext in pic:
                    vid = False
                    print('safe search')
                    client = vision.ImageAnnotatorClient()
                    with io.open(str(path) + '/tmp/' + str(name), 'rb') as image_file:
                        content = image_file.read()

                    image = vision.Image(content=content)

                    response = client.safe_search_detection(image=image)
                    safe = response.safe_search_annotation
                    # UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY
                    likelihood_name = ('no', 'no', 'no', 'no', 'yes', 'yes')
                    likelihood_name_real = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
                    nsfw = likelihood_name[safe.adult]
                    gore = likelihood_name[safe.violence]
                    med = likelihood_name[safe.medical]
                    log('SafeSearch Results = NSFW : ' + str(likelihood_name_real[safe.adult]) + ' Violence : ' +
                        str(likelihood_name_real[safe.violence]) + 'Medical : ' +
                        str(likelihood_name_real[safe.medical]), str(userid))
                    if med == 'yes':
                        gore == 'yes'


                if nsfw == 'no' and gore == 'no' or vid != False:
                    print('Image intake ---')
                    start = time.time()
                    val = str(userid), str(name)
                    user_string = str(userid)
                    mysql_connector('INSERT INTO images (USERID, IMGID) VALUES (%s, %s)', val)
                    mysql_connector('INSERT INTO users (userid, uploads) VALUES ('
                                    + user_string + ', 1) ON DUPLICATE KEY UPDATE uploads = uploads + 1', '')
                    end = time.time()
                    timer = end - start
                    print('Database Commit time : ' + str(timer) + 'ms')
                    print(str(userid) + ' Saved Image')
                    movepath = str(path) + '/tmp/' + str(name)
                    nmove = '/var/www/neonhaze/html/img/' + str(name)
                    shutil.move(movepath, nmove)
                    print('Moved Image to IMG folder')
                    log('Image Saved : ' + name, str(userid))
                    procte = time.time()
                    proctime = procte - proct
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Rehosted @ https://neonhaze.wtf/img/'
                                                                                + str(name), color=discord.Color.blue())
                    thumb = 'https://neonhaze.wtf/img/' + str(name)
                    embed.set_thumbnail(url=thumb)
                    mention = '<@!' + str(message.author.id) + '>'
                    embed.add_field(name="Image is ready ", value=str(mention), inline=False)
                    embed.add_field(name="Delete Image", value='Delete your image with (?imdel ' + str(name) + ')',
                                    inline=False)
                    embed.add_field(name='Processing Time', value=str(round(proctime, 4)) + 'seconds', inline=False)

                    if vid == False:
                        embed.set_footer(text='Is image spoof ? ' + str(likelihood_name_real[safe.spoof]))

                    await procem.edit(embed=embed)
                    print('Sent Hosted image embed')
                else:
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Forbidden', color=discord.Color.red())
                    embed.add_field(name='Forbidden content Found.', value='NSFW/GORE is not allowed.', inline=False)
                    embed.add_field(name='Is image NSFW', value=str(likelihood_name[safe.adult]), inline=False)
                    embed.add_field(name='Is image Gore', value=str(likelihood_name[safe.violence]), inline=False)
                    await message.channel.send(embed=embed)
                    os.remove(str(path) + '/tmp/' + str(name))
                    log('Denied and deleted image ' + name, str(userid))

    if message.content.startswith('?port'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
            return
        else:
            if str(message.content) == '?port':
                await message.delete()
                log('Ownership transfer request', str(userid))
                embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Owner Transfer',
                                      color=discord.Color.greyple())
                embed.add_field(name="Transfer images like so :", value='?port<userid>:<img name>', inline=False)
                embed.add_field(name="<user id>", value='<userid> is your owm user id (?id to get own id)',
                                inline=False)
                embed.add_field(name="<image id>", value='<img name> is the file name like in the ?imdel', inline=False)
                await message.channel.send(embed=embed)
                print('Sent ?port help')
            else:
                print('Transfer request incoming...')
                uinput = str(message.content)
                cinput = uinput.replace('?port', '')
                ccinput = cinput.strip()
                userold = message.author.id
                userid, imgid = ccinput.split(':')
                if len(userid) == 18:
                    if str(imgid.strip()) == '':
                        await message.delete()
                        embed = discord.Embed(title=f'NeonHaze Rehost', description=f'', color=discord.Color.dark_red())
                        embed.add_field(name="Check Image ID", value='No image ID given', inline=False)
                        await message.channel.send(embed=embed)
                        log('OTR No image ID given.', str(userid))
                else:
                    await message.delete()
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'', color=discord.Color.dark_red())
                    embed.add_field(name="Check User ID", value='User ID incorrect length', inline=False)
                    embed.add_field(name="User ID", value=str(userid), inline=False)
                    await message.channel.send(embed=embed)
                    print('UserID length ERROR')
                    return
                if guild.get_member(int(userid)) is None:
                    await message.delete()
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'', color=discord.Color.dark_red())
                    embed.add_field(name="Check User ID", value='User not in Server', inline=False)
                    embed.add_field(name="User ID", value=str(userid), inline=False)
                    await message.channel.send(embed=embed)
                    print('None Member ERROR')
                    log('OTR None member transfer ', str(userid))
                    return

                values = (userold, imgid)
                result = mysql_connector('SELECT * FROM images WHERE USERID = %s AND IMGID = %s', values)
                if str(result) != '[]':
                    val = userid, imgid
                    mysql_connector('UPDATE images SET USERID= %s WHERE IMGID=%s;', val)
                    await message.delete()
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Image Transferred',
                                          color=discord.Color.greyple())
                    thumb = 'https://neonhaze.wtf/img/' + str(imgid)
                    embed.set_thumbnail(url=thumb)
                    mention = '<@!' + str(userid) + '>'
                    embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value='New Owner : ' + mention, inline=False)
                    mention = '<@!' + str(userold) + '>'
                    embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value='Old Owner : ' + mention, inline=False)
                    embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value=str(thumb), inline=False)
                    embed.add_field(name=':x::x::x::x::x::x::x::x::x::x:', value='Delete with \"?imdel ' + str(imgid) +
                                                                                 '\"', inline=False)
                    await message.channel.send(embed=embed)
                    log('OTR success new owner : ' + userid, str(userid))
                    print('Transfer success !')
                else:
                    embed = discord.Embed(title=f'NeonHaze Rehost', description=f'Something went wrong.',
                                          color=discord.Color.blurple())
                    await message.channel.send(embed=embed)
                    print('Unable to find User/IMG in Database')
                    log('OTR File not found with userid ', str(userid))

    if message.content.startswith('?id'):
        guild = bot.get_guild(873015473829195816)
        userid = message.author.id
        if guild.get_member(int(userid)) is None:
            return
        else:
            await message.delete()
            embed = discord.Embed(title=f'NeonHaze Rehost', description=f'', color=discord.Color.dark_gold())
            embed.add_field(name="User ID", value=str(message.author.id), inline=False)
            await message.channel.send(embed=embed)
            log('?id ', str(message.author.id))
            print('?id REQUEST')

bot.run('ODczNzY1MTExNjE2MTEwNjQy.YQ9LLA._vfqTMwcvibSmWA0X8Cy3zsXuJ4')
