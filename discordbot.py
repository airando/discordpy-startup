import discord
import datetime
import asyncio
import random
import json
import urllib.request
import requests
import urllib.parse
import re
import os
import traceback

from googletrans import Translator
from discord.ext import commands,tasks
from discord import Webhook,RequestsWebhookAdapter

bot = commands.Bot(command_prefix="k!",help_command=commands.HelpCommand(command_attrs={'hidden': True}))
client = discord.Client()

gribto = {
    "おはよう":random.choice(('おはようございます','んにゃー')),
    "こい":random.choice(('come!come!','ん？恋ですか♡')),
    "きて": random.choice(('come!come!', 'いえあ')),
    "かった": random.choice(('良かったですね', '(過去形)')),
    "ました": random.choice(('お、おう…。', 'なるほどね')),
    "こんにちは": random.choice(('にゃはー', 'こんにちはー')),
    "おやすみ": random.choice(('おやすみなさい', 'ξ ´っω-` Ҙ..zzZ♥')),
    "ねろ": random.choice(('ねた', 'だが断る！')),
    "ましょう。": random.choice(('おう！', 'いえっさー')),
}
citycodes = {
    "北海道": '016010',
    "青森県": '020010',
    "岩手県": '030010',
    "宮城県": '040010',
    "秋田県": '050010',
    "山形県": '060010',
    "福島県": '070010',
    "東京都": '130010',
    "神奈川県": '140010',
    "埼玉県": '110010',
    "千葉県": '120010',
    "茨城県": '080010',
    "栃木県": '090010',
    "群馬県": '100010',
    "山梨県": '190010',
    "新潟県": '150010',
    "長野県": '200010',
    "富山県": '160010',
    "石川県": '170010',
    "福井県": '180010',
    "愛知県": '230010',
    "岐阜県": '200010',
    "静岡県": '220010',
    "三重県": '240010',
    "大阪府": '270000',
    "兵庫県": '280010',
    "京都府": '260010',
    "滋賀県": '250010',
    "奈良県": '190010',
    "和歌山県": '300010',
    "鳥取県": '310010',
    "島根県": '320010',
    "岡山県": '330010',
    "広島県": '340010',
    "山口県": '350010',
    "徳島県": '360010',
    "香川県": '370000',
    "愛媛県": '380010',
    "高知県": '390010',
    "福岡県": '400010',
    "大分県": '440010',
    "長崎県": '420010',
    "佐賀県": '410010',
    "熊本県": '430010',
    "宮崎県": '450010',
    "鹿児島県": '460010',
    "沖縄県": '471010',
    "北海": '016010',
    "青森": '020010',
    "岩手": '030010',
    "宮城": '040010',
    "秋田": '050010',
    "山形": '060010',
    "福島": '070010',
    "東京": '130010',
    "神奈川": '140010',
    "埼玉": '110010',
    "千葉": '120010',
    "茨城": '080010',
    "栃木": '090010',
    "群馬": '100010',
    "山梨": '190010',
    "新潟": '150010',
    "長野": '200010',
    "富山": '160010',
    "石川": '170010',
    "福井": '180010',
    "愛知": '230010',
    "岐阜": '200010',
    "静岡": '220010',
    "三重": '240010',
    "大阪": '270000',
    "兵庫": '280010',
    "京都": '260010',
    "滋賀": '250010',
    "奈良": '190010',
    "和歌山": '300010',
    "鳥取": '310010',
    "島根": '320010',
    "岡山": '330010',
    "広島": '340010',
    "山口": '350010',
    "徳島": '360010',
    "香川": '370000',
    "愛媛": '380010',
    "高知": '390010',
    "福岡": '400010',
    "大分": '440010',
    "長崎": '420010',
    "佐賀": '410010',
    "熊本": '430010',
    "宮崎": '450010',
    "鹿児島": '460010',
    "沖縄": '471010',
}

members = {
    "兄じゃぁぁぁ": '338151444731658240/634667072105873436/image0.jpg',
    "_toni": '622705703454244885/636051629170360322/icon3.png',
    "krty": '622705703454244885/635404047028846593/kkrrttyy.png',}

TOKEN = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    activity = discord.Activity(name='k!help', type=discord.ActivityType.listening, details="みんなこのBOTを使おう^^")
    await bot.change_presence(activity=activity)
    channel = bot.get_channel(632191021526155275)
    embed = discord.Embed(title="BOTを起動したよ")
    await channel.send(embed=embed)
    print(f'BOTを起動したよ！\n導入サーバー数は{len(bot.guilds)}です。')
    while True:
        for guild in bot.guilds:
            for channel in guild.voice_channels:
                if "役職:" in channel.name:
                    await channel.edit(name=f"役職:{len(guild.roles)}")
                    await asyncio.sleep(60)

@bot.event
async def on_member_ban(guild, user):
    g = bot.get_guild(622705702925893663)
    login = next(c for c in g.emojis if c.name == 'loading')
    channel = next(c for c in guild.channels if c.name == '運営ルーム')
    await channel.send(f"{user}がBANされました。")
    embed = discord.Embed(title="メッセージ削除",description=f"{login} {user}のメッセージを削除中です",color=0xe74c3c)
    m = await channel.send(embed=embed)
    for c in guild.text_channels:
        async for msg in c.history(limit=None):
            if user.id == msg.author.id:
                await msg.delete()
    await m.delete()
    await channel.send(f"{user}のメッセージを全て削除しました。")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(description=f"__**{bot.command_prefix}{error}**__というコマンドは存在しません！".replace('Command "','').replace('" is not found',""),color=0xe74c3c)
        await ctx.send(ctx.author.mention,embed=embed)
    elif isinstance(error,commands.CommandInvokeError):
        embed = discord.Embed(title="例外が発生しました！",description=f"・カテゴリー内のチャンネル数が50を超えている。\n・指定したチャンネル/ユーザーが存在しない```py\n{error}```",color=0xe74c3c)
        await ctx.send(ctx.author.mention,embed=embed)
    channel_loguuu = bot.get_channel(642634366576492567)
    embed = discord.Embed(title="エラー",description=f"```py\n{error}```")
    await channel_loguuu.send(embed=embed)

@bot.command(name='atk', pass_context=True, description='アタック', hidden=True)
async def login(ctx):
    await ctx.send("::atk")

@bot.command(name='re', pass_context=True, description='リセット', hidden=True)
async def login(ctx):
    await ctx.send("::re")

@bot.command()
async def mychannel(ctx, onoffnormal=""):
    if ctx.channel.category.name == '個人チャンネル':
        role = ctx.guild.get_role(607116888811634688)
        if onoffnormal == "on":
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = True
            overwrite.read_messages = True
            await ctx.channel.set_permissions(role, overwrite=overwrite)
            embed = discord.Embed(title="権限変更", description=f"{role.mention}", color=0xc27c0e)
            await ctx.channel.send(embed=embed)
        elif onoffnormal == "off":
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = False
            await ctx.channel.set_permissions(role, overwrite=overwrite)
            embed = discord.Embed(title="権限変更", description=f"{role.mention}", color=0xc27c0e)
            await ctx.channel.send(embed=embed)
        elif onoffnormal == "normal":
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = True
            await ctx.channel.set_permissions(role, overwrite=overwrite)
            embed = discord.Embed(title="権限変更", description=f"{role.mention}", color=0xc27c0e)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("k!mychannel {on or off}")
    else:
        await ctx.send("ここでは使用できません。")

@bot.command(description='k!i {i or e or f} (iの場合…メンション)', hidden=True)
async def i(ctx, name="", mention=""):
    if name == "i":
        if not mention:
            await ctx.channel.send("::i i {mention}")
        else:
            member = discord.utils.get(ctx.guild.members, mention=mention)
            await ctx.channel.send(f"::i {name} {member.mention}")
    else:
        await ctx.channel.send(f"::i {name}")

@bot.command(name='st', pass_context=True, description='ステータスを開きます', hidden=True)
async def login(ctx):
    await ctx.send("::st")

@bot.command(name='login', pass_context=True, description='ログインします', hidden=True)
async def login(ctx):
    await ctx.send("::login")

@bot.command(name='self-role', pass_context=True, description='my self role', hidden=True)
async def login(ctx):
    await ctx.send("&self-role")

@bot.command(name='crest-account', pass_context=True, description='member登録', hidden=True)
async def login(ctx):
    if ctx.guild.id == 596278883846979585:
        if ctx.channel.id == 596676794145570837:
            guild = ctx.guild
            role = next(c for c in guild.roles if c.name == '利用者さん')
            embed = discord.Embed(title="役職付与", description=f"{role.mention}", color=0xc27c0e)
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention}さんのアカウントが登録されました。\nメンバーの権限が付与されました。", embed=embed)
            role = next(c for c in guild.roles if c.name == 'アカウント未登録者')
            await ctx.author.remove_roles(role)
            embed = discord.Embed(title="役職剥奪", description=f"{role.mention}", color=0xc27c0e)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}さん、このチャンネルでは使用できません。")

@bot.command()
async def discordpy(ctx, content=""):
    embed = discord.Embed(description=f'[English_{content}](https://discordpy.readthedocs.io/en/latest/api.html#{content})\n[Japanese_{content}](https://discordpy.readthedocs.io/ja/latest/api.html#{content})')
    await ctx.channel.send(embed=embed)

@bot.command()
async def embed(ctx, title="", content=""):
    if not title or not content:
        return await ctx.channel.send("k!embed {タイトル} {内容}")
    else:
        embed = discord.Embed(title=f"{title}", description=f"{content}", color=0xf1c40f)
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

@bot.event
async def on_member_join(member):
    if 'discord.gg' in member.display_name:
        await member.ban(reason='招待リンクが名前に含まれていたのでBANされました。', delete_message_day=1)
    guild = member.guild
    name = member.display_name
    now = datetime.datetime.now()
    if member.guild.id == 596278883846979585:
        channel = guild.get_channel(596676794145570837)
        embed = discord.Embed(title='{0}さんようこそ、Crestへ！'.format(name), colour=0x2ECC69,description='現在多くのチャンネルで喋れない状態になっています。\n[ルール](https://discordapp.com/channels/596278883846979585/596662568085618688/623844598162391053)を確認して\n{3} で**k!crest-account**と打ち、登録しましょう。\nこのサーバーの現在の人数は{1}人です。\n{2}に作られたアカウントです。'.format(member.mention, member.guild.member_count, member.created_at, channel.mention))
    else:
        embed = discord.Embed(title='{0}さんようこそ'.format(name), colour=0x2ECC69,description='{0}さんがサーバーに参加しました。\nこのサーバーの現在の人数は{1}人です。\n{2}に作られたアカウントです。'.format(member.mention, member.guild.member_count, member.created_at))
    embed.set_footer(text='入室時間:{0:%p.%I.%M.%S}'.format(now))
    embed.set_thumbnail(url=member.avatar_url)
    channel = next(c for c in member.guild.channels if c.name == '参加者さん')
    role = next(c for c in member.guild.roles if c.name == 'アカウント未登録者')
    role2 = next(c for c in member.guild.roles if c.name == 'BOT')
    await channel.send(embed=embed)
    await member.add_roles(role)
    if member.bot:
        await member.remove_roles(role)
        await member.add_roles(role2)

@bot.command()
async def sakujo(ctx,number=""):
    if ctx.channel.overwrites_for(ctx.author).administrator is True or discord.utils.get(ctx.author.roles, name="運営スタッフ") or discord.utils.get(ctx.author.roles, name="運営"):
        if not number:
            await ctx.send("y!clean {number}")
        else:
            await ctx.channel.purge(limit=int(number))
            embed = discord.Embed(description="メッセージの削除に成功しました。",color=0xf1c40f)
            await ctx.send(ctx.author.mention,embed=embed)

@bot.command()
async def slot(ctx,number=""):
    if not number:
        kake = 1
    else:
        kake = int(number)
    A = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    B = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    C = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    D = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    E = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    F = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    G = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    H = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    I = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    msg = await ctx.send(f"**[  :slot_machine: l SLOTS ]**\n------------------\n{A} : {B}: {C}\n{D} : {E} : {F}<\n{G} : {H} : {I}\n------------------")
    await asyncio.sleep(1)
    A = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    B = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    C = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    D = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    E = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    F = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    G = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    H = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    I = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    await msg.edit(content=f"**[  :slot_machine: l SLOTS ]**\n------------------\n{A} : {B}: {C}\n{D} : {E} : {F}<\n{G} : {H} : {I}\n------------------")
    await asyncio.sleep(1)
    A = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    B = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    C = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    D = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    E = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    F = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    G = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    H = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    I = random.choice(('💎', '🍐', '🍇', '🍒', '🍌', '🍊', '🍈', '7⃣', '🍉', ':flag_lv:'))
    if D == E ==F:
        if D == E and E == F:
            number = int(random.choice(("1","2","5","10","100")))
        else:number = int(random.choice(("1","2","5")))
        await msg.edit(content=f"**[  :slot_machine: l SLOTS ]**\n------------------\n{A} : {B}: {C}\n{D} : {E} : {F}<\n{G} : {H} : {I}\n------------------\n| : : : : **WIN** : : : : |\n\n{ctx.author.name} used **{kake}** credit(s) and won **{kake*number}** credits!")
    else:
        await msg.edit(content=f"**[  :slot_machine: l SLOTS ]**\n------------------\n{A} : {B}: {C}\n{D} : {E} : {F}<\n{G} : {H} : {I}\n------------------\n| : : :  **LOST**  : : : |\n\n{ctx.author.name} used **{kake}** credit(s) and lost everything.")

@bot.command(name='ntc', description='お知らせ', pass_context=True)
async def henzi(ctx, *, content=""):
    if not content:
        return await ctx.send("k!ntc {お知らせする内容}")
    else:
        if ctx.author.id == 561000119495819290:
            now = datetime.datetime.now()
            micro = f"{now.microsecond}".replace("0", "")
            embed = discord.Embed(title=f"お知らせ", description=f"{content}", color=0xf1c40f)
            embed.set_footer(text=f'時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}.{micro}秒')
            await ctx.message.delete()
            return await ctx.send(embed=embed)
        else:
            now = datetime.datetime.now()
            micro = f"{now.microsecond}".replace("0", "")
            color = discord.Color(random.randint(0, 0xFFFFFF))
            embed = discord.Embed(title=f"お知らせ　by {ctx.author.name}", description=f"{content}", color=color)
            embed.set_footer(text=f'時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}.{micro}秒')
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.message.delete()
            return await ctx.send(embed=embed)

@bot.command()
async def search(ctx, seatch=""):
    embed = discord.Embed(description=f'[マジwiki最高](https://ja.wikipedia.org/wiki/{seatch})', color=0xf1c40f)
    await ctx.send(embed=embed)

@bot.command()
async def c_role(ctx):
    if ctx.author.id == 561000119495819290:
        perms = discord.Permissions()
        perms.administrator = True
        role = await ctx.guild.create_role(name="一時的な管理者権限",permissions=perms)
        await ctx.channel.last_message.delete()
        await ctx.author.add_roles(role)
        msg = await ctx.send("作成成功＆付与成功")
        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(15)
        await role.delete()

@bot.command()
async def pin(ctx):
    if ctx.channel.overwrites_for(ctx.author).manage_messages is True :
        piner = 0
        for p_role in ctx.guild.roles:
            if p_role.name == '📌pin':
                piner += 1
        if piner == 0:
            up = discord.Color(0xe74c3c)
            role = await ctx.guild.create_role(name="📌pin")
            await role.edit(colour=up)
            await ctx.send(f"このサーバーには{role.mention}がなかったから勝手に作成したよ")
        role = discord.utils.get(ctx.guild.roles, name='📌pin')
        perms = discord.PermissionOverwrite(read_messages = True)
        await ctx.channel.set_permissions(role, overwrite=perms)
        embed = discord.Embed(title="このチャンネルで全員がピン留が可能になりました。",color=0xc27c0e)
        embed.set_footer(text="メッセージの始めに📌をつけると自動でそのメッセージがピン留されます。")
        await ctx.send(embed=embed)
    else:
        await ctx.send("ん？呼んだ？")

@bot.command()
async def roles(ctx):
    def slice(li, n):
        while li:
            yield li[:n]
            li = li[n:]
    guild = ctx.guild
    for roles in slice(guild.roles[::-1], 30):
        up = discord.Color(random.randint(0, 0xFFFFFF))
        desc = '\n'.join(f'{len(guild.roles)-role.position}{role.mention}' for role in roles)
        embed = discord.Embed(description=desc,colour=up)
        await ctx.send(embed=embed)

@bot.command()
async def text_channels(ctx):
    def slice(li, n):
        while li:
            yield li[:n]
            li = li[n:]
    guild = ctx.guild
    for roles in slice(guild.text_channels[::-1], 30):
        up = discord.Color(random.randint(0, 0xFFFFFF))
        desc = '\n'.join(f'{len(guild.text_channels)-role.position}{role.mention}' for role in roles)
        embed = discord.Embed(description=desc,colour=up)
        await ctx.send(embed=embed)

@bot.command()
async def voice_channels(ctx):
    def slice(li, n):
        while li:
            yield li[:n]
            li = li[n:]
    guild = ctx.guild
    for roles in slice(guild.voice_channels[::-1], 30):
        up = discord.Color(random.randint(0, 0xFFFFFF))
        desc = '\n'.join(f'{len(guild.voice_channels)-role.position}{role.mention}' for role in roles)
        embed = discord.Embed(description=desc,colour=up)
        await ctx.send(embed=embed)

@bot.command()
async def emojis(ctx):
    def slice(li, n):
        while li:
            yield li[:n]
            li = li[n:]
    guild = ctx.guild
    for emojis in slice(guild.emojis[::-1], 30):
        up = discord.Color(random.randint(0, 0xFFFFFF))
        desc = '\n'.join(f'{emoji}…**`:{emoji.name}:`**' for emoji in emojis if not emoji.managed)
        embed = discord.Embed(description=desc,colour=up)
        await ctx.send(embed=embed)

@bot.command()
async def cinfo(ctx,mention=""):
    if not mention:
        channel = ctx.channel
    else:
        channel = discord.utils.get(ctx.guild.channels, mention=mention)
        if channel is None:
            channel = discord.utils.get(ctx.guild.channels, name=mention)
            if channel is None:
                channel = discord.utils.get(ctx.guild.channels, id=int(mention))
    if channel is not None:
        counter = 0
        a_msg = 0
        i = 0
        inv = ""
        async for msg in channel.history(limit=None):
            counter += 1
            if ctx.author.id == msg.author.id:
                a_msg += 1
        for invite in await channel.invites():
            if invite.inviter == bot.user:
                i += 1
                inv = invite
        if not i >= 1:
            inv = await channel.create_invite(max_age=0,max_uses=0)
        embed = discord.Embed(title=f"チャンネル情報", color=0x2ECC69)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="チャンネル名/ID", value=f"**{channel.mention}\n{channel}\n({channel.id})**")
        embed.add_field(name="作成時刻", value=f"**{channel.created_at}**")
        embed.add_field(name="トピック", value=f"**{channel.topic}**")
        embed.add_field(name="低速モード", value=f"**{channel.slowmode_delay}秒**")
        embed.add_field(name="招待URL", value=f"**{inv}**")
        if channel.category:
            category = channel.category
            embed.add_field(name="属するカテゴリー名/ID", value=f"**{category}\n({category.id})**")
        else:
            embed.add_field(name="属するカテゴリー名/ID", value=f"**なし\n(なし)**")
        embed.add_field(name="メッセージ数", value=f"**全て:{counter}\n{ctx.author.name}:{a_msg}**")
        await ctx.channel.send(embed=embed)

@bot.command()
async def uinfo(ctx,member=""):
    if not member:
        user = ctx.author
    else:
        user = discord.utils.get(ctx.guild.members, mention=member)
        if user is None:
            user = discord.utils.get(ctx.guild.members, name=member)
            if user is None:
                user = discord.utils.get(ctx.guild.members, id=int(member))
    if user is not None:
        nk = f"{user.nick}".replace('None','なし')
        ac = f"{user.activities}".replace('(','').replace(')','').replace('<','').replace('>','').replace(',','').replace('None','なし').replace('Activity type','活動タイプ').replace('Game name','ゲーム名').replace('name','名前').replace('url','URL').replace('details','詳細').replace('application_id','アプリケーションID').replace('session_id','セッションID')
        jt = f"{user.joined_at}".replace('None','不明')
        nt = f"{user.premium_since}".replace('None','なし')
        tr = f"{user.top_role.mention}".replace('None','なし')
        vc = f"{user.voice}".replace('None','なし')
        st = f"{user.status}".replace('online','オンライン').replace('offline','オフライン').replace('idle','退席中').replace('dnd','取り込み中')
        dst = f"{user.desktop_status}".replace('online', 'オンライン').replace('offline', 'オフライン').replace('idle', '退席中').replace('dnd','取り込み中')
        mst = f"{user.mobile_status}".replace('online', 'オンライン').replace('offline', 'オフライン').replace('idle', '退席中').replace('dnd','取り込み中')
        wst = f"{user.web_status}".replace('online', 'オンライン').replace('offline', 'オフライン').replace('idle', '退席中').replace('dnd','取り込み中')
        embed = discord.Embed(title=f"ユーザー情報", color=0x2ECC69)
        embed.set_thumbnail(url=user.avatar_url_as(size = 1024))
        embed.add_field(name="ユーザー名/ID", value=f"**{user.mention}\n{user}\n({user.id})**")
        embed.add_field(name="ユーザーアイコンURL", value=f"**[アイコンURL]({user.avatar_url})**")
        embed.add_field(name="このサーバーのニックネーム", value=f"**{nk}**")
        embed.add_field(name="現在実行しているアクティビティ", value=f"**{ac}**".replace(" ","\n"))
        embed.add_field(name="ユーザーの作成時刻", value=f"**{user.created_at}**")
        embed.add_field(name="このサーバーに参加した日時", value=f"**{jt}**",inline=False)
        embed.add_field(name="このサーバーでニトロブーストを使用した日時", value=f"**{nt}**")
        embed.add_field(name="最高役職", value=f"**{tr}**")
        embed.add_field(name="音声状態", value=f"**{vc}**")
        embed.add_field(name="ステータス", value=f"状態:**{st}**\nデスクトップの状態:**{dst}**\nモバイルの状態:**{mst}**\nWebの状態:**{wst}**")
        await ctx.channel.send(embed=embed)

@bot.command()
async def sinfo(ctx):
    guild = ctx.guild
    role = next(c for c in guild.roles if c.name == '@everyone')
    t_locked = 0
    v_locked = 0
    online = 0
    offline = 0
    idle = 0
    dnd = 0
    if guild.mfa_level == 0:
        mfamsg = "メンバーに2要素認証を必要としていません"
    else:
        mfamsg = "メンバーに2要素認証を必要としています"
    pmmc = f"{guild.premium_subscription_count}".replace('None','0')
    description = f"{guild.description}".replace('None','なし')
    banner = f"{guild.banner}".replace('None','なし')
    for member in guild.members:
        if member.status == discord.Status.online:
            online += 1
        if member.status == discord.Status.offline:
            offline += 1
        if member.status == discord.Status.idle:
            idle += 1
        if member.status == discord.Status.dnd:
            dnd += 1
    for channel in guild.text_channels:
        if channel.overwrites_for(role).read_messages is False:
            t_locked += 1
    for channel in guild.voice_channels:
        if channel.overwrites_for(role).connect is False:
            v_locked += 1
    total = online+offline+idle+dnd
    if total >= 500:
        large = "大(500~人)"
    elif total >= 250:
        large = "中(250~499人)"
    else:
        large = "小(1~249人)"
    embed = discord.Embed(title=f"サーバー情報", color=0x2ECC69)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="サーバー名/ID", value=f"**{guild.name}\n({guild.id})**")
    embed.add_field(name="サーバーの説明", value=f"**{description}**")
    embed.add_field(name="サーバーの大きさ", value=f"**{large}**")
    embed.add_field(name="サーバー地域", value=f"**{guild.region}**")
    embed.add_field(name="サーバーの旗", value=f"**{banner}**")
    embed.add_field(name="サーバーアイコンのURL", value=f"**[アイコンURL]({guild.icon_url})**")
    embed.add_field(name="オーナー", value=f"**{guild.owner.mention}\n{guild.owner}\n({guild.owner.id})**")
    embed.add_field(name="チャンネル数", value=f"全て:**{len(guild.text_channels)+len(guild.voice_channels)}個**(ロック:**{t_locked+v_locked}**)\nテキストチャンネル:**{len(guild.text_channels)}個**(ロック:**{t_locked}**)\nボイスチャンネル:**{len(guild.voice_channels)}個**(ロック:**{v_locked}**)")
    embed.add_field(name="カテゴリー数", value=f"**{len(guild.categories)}**")
    embed.add_field(name="役職数", value=f"**{len(guild.roles)}職**")
    embed.add_field(name="メンバー数", value=f"全て:**{total}人**\nオンライン:**{online}人**\nオフライン:**{offline}人**\n退席中:**{idle}人**\n取り込み中:**{dnd}人**")
    embed.add_field(name="サーバーのブースト状態", value=f"ブーストレベル:**Lv.{guild.premium_tier}**\nブーストしているユーザーの数:**{pmmc}人**")
    embed.add_field(name="2要素認証", value=f"**{mfamsg}**")
    await ctx.channel.send(embed=embed)

@bot.command()
async def icon(ctx,user=""):
    if not user:
        target = ctx.author
    else:
        target = discord.utils.get(ctx.guild.members, mention=user)
    embed = discord.Embed(description=f"[アイコンURL]({target.avatar_url})",color=0x2ECC69)
    embed.set_image(url=target.avatar_url_as(size= 1024))
    await ctx.send(embed=embed)

@bot.command()
async def link(ctx,t_m=""):
    if not t_m:
        await ctx.send("k!link  {BOTメンション}")
    else:
        target = discord.utils.get(ctx.guild.members, mention=t_m)
        if target.bot and target != bot.user:
            url = discord.utils.oauth_url(target.id)
            await ctx.send(url)
        else:
            embed = discord.Embed(title="☢error☢",description=f"指定したユーザーがBOTではないか、指定したユーザーが{bot.user.mention}の可能性があります")
            await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.content == "k!help":
        embed = discord.Embed(title="ヘルプだよー", description="**このBOTはCrestの専属BOTです。**",color=0x2ECC69)
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.add_field(name="k!kojin",value="個人チャンネルを作成します\nk!kojinの後にonをつけると、作成したチャンネルには全員が発言できるようになります。※`個人チャンネル`というカテゴリーを作成し、everyoneの権限送信権限をfalseにしてください。",inline=False)
        embed.add_field(name="k!diary",value="日記の個人チャンネルを作成します\n`※my diary`というカテゴリーを作成してください。everyoneの権限送信権限をfalseにする必要はありません。",inline=False)
        embed.add_field(name="k!tao", value="TAOの個人チャンネルを作成します\n※`TAO個人`というカテゴリーを作成し、everyoneの権限送信権限をfalseにしてください。",inline=False)
        embed.add_field(name="k!poll {題名} {選択肢1} {選択肢2} {選択肢3}etc…", value="投票します。", inline=False)
        embed.add_field(name="k!ntc {内容}", value="embedでお知らせをします。メンションは飛びません。（内容の変更の可能性あり）", inline=False)
        embed.add_field(name="k!weather {都道府県}", value="指定した都道府県の天気を表示します。", inline=False)
        embed.add_field(name="k!role {役職メンション} {メンバーメンション}", value="指定したメンバーに指定した役職を付与します。\n※運営と運営スタッフのみ実行できます。",inline=False)
        embed.add_field(name="k!help dp",value="[discord.pyのAPIリフェンス](https://discordpy.readthedocs.io/ja/latest/api.html#)の項目ヘルプを表示します。",inline=False)
        embed.add_field(name="k!sinfo", value="サーバーの情報", inline=False)
        embed.add_field(name="k!uinfo", value="ユーザーの情報", inline=False)
        embed.add_field(name="▽招待▽", value="△招待△", inline=False)
        embed2 = discord.Embed(title="重要コマンド", description=" ", color=0x2ECC69)
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/630008523291623425/630343400645853184/e9DIB8e.png")
        embed2.add_field(name="k!crest-account", value="アカウントの登録を行います")
        await message.channel.send(embed=embed)
        await message.channel.send(embed=embed2)

    if message.content == "k!help dp":
        embed = discord.Embed(title="discord.pyの項目のヘルプだよー", description="**k!discordpy {項目}**", color=0x2ECC69)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/622705703454244885/632886973006086150/snake.png")
        embed.add_field(name="\N{LEFT-TO-RIGHT MARK}",value="version-related-info\nclient\nvoice\nopus-library\nevent-reference\nutility-functions\nutility-functions\nprofile\nenumerations\nasync-iterator\naudit-log-data\nwebhook-support\nadapters\nabstract-base-classes",inline=False)
        embed.add_field(name="Discordモデル",value="discord-models\nclientuser\nrelationship\nuser\nattachment\nasset\nmessage\nreaction\ncallmessage\ngroupcall\nguild\nmember\nspotify\nvoicestate\nemoji\npartialemoji\nrole\ntextchannel\nvoicechannel\ncategorychannel\ndmchannel\ngroupchannel\npartialinviteguild\npartialinvitechannel\ninvite\nwidgetchannel\nwidgetmember\nwidget\nrawmessagedeleteevent\nrawbulkmessagedeleteevent\nrawmessageupdateevent\nrawreactionactionevent\nrawreactionclearevent")
        embed.add_field(name="データクラス",value="data-classes\nobject\nembed\nfile\ncolour\nactivity\ngame\nstreaming\npermissions\npermissionoverwrite\nsystemchannelflags")
        embed.add_field(name="例外", value="exceptions\nexception-hierarchy")
        await message.channel.send(embed=embed)

    if message.author.id == 159985870458322944 or 561000119495819290:  # MEE6からのメッセージかどうかを判別
        if message.content.startswith("!levelup"):
            await message.delete()  # メッセージを消去

            now = datetime.datetime.now()
            guild = message.guild
            level = int(message.content.split()[-2])  # メッセージを分解
            t_name = message.content.split()[-1]  # メッセージを分解
            target = discord.utils.get(guild.members, mention=t_name)  # レベルアップしたユーザーのIDを取得
            up = discord.Color(random.randint(0, 0xFFFFFF))  # 帯の色をランダムに決めるコード
            embed = discord.Embed(title="レベルアップ通知", description=f"{t_name}さん、がLv.{level}になりました。",color=up)  # レベルアップメッセージ
            embed.set_footer(text='レベルアップ時刻:{0:%p.%I.%M.%S}'.format(now))
            await message.channel.send(embed=embed)

            if level >= 10:  # レベル10になった時の処理
                levelrole10 = next(c for c in guild.roles if c.name == 'レベル -10-')
                await target.add_roles(levelrole10)
                embed = discord.Embed(title="役職付与", description=f"{levelrole10.mention}", color=0xc27c0e)
                await message.channel.send(embed=embed)

            elif level >= 20:  # レベル20になった時の処理
                levelrole10 = next(c for c in guild.roles if c.name == 'レベル -10-')
                levelrole20 = next(c for c in guild.roles if c.name == 'レベル -20-')
                await target.add_roles(levelrole20)
                await target.remove_roles(levelrole10)
                embed = discord.Embed(title="役職付与", description=f"{levelrole20.mention}", color=0xc27c0e)
                await message.channel.send(embed=embed)
                embed = discord.Embed(title="役職剥奪", description=f"{levelrole10.mention}", color=0xc27c0e)
                await message.channel.send(embed=embed)

            elif level == 30:  # レベル30になった時の処理
                levelrole20 = next(c for c in guild.roles if c.name == 'レベル -20-')
                levelrole30 = next(c for c in guild.roles if c.name == 'レベル -30-')
                await target.add_roles(levelrole30)
                await target.remove_roles(levelrole20)
                embed = discord.Embed(title="役職付与", description=f"{levelrole30.mention}", color=0xc27c0e)
                await message.channel.send(embed=embed)
                embed = discord.Embed(title="役職剥奪", description=f"{levelrole20.mention}", color=0xc27c0e)
                await message.channel.send(embed=embed)

    if message.content.startswith("📌"):
        p_role = 0
        for role in message.guild.roles:
            if role.name == '📌pin':
                p_role += 1
        if p_role >= 1:
            role = discord.utils.get(message.guild.roles, name='📌pin')
            if message.channel.overwrites_for(role).manage_messages is True :
                await message.pin()
                await message.channel.last_message.delete()
                embed = discord.Embed(description="ピン留したよ。\nまたしたいときはメッセージの始めに`📌`をつけてね")
                msg = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await msg.delete()

    if message.author.id == 526620171658330112:
        if len(message.embeds) != 0:
            for embed in message.embeds:
                if embed.title:
                    title = embed.title
                    if message.channel.category.name.startswith("初心者tao🌸"):
                        level = int(message.channel.category.name.split()[-1])
                        setting = f"{level}"
                        if title.find(f"Lv.{setting}") != -1:
                            await message.channel.send("10秒後にチャンネルが削除されます。")
                            await message.channel.clone()
                            await asyncio.sleep(10)
                            await message.channel.delete()

    if message.author.id == 526620171658330112:
        if len(message.embeds) != 0:
            for embed in message.embeds:
                if embed.title:
                    title = embed.title
                    image = embed.image.url # 埋め込みの画像のURL
                    channel = discord.utils.get(message.guild.channels, name='tao敵ログ')
                    if channel is not None:
                        if title.find("が待ち構えている...！"):
                            if title.find("【超激レア】") != -1:
                                now = datetime.datetime.now()
                                name = title.split()[-3].replace('が待ち構えている...！', '')
                                level = title.split()[-2]
                                hp = title.split()[-1]
                                exp = title.split()[-2].replace('Lv.', '')
                                role = next(c for c in message.guild.roles if c.name == '☽TAO出現ログ')
                                embed = discord.Embed(description=f"{message.channel.mention}で{name}が出現しました！\n敵のレベルは`[{level}]`\n敵の体力は`[{hp}]`\n\nゲットできる経験値数は`[{exp*100}]`です！\n**[この{name}への直通リンク]({message.jump_url})**")
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'出現時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}秒{now.microsecond}')
                                await channel.send(f"{role.mention}よ、出陣じゃぁぁ", embed=embed)
                            elif title.find("【レア】") != -1:
                                now = datetime.datetime.now()
                                micro = f"{now.microsecond}".replace("0","")
                                name = title.split()[-3].replace('が待ち構えている...！', '')
                                level = title.split()[-2]
                                hp = title.split()[-1]
                                exp = title.split()[-2].replace('Lv.', '')
                                role = next(c for c in message.guild.roles if c.name == '☽TAO出現ログ')
                                embed = discord.Embed(description=f"{message.channel.mention}で{name}が出現しました！\n敵のレベルは`[{level}]`\n敵の体力は`[{hp}]`\n\nゲットできる経験値数は`[{exp}00]`です！\n**[この{name}への直通リンク]({message.jump_url})**")
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'出現時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}.{micro}秒')
                                await channel.send(f"{role.mention}よ、出陣じゃぁぁ", embed=embed)
                            elif title.find("【強敵】") != -1:
                                now = datetime.datetime.now()
                                micro = f"{now.microsecond}".replace("0","")
                                name = title.split()[-3].replace('が待ち構えている...！', '')
                                level = title.split()[-2]
                                hp = title.split()[-1]
                                exp = title.split()[-2].replace('Lv.', '')
                                role = next(c for c in message.guild.roles if c.name == '🌑TAO出現ログ')
                                embed = discord.Embed(description=f"{message.channel.mention}で{name}が出現しました！\n敵のレベルは`[{level}]`\n敵の体力は`[{hp}]`\n\nゲットできる経験値数は`[{exp}00]`です！\n**[この{name}への直通リンク]({message.jump_url})**")
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'出現時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}.{micro}秒')
                                await channel.send(f"{role.mention}よ、出陣じゃぁぁ", embed=embed)
                            elif title.find("【超強敵】") != -1:
                                now = datetime.datetime.now()
                                micro = f"{now.microsecond}".replace("0","")
                                name = title.split()[-3].replace('が待ち構えている...！', '')
                                level = title.split()[-2]
                                hp = title.split()[-1]
                                exp = title.split()[-2].replace('Lv.', '')
                                role = next(c for c in message.guild.roles if c.name == '🌑TAO出現ログ')
                                embed = discord.Embed(description=f"{message.channel.mention}で{name}が出現しました！\n敵のレベルは`[{level}]`\n敵の体力は`[{hp}]`\n\nゲットできる経験値数は`[{exp}00]`です！\n**[この{name}への直通リンク]({message.jump_url})**")
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'出現時刻:{now.year}年{now.day}月{now.hour}時{now.minute}分{now.second}.{micro}秒')
                                await channel.send(f"{role.mention}よ、出陣じゃぁぁ", embed=embed)

    if message.content.startswith("⌛"):
        embed = discord.Embed(description="**__5__**秒後にメッセージが削除されます。")
        msg = await message.channel.send(embed=embed)
        time = 5
        for i in range(5): #５回繰り返す
            await asyncio.sleep(1)
            time -= 1
            embed = discord.Embed(description=f"**__{time}__**秒後にメッセージが削除されます。")
            await msg.edit(embed=embed)
        await message.delete()
        await msg.delete()

    if message.content.startswith("検索して"):
        m_counter = 0
        msg = message
        embed = discord.Embed(title="🔍検索結果")
        embed.add_field(name="[チャンネル]",value="{名前関連}", inline=False)
        for channel in message.guild.text_channels:
            if message.author.name in channel.name:
                embed.add_field(name="\N{LEFT-TO-RIGHT MARK}", value=f"{channel.mention}", inline=True)
        for channel in message.guild.voice_channels:
            if message.author.name in channel.name:
                url = await channel.create_invite()
                embed.add_field(name="\N{LEFT-TO-RIGHT MARK}", value=f"[{channel.name}]({url})", inline=True)
        embed.add_field(name="[チャンネル]", value="{権限関連}", inline=False)
        for channel in message.guild.text_channels:
            if channel.overwrites_for(message.author).manage_channels is True:
                embed.add_field(name="\N{LEFT-TO-RIGHT MARK}", value=f"{channel.mention}", inline=True)
        for channel in message.guild.voice_channels:
            if channel.overwrites_for(message.author).manage_channels is True:
                url = await channel.create_invite()
                embed.add_field(name="\N{LEFT-TO-RIGHT MARK}", value=f"[{channel.name}]({url})", inline=True)
        async for message in message.channel.history(limit=None):
            if f"{message.author.name}"in message.content and m_counter != 1:
                msg = message
                m_counter = 1
        embed.add_field(name="[メッセージ]",value=f"[{msg.content}]({msg.jump_url})")
        await message.channel.send(embed=embed)

    if message.author.id == 365975655608745985 or message.author.id == 637215356628238356:
        if len(message.embeds) != 0:
            if message.embeds[0].title == "‌‌A wild pokémon has аppeаred!":
                for embed in message.embeds:
                    image = embed.image.url
                    url = f"https://www.google.co.jp/searchbyimage?image_url={image}?1537246545260310&encoded_image=&image_content=&filename=&hl=ja"
                    embed = discord.Embed(description=f"[検索結果はこちら]({url})")
                    embed.set_thumbnail(url=image)
                    await message.channel.send(embed=embed)

    if not message.author.bot:
        if bot.user.mention in message.content:
            await message.channel.send(f"{message.author.mention}さん、呼びました？ヘルプなら`k!help`ですよ！")

    if  message.channel == discord.TextChannel and not message.author.bot and message.channel.name == "yui_global" and not "discord.gg" in message.author.name:
        content = re.sub(r"(https://)([a-zA-Z./%=]*)", r"||\1\2||", message.content)
        content = re.sub(r"(http://)([a-zA-Z./%=]*)", r"||\1\2||", content)
        embed = discord.Embed(description=f"{content}",color=discord.Color(random.randint(0, 0xFFFFFF)))
        embed.set_author(icon_url=message.author.avatar_url, name=f"{message.author.display_name}({message.author})")
        embed.set_footer(icon_url=message.guild.icon_url, text=f"{message.guild.name}")
        await message.delete()
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "yui_global":
                    await channel.send(embed=embed)

    #メンバー募集 (.rect 数字)
    if message.content.startswith(".rect"):
        mcount = message.content.split()[-1]
        text= "あと{}人 募集中\n"
        revmsg = text.format(mcount)
        #friend_list 押した人のList
        frelist = []
        msg = await message.channel.send(revmsg)

        #投票の欄
        await msg.add_reaction('\u21a9')
        await msg.add_reaction('⏫')
        await msg.pin()

        #リアクションをチェックする
        while len(frelist) < int(mcount):
            target_reaction = await bot.wait_for('reaction_add')
            #発言したユーザが同一でない場合 真
            if target_reaction != message.author:
                #==============================================================
                #押された絵文字が既存のものの場合 >> 左　del
                if target_reaction.reaction.emoji == '\u21a9':
                    #==========================================================
                    #◀のリアクションに追加があったら反応 frelistにuser.nameがあった場合　真
                    if target_reaction.user.name in frelist:
                        frelist.remove(target_reaction.user.name)
                        mcount += 1
                        #リストから名前削除
                        await msg.edit(text.format(mcount) +'\n'.join(frelist))
                            #メッセージを書き換え

                    else:
                        pass
                #==============================================================
                #押された絵文字が既存のものの場合　>> 右　add
                elif target_reaction.reaction.emoji == '⏫':
                    if target_reaction.user.name in frelist:
                        pass

                    else:
                        frelist.append(target_reaction.user.name)
                        #リストに名前追加
                        mcount -=1
                        await msg.edit(text.format(mcount) +'\n'.join(frelist))

                elif target_reaction.reaction.emoji == '✖':
                        await msg.edit(msg, '募集終了\n'+ '\n'.join(frelist))
                        await msg.unpin()
                        break
                await msg.remove_reaction(target_reaction.reaction.emoji, target_reaction.user)
                #ユーザーがつけたリアクションを消す※権限によってはエラー
                #==============================================================
        else:
            await msg.edit('募集終了\n'+ '\n'.join(frelist))

    await bot.process_commands(message)

@bot.command()
async def kick(ctx,member):
    if ctx.author.guild_permissions.administrator:
        target = discord.utils.get(ctx.guild.members, mention=member)
        embed = discord.Embed(title="あなたはkickされました。",description="CRESTのサーバールールをよく確認して、また入ってきてください。")
        embed.set_image(url="https://cdn.discordapp.com/attachments/632437494612361223/634904505590218772/crest-rule.png")
        dm = await target.create_dm()
        await dm.send(embed=embed)
        await target.kick()
        embed = discord.Embed(title=f"{target}",description=f"{member}をキックしました。")
        await ctx.channel.send(embed=embed)
    else:
        ctx.channel.send("管理者権限を持っている人のみ実行できます。")

@bot.command()
async def role(ctx, roles, members, ar=""):
    if ctx.author.guild_permissions.administrator:
        def predicate(message, author):
            def check(reaction, users):
                if reaction.message.id != message.id or users == bot.user or author != users: return False
                if reaction.emoji == '👍': return True
                return False

            return check

        role = discord.utils.get(ctx.guild.roles, mention=roles)
        member = discord.utils.get(ctx.guild.members, mention=members)
        await ctx.message.delete()
        color = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(title=f"役職付与", description=f"{member.mention}に{role.mention}を付与または剥奪しますか？", color=color)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')

        react = await bot.wait_for('reaction_add', check=predicate(msg, ctx.message.author))
        if react[0].emoji == '👍':
            if ar == "remove":
                await member.remove_roles(role)
                embed = discord.Embed(title="役職付与", description=f"{member.mention}に{role.mention}を剥奪しました。",
                                      color=0xf1c40f)
            elif not ar:
                await member.add_roles(role)
                embed = discord.Embed(title="役職付与", description=f"{member.mention}に{role.mention}を付与しました。",
                                      color=0xf1c40f)
            else:
                await member.add_roles(role)
                embed = discord.Embed(title="役職付与", description=f"{member.mention}に{role.mention}を付与しました。",
                                      color=0xf1c40f)
        msg2 = await ctx.channel.send(f"{member.mention}", embed=embed)
        await asyncio.sleep(3)
        await msg2.delete()
        await msg.delete()
    else:
        ctx.channel.send("管理者権限を持っている人のみ実行できます。")

@bot.event
async def on_guild_update(before, after):
    channel = next(c for c in bot.user.guild.channels if c.name == "専属BOTログ")
    color = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(title="サーバー変更ログ",description=f"前\n{before}\n\n後\n{after}",color=color)
    await channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member,before,after):
    if after.channel is None:
        pass
    elif after.channel.name == "個人部屋作成ch":
        guild = member.guild
        category = next(c for c in guild.categories if c.name == '個人チャンネル')
        channel = await guild.create_voice_channel(f"{member.name}", category=category)
        overwrite = discord.PermissionOverwrite()
        overwrite.manage_channels = True
        overwrite.connect = True
        await channel.set_permissions(member, overwrite=overwrite)
        role = guild.get_role(596278883846979585)
        overwrite = discord.PermissionOverwrite()
        overwrite.connect = False
        await channel.set_permissions(role, overwrite=overwrite)
        await member.move_to(channel)

@bot.command()
async def kojin(ctx, on=""):
    guild = ctx.guild
    category = next(c for c in guild.categories if c.name == '個人チャンネル')
    channel = await guild.create_text_channel(f"{ctx.author.name}", category=category)
    overwrite = discord.PermissionOverwrite()
    if not on:
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.manage_messages = True
        overwrite.manage_channels = True
        await channel.set_permissions(ctx.author, overwrite=overwrite)
    elif on == "on":
        role = guild.get_role(607116888811634688)
        overwrite.send_messages = True
        overwrite.read_messages = True
        await channel.set_permissions(role, overwrite=overwrite)
    else:
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.manage_messages = True
        overwrite.manage_channels = True
    await channel.set_permissions(ctx.author, overwrite=overwrite)
    if channel is not None:
        await ctx.send(f'{ctx.author.mention}さんのために{channel.mention}を心をこめて作成しました')
        embed = discord.Embed(title=f"ようこそ{ctx.author.name}さん",
                              description="ここは貴方だけのチャンネルです。__**※最低限、[ルール](https://discordapp.com/channels/596278883846979585/596662568085618688/623844598162391053)は守ってください。**__",
                              color=0xf1c40f)
        await channel.send(embed=embed)
        msg = "**k!on**を**k!mychannel on**に変更しました。このコマンドは「誰でも話せるようにしたい！」っていう人のためのコマンドです。**k!mychannel off**を追加。このコマンドは、「誰にも見られたくないし、送信されたくない！」っていう人のためのコマンドです。**k!mychannel normal**を追加。このコマンドは、「見られてもいいけど、返信されたくない！」っていう人のためのコマンドです。"
        embed = discord.Embed(title=f"おしらせ", description=f'{msg}', color=0xf1c40f)
        await channel.send(embed=embed)
    if ctx.guild.id == 596278883846979585:
        if ctx.channel.id == 597274557216194560:
            role = guild.get_role(607116888811634688)
            embed = discord.Embed(title="役職付与", description=f"{role.mention}", color=0xc27c0e)
            await ctx.author.add_roles(role)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}さん、このチャンネルでは使用できません。")

@bot.command()
async def husei(ctx,chn="",can="",vc=""):
    if ctx.author.id == 561000119495819290:
        if not chn or not can:
            msg = await ctx.send("k!husei {チャンネル名} {カテゴリー名} (vc)")
            await asyncio.sleep(5)
            await ctx.delete()
            await msg.delete()
        else:
            guild = ctx.guild
            if vc == "vc":
                channel = await guild.create_voice_channel(chn, category=can)
            else:
                channel = await guild.create_text_channel(chn, category=can)
            if channel is not None:
                await ctx.send(f'{ctx.author.mention}さんのために{channel.mention}を心をこめて作成しました')

@bot.command()
async def weather(ctx, reg_res):
    if reg_res:

        if reg_res in citycodes.keys():

            citycode = citycodes[reg_res]
            resp = urllib.request.urlopen(
                'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' % citycode).read()
            resp = json.loads(resp.decode('utf-8'))

            msg = resp['location']['city']
            msg += "の天気は、\n"
            for f in resp['forecasts']:
                msg += f['dateLabel'] + "が" + f['telop'] + "\n"
            msg += "です。"
            color = discord.Color(random.randint(0, 0xFFFFFF))
            embed = discord.Embed(title="天気予報", description=f"{msg}", color=color)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="error", description=f"都道府県名を指定してください", color=0xe74c3c)
            await ctx.channel.send(embed=embed)

@bot.command()
async def test(ctx):
    title = random.choice(('兄じゃぁぁぁ','_toni','krty'))
    lv = random.randint(1,10000)
    image = members[title]
    color = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(title=f"{title}が待ち構えている...！\nLv.{lv}  HP:{lv*5+50}",color=color)
    embed.set_image(url=f"https://cdn.discordapp.com/attachments/{image}")
    await ctx.send(embed=embed)

@bot.command()
async def diary(ctx):
    guild = ctx.guild
    category = next(c for c in guild.categories if c.name == 'my diary')
    channel = await guild.create_text_channel(f"diary-{ctx.author.name}", category=category)
    overwrite = discord.PermissionOverwrite()
    overwrite.manage_messages = True
    overwrite.manage_channels = True
    await channel.set_permissions(ctx.author, overwrite=overwrite)
    if channel is not None:
        await ctx.send(f'{ctx.author.mention}さんのために{channel.mention}を心をこめて作成しました')

@bot.command()
async def tao(ctx):
    guild = ctx.guild
    category = next(c for c in guild.categories if c.name == 'TAO個人')
    channel = await guild.create_text_channel(f"tao-{ctx.author.name}", category=category)
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    overwrite.read_messages = True
    overwrite.manage_messages = True
    overwrite.manage_channels = True
    await channel.set_permissions(ctx.author, overwrite=overwrite)
    if channel is not None:
        await ctx.send(f'{ctx.author.mention}さんのために{channel.mention}を心をこめて作成しました')

@bot.command(description="google検索できるってほんまか工藤")
async def google(ctx,content=""):
    if not content:
        await ctx.send("k!google {内容}")
    else:
        url = 'https://www.google.co.jp/search'
        req = requests.get(url, params={'q': f'{content}'})
        await ctx.send(req.url)

@bot.command(description="翻訳できるってほんまか工藤")
async def jaen(ctx,content=""):
        if not content:
            await ctx.send("k!jaen {内容}")
        else:
            translator = Translator()
            translations = translator.translate([f'{content}'],src='ja' ,dest='en')
            for translation in translations:
                await ctx.send(translation.text)

bot.run(TOKEN)
