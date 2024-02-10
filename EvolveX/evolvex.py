import discord
from io import BytesIO
from discord.ext import commands
from discord.ext import tasks
import openai
import asyncio
import json
import requests
import os
import random
from datetime import datetime, timedelta


prefix = "x"
TOKEN = "MTE3NTg4OTc1ODkyNTM2OTQ3NQ.GhCuSJ.DKHenN4cO6WPi_12q5vWNb8jenyoCqMPnuJM2g"
STATUS = "EvolveX"
owner_id = 1002971583989690418

WARNING_DURATION = 60
intents = discord.Intents.all()
intents.messages = True


bot = commands.Bot(command_prefix=prefix, intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.chane_presence(activity=discord.Game(name="EvolveX"))




spam_filter_enabled = False
BAKIYE_VERITABANI = "economy.json"
PAZAR_VERITABANI = "pazar.json"
database_file = 'database.json'
RANK_FILE = "rank.json"
antiraid_file = "antiraid.json"
afk_file = 'afk.json'
ANTIRAID_FILE = "antiraid.json"
WARNING_DURATION = 60 
antiraid_warnings = {}
antiraid_timeout = timedelta(seconds=30)
antiraid_data = {}
DEFAULT_LEVEL = 1
DEFAULT_XP = 0
uyari_dict = {}
spam_dict = {}
bahisler = {}
tickets = {}
rank_data = {}
afk_users = {}
blocked_users = {}
warnings = {}
support_role_id = None
caps_filter_enabled = True

def contains_caps(message):
    
    return sum(1 for c in message if c.isupper()) > len(message) / 2



try:
    with open('caps.json', 'r') as f:
        blocked_users = json.load(f)
except FileNotFoundError:
    blocked_users = []


if os.path.exists(BAKIYE_VERITABANI):
    
    with open(BAKIYE_VERITABANI, "r") as f:
        bakiyeler = json.load(f)

if not os.path.exists(PAZAR_VERITABANI):
    with open(PAZAR_VERITABANI, "w") as f:
        json.dump({}, f)

def load_database():
    global tickets, support_role_id
    try:
        with open(database_file, 'r') as file:
            data = json.load(file)
            tickets = data.get('tickets', {})
            support_role_id = data.get('support_role_id', None)
    except FileNotFoundError:
        pass

def save_database():
    data = {'tickets': tickets, 'support_role_id': support_role_id}
    with open(database_file, 'w') as file:
        json.dump(data, file, indent=2)

@bot.event
async def on_ready():
    if not os.path.exists(database_file):
        with open(database_file, 'w') as file:
            json.dump({'tickets': {}, 'support_role_id': None}, file, indent=2)
    load_database()

help_dict = {
    "afk": "AFK moduna geçer.",
    "antiraid": "Anti-raid sistemini açar/kapatır.",
    "avatar": "Belirtilen kullanıcının avatarını paylaşır.",
    "bahis": "Belirtilen miktarla bahis yapar. Örneğin: !bahis 100",
    "capsengel": "Capslock kullanımını engeller.",
    "günlük": "Günlük ödül alırsınız.",
    "help": "Bu mesajı gösterir.",
    "hesap": "Banka hesap bilgilerinizi gösterir.",
    "level": "Seviyenizi gösterir.",
    "levelsys": "Seviye sistemini yönetir.",
    "market": "Marketi görüntüler.",
    "mute": "Kullanıcıyı susturur.",
    "para": "Mevcut bakiyenizi gösterir.",
    "pazar": "Pazardaki ürünleri gösterir.",
    "ping": "Botun pingini gösterir.",
    "plastikelisleri": "Plastik el işleri hakkında bilgi alın.",
    "profil": "Profilinizi gösterir.",
    "rank": "Sıralamanızı gösterir.",
    "rastgele": "Rastgele bir sayı gösterir.",
    "satınal": "Pazardan belirtilen ürünü satın alır.",
    "sonuç": "Bahisin sonuçlanmasını kontrol eder.",
    "spamengel": "Spam engelini açma veya kapatma.",
    "temizle": "Belirtilen miktarda mesaj siler.",
    "ticket": "Yeni bir destek talebi oluşturur.",
    "ticketkapat": "Destek talebini kapatır.",
    "ticketrol": "Destek talepleri için rol ataması yapar.",
    "transfer": "Belirtilen kullanıcıya para transfer eder.",
    "uyarı": "Kullanıcıya uyarı verir. 3 uyarı alınca mute atılır.",
    "yardim": "Botun genel komutlarını gösterir.",
    "ürünekle": "Pazara yeni bir ürün ekler.",
    "capsengel": "Caps-Lock engelini açar/kapatır."
}




@bot.command(name="yardım")
async def help_command(ctx, *, command=None):
    if command is None:
        help_embed = discord.Embed(title="Komutlar", color=discord.Color.blue())
        for command, description in help_dict.items():
            help_embed.add_field(name=f"{prefix}{command}", value=description, inline=False)
        await ctx.send(embed=help_embed)
    elif command.lower() in help_dict:
        specific_command = command.lower()
        specific_description = help_dict[specific_command]
        specific_embed = discord.Embed(title=f"{prefix}{specific_command}", description=specific_description, color=discord.Color.green())
        await ctx.send(embed=specific_embed)
    else:
        await ctx.send("Belirtilen komut bulunamadı.")


@bot.command(name='para', help='Mevcut bakiyenizi gösterir.')
async def para(ctx):
    user_id = str(ctx.author.id)
    with open("economy.json", "r") as f:
        economy_data = json.load(f)
        bakiye = economy_data.get(user_id, 0)
    await ctx.send(f'{ctx.author.mention} Mevcut bakiyeniz: {bakiye} TL')


@bot.command(name='günlük', help='Günlük ödül alırsınız.')
async def gunluk(ctx):
    user_id = str(ctx.author.id)
    with open("economy.json", "r") as f:
        economy_data = json.load(f)
        last_claimed = economy_data.get(f"{user_id}_last_claimed", None)

    if last_claimed is not None:
        last_claimed = datetime.strptime(last_claimed, "%Y-%m-%d %H:%M:%S")
        if datetime.utcnow() - last_claimed < timedelta(days=1):
            await ctx.send(f'{ctx.author.mention} Zaten bugün günlük ödülünü aldınız.')
            return

    odul = random.randint(100, 500)
    economy_data[user_id] = economy_data.get(user_id, 0) + odul
    economy_data[f"{user_id}_last_claimed"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    with open("economy.json", "w") as f:
        json.dump(economy_data, f)

    await ctx.send(f'{ctx.author.mention} Günlük ödülünüz: {odul} TL')


@bot.command(name='transfer', help='Belirtilen kullanıcıya para transfer eder.')
async def transfer(ctx, kullanici: discord.Member, miktar: int):
    if miktar <= 0:
        await ctx.send('Geçersiz miktar. Lütfen pozitif bir miktar girin.')
        return

    user_id = str(ctx.author.id)
    target_user_id = str(kullanici.id)

    with open("economy.json", "r") as f:
        economy_data = json.load(f)
        bakiye = economy_data.get(user_id, 0)

    if bakiye < miktar:
        await ctx.send('Yetersiz bakiye. Transfer işlemi gerçekleştirilemedi.')
        return

    economy_data[user_id] -= miktar
    economy_data[target_user_id] = economy_data.get(target_user_id, 0) + miktar

    with open("economy.json", "w") as f:
        json.dump(economy_data, f)

    await ctx.send(f'{ctx.author.mention} Başarıyla {kullanici.mention} kullanıcısına {miktar} TL transfer edildi.')


@bot.command(name='hesap', help='Banka hesap bilgilerinizi gösterir.')
async def hesap(ctx):
    user_id = str(ctx.author.id)
    with open("economy.json", "r") as f:
        economy_data = json.load(f)
        bakiye = economy_data.get(user_id, 0)

    await ctx.send(f'{ctx.author.mention} Banka hesap bilgileriniz: {bakiye} TL')


@bot.command(name='market', help='Marketi görüntüler.')
async def market(ctx):
    embed = discord.Embed(title='Market', description='Aşağıda market ürünleri bulunmaktadır:', color=discord.Color.gold())
    embed.add_field(name='1. Yemek', value='Fiyat: 50 TL, Enerji: +20', inline=False)
    embed.add_field(name='2. İçecek', value='Fiyat: 30 TL, Susuzluk: -10', inline=False)
    embed.add_field(name='3. Hediyelik Eşya', value='Fiyat: 100 TL, Mutluluk: +30', inline=False)
    await ctx.send(embed=embed)



@bot.command(name='ping', description='Botun gecikmesini gösterir.')
async def ping(ctx):
    row = discord.ui.View()

    message = await ctx.send(content=f'https://dummyimage.com/2000x500/33363c/ffffff&text={round(bot.latency * 1000)}%20MS', view=row)

    def check(interaction):
        return interaction.user.id == ctx.author.id

    try:
        interaction = await bot.wait_for('button_click', timeout=30, check=check)
        if interaction.custom_id == 'guq':
            await message.edit(content=f'https://dummyimage.com/2000x500/33363c/ffffff&text={round(bot.latency * 1000)}%20MS /n YiTechX Code', view=None)
    except asyncio.TimeoutError:
        await message.edit(content='Zaman aşımına uğradı', view=None)

@bot.command(name='temizle', help='Belirtilen miktarda mesaj siler.')
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1) 
    await ctx.send(f'{miktar} mesaj silindi.')




@bot.command(name='rastgele', help='Rastgele bir sayı gösterir.')
async def rastgele(ctx):
    import random
    random_number = random.randint(1, 100)
    await ctx.send(f'Rastgele sayı: {random_number}')


@bot.command(name='uyarı', help='Kullanıcıya uyarı verir. 3 uyarı alınca mute atılır.')
@commands.has_permissions(manage_messages=True)
async def uyarı(ctx, member: discord.Member):
    
    if member.id not in uyari_dict:
        uyari_dict[member.id] = 1
    else:
        uyari_dict[member.id] += 1

    await ctx.send(f'{member.mention} kullanıcısına bir uyarı verildi. Toplam uyarı sayısı: {uyari_dict[member.id]}')

    
    if uyari_dict[member.id] >= 3:
        await mute(ctx, member)


@bot.command(name='mute', help='Kullanıcıyı susturur.')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason='Yok'):
   
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not muted_role:
        
        muted_role = await ctx.guild.create_role(name="Muted", reason="Mute komutu için otomatik oluşturuldu.")
        
       
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'{member.mention} susturuldu. Sebep: {reason}')


@bot.command(name='spamengel', help='Spam engelini açma veya kapatma.')
@commands.has_permissions(manage_messages=True)
async def spamengel(ctx, option):
    global spam_filter_enabled
    if option.lower() == 'aç':
        spam_filter_enabled = True
        await ctx.send('Spam engeli açıldı.')
    elif option.lower() == 'kapat':
        spam_filter_enabled = False
        await ctx.send('Spam engeli kapatıldı.')
    else:
        await ctx.send('Geçersiz bir seçenek. !spamengel aç veya !spamengel kapat kullanın.')


@tasks.loop(seconds=5)
async def spam_control():
    global spam_filter_enabled
    global spam_dict
    
    if spam_filter_enabled:
        for user_id, messages in list(spam_dict.items()):
            if len(messages) > 5:
                member = bot.get_user(user_id)
                await member.send('Spam yapma! Uyarıldın.')
                await member.kick(reason='Spam engel')
                del spam_dict[user_id]


@bot.event
async def on_message(message):
    global spam_filter_enabled
    global spam_dict
    
    if spam_filter_enabled and message.author.id not in spam_dict:
        spam_dict[message.author.id] = [message.content]
    elif spam_filter_enabled:
        spam_dict[message.author.id].append(message.content)

    await bot.process_commands(message)
    

@bot.command(name='bahis', help='Belirtilen miktarla bahis yapar. Örneğin: !bahis 100')
async def bahis(ctx, miktar: int):
    user_id = str(ctx.author.id)

   
    with open(BAKIYE_VERITABANI, "r") as f:
        economy_data = json.load(f)
        bakiye = economy_data.get(user_id, 0)

    if user_id in bahisler:
        await ctx.send('Zaten bir bahis yapmışsınız. Lütfen mevcut bahisin sonuçlanmasını bekleyin.')
        return

    if miktar > bakiye:
        await ctx.send('Yetersiz bakiye. Daha düşük bir bahis miktarı girin.')
        return

    if user_id not in economy_data:
        economy_data[user_id] = 500 

       
        with open(BAKIYE_VERITABANI, "w") as f:
            json.dump(economy_data, f)

    
    bahisler[user_id] = miktar

    await ctx.send(f'{ctx.author.mention} Başarıyla {miktar} TL ile bahis yaptınız.')
    


@bot.command(name='sonuç', help='Bahisin sonuçlanmasını kontrol eder.')
async def sonuc(ctx):
    user_id = str(ctx.author.id)

    if user_id not in bahisler:
        await ctx.send('Henüz bir bahis yapmadınız. xbahis komutu ile bahis yapabilirsiniz.')
        return

    
    kazandi = random.choice([True, False])

   
    miktar = bahisler.pop(user_id)

    
    with open(BAKIYE_VERITABANI, "r") as f:
        bakiyeler = json.load(f)

    if kazandi:
        bakiye = bakiyeler.get(user_id, 0) + miktar
        await ctx.send(f'{ctx.author.mention} Tebrikler! {miktar} TL kazandınız. Yeni bakiyeniz: {bakiye} TL')
    else:
        bakiye = bakiyeler.get(user_id, 0)
        await ctx.send(f'{ctx.author.mention} Maalesef! {miktar} TL kaybettiniz. Mevcut bakiyeniz: {bakiye} TL')

    bakiyeler[user_id] = bakiye

    with open(BAKIYE_VERITABANI, "w") as f:
        json.dump(bakiyeler, f)


@bot.command(name='ürünekle', help='Pazara yeni bir ürün ekler.')
async def urun_ekle(ctx, urun: str, fiyat: int):
    user_id = str(ctx.author.id)

    
    with open(PAZAR_VERITABANI, "r") as f:
        pazar_data = json.load(f)

    
    if user_id in pazar_data:
        await ctx.send('Zaten pazarda bir ürününüz bulunuyor. Satın alınana kadar ek ürün ekleyemezsiniz.')
        return

    
    pazar_data[user_id] = {"urun": urun, "fiyat": fiyat}

    
    with open(PAZAR_VERITABANI, "w") as f:
        json.dump(pazar_data, f)

    await ctx.send(f'{ctx.author.mention} Başarıyla pazarı güncellediniz. Ürün: {urun}, Fiyat: {fiyat} TL')


@bot.command(name='pazar', help='Pazardaki ürünleri gösterir.')
async def pazar_goster(ctx):
    
    with open(PAZAR_VERITABANI, "r") as f:
        pazar_data = json.load(f)

    if not pazar_data:
        await ctx.send('Pazarda henüz ürün bulunmuyor.')
        return

    pazar_listesi = "\n".join([f'{ctx.guild.get_member(int(user_id)).display_name}: {veri["urun"]} - {veri["fiyat"]} TL' for user_id, veri in pazar_data.items()])
    await ctx.send(f'Pazardaki Ürünler:\n{pazar_listesi}')


@bot.command(name='satınal', help='Pazardan belirtilen ürünü satın alır.')
async def urun_satin_al(ctx, urun: str):
    user_id = str(ctx.author.id)

    
    with open(PAZAR_VERITABANI, "r") as f:
        pazar_data = json.load(f)

    
    if user_id not in pazar_data:
        await ctx.send('Pazarda satın alabileceğiniz bir ürün bulunmuyor.')
        return

    
    satici_id = user_id
    satici_veri = pazar_data.pop(satici_id)
    fiyat = satici_veri["fiyat"]

   
    with open(BAKIYE_VERITABANI, "r") as f:
        economy_data = json.load(f)
        bakiye = economy_data.get(user_id, 0)

    if bakiye < fiyat:
        await ctx.send('Yetersiz bakiye. Ürün satın alınamadı.')
        return

    
    economy_data[user_id] -= fiyat

    
    economy_data[satici_id] = economy_data.get(satici_id, 0) + fiyat

   
    with open(BAKIYE_VERITABANI, "w") as f:
        json.dump(economy_data, f)

    with open(PAZAR_VERITABANI, "w") as f:
        json.dump(pazar_data, f)

    
    satici = ctx.guild.get_member(int(satici_id))
    await satici.send(f'{ctx.author.display_name} tarafından {urun} satın alındı! {fiyat} TL hesabınıza eklendi.')

    await ctx.send(f'{ctx.author.mention} Başarıyla {satici.display_name} kullanıcısından {urun} satın aldınız. {fiyat} TL ödeme yapıldı.')


@bot.command(name='avatar', help='Belirtilen kullanıcının avatarını paylaşır.')
async def avatar(ctx, kullanici: discord.Member = None):
    
    if kullanici is None:
        kullanici = ctx.author
    avatar_url = kullanici.avatar.url

    response = requests.get(avatar_url)
    
    avatar_bytes = BytesIO(response.content)

    await ctx.send(f"**{kullanici.display_name}**'ın avatarı:", file=discord.File(avatar_bytes, f"{kullanici.id}_avatar-evolvex.png"))


def load_database():
    global tickets, support_role_id
    try:
        with open(database_file, 'r') as file:
            data = json.load(file)
            tickets = data.get('tickets', {})
            support_role_id = data.get('support_role_id', None)
    except FileNotFoundError:
        pass

def save_database():
    data = {'tickets': tickets, 'support_role_id': support_role_id}
    with open(database_file, 'w') as file:
        json.dump(data, file, indent=2)

@bot.event
async def on_ready():
    if not os.path.exists(database_file):
        with open(database_file, 'w') as file:
            json.dump({'tickets': {}, 'support_role_id': None}, file, indent=2)
    load_database()

@bot.command(name="ticketrol", help='Ticket rolünü ayarlar.')
async def ticketdestek(ctx, role: discord.Role):
    global support_role_id
    support_role_id = role.id
    save_database()
    await ctx.send(f"Destek ekibi rolü {role.mention} olarak ayarlandı.")

@bot.command(name="ticket", help='Ticket kanalı ayarlar.')
async def ticket(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send("Lütfen bir kanal etiketleyin. Örnek: `{prefix}ticket #kanal`")
        return

    embed = discord.Embed(title="Ticket Oluştur", description="Ticket açmak için reaksiyon ekleyin.", color=0x3498db)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1172196055018909718/1202223872309727272/image.png?ex=65ccad3b&is=65ba383b&hm=aff14e0899b1baecb43565bdce5a5cbc3a7dab31a624849632ce0d1e7f94b189")
    message = await channel.send(embed=embed)

    await message.add_reaction("🎫")  

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.emoji == "🎫":   
        overwrites = {
            reaction.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            reaction.message.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_id = len(tickets) + 1

        ticket_channel = await reaction.message.guild.create_text_channel(f'ticket-{ticket_id}-{user.display_name}', overwrites=overwrites)
        tickets[ticket_id] = {'channel_id': ticket_channel.id, 'author_id': user.id, 'status': 'Open'}
        save_database()

        embed = discord.Embed(title="Ticket Oluşturuldu", description="Sorunlarınızı buradan bildirebilirsiniz.", color=0x00ff00)
        await ticket_channel.send(embed=embed)

@bot.command(name="ticketkapat", help='Ticket kanalını kapatır.')
async def kapat(ctx):
    if ctx.channel.id in [ticket['channel_id'] for ticket in tickets.values()]:
        ticket_id = [key for key, value in tickets.items() if value['channel_id'] == ctx.channel.id][0]

        if ctx.author.id == tickets[ticket_id]['author_id']:
            await ctx.send("Ticket kapatılıyor...", delete_after=5)
            await ctx.channel.delete()
            del tickets[ticket_id]
            save_database()
        elif support_role_id and discord.utils.get(ctx.author.roles, id=support_role_id):
            await ctx.send("Destek ekibi tarafından ticket kapatılıyor...", delete_after=5)
            await ctx.channel.delete()
            del tickets[ticket_id]
            save_database()
    else:
        await ctx.send("Bu komut sadece bir ticket kanalında kullanılabilir.")

@bot.event
async def on_message(message):
    if not message.author.bot:
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)

        if guild_id in rank_data:
            
            user_level = rank_data[guild_id].get(user_id, DEFAULT_LEVEL)
            
            user_xp = rank_data[guild_id].get(f'{user_id}_xp', DEFAULT_XP)

            
            user_xp += 1

            
            if user_xp >= user_level * 10:
                user_level += 1
                await message.channel.send(f'{message.author.mention} seviye atladı! Yeni seviyesi: {user_level}')

            
            rank_data[guild_id][user_id] = user_level
            rank_data[guild_id][f'{user_id}_xp'] = user_xp

            
            with open(RANK_FILE, 'w') as f:
                json.dump(rank_data, f)

    await bot.process_commands(message)

try:
    with open(RANK_FILE, 'r') as f:
        rank_data = json.load(f)
except FileNotFoundError:
    pass  

@bot.command(name="levelsys", help='Level sistemini açar/kapatır.')
async def level(ctx, arg):
    if arg.lower() == 'aç':
        rank_data[str(ctx.guild.id)] = {}
        await ctx.send('Level sistemi açıldı!')
    elif arg.lower() == 'kapat':
        if str(ctx.guild.id) in rank_data:
            del rank_data[str(ctx.guild.id)]
            await ctx.send('Level sistemi kapatıldı!')
        else:
            await ctx.send('Level sistemi zaten kapalı!')
    else:
        await ctx.send('Geçersiz komut. `aç` veya `kapat` yazın.')

@bot.command(name="rank", help='Levelinizi görüntüler.')
async def level(ctx):
    guild_id = str(ctx.guild.id)
    if guild_id in rank_data:
        await ctx.send(f'*Level*: **{rank_data[guild_id].get(str(ctx.author.id), DEFAULT_LEVEL)}**')
    else:
        await ctx.send('Level sistemi bu sunucuda kapalı!')

@bot.command(name="level", help='Levelinizi görüntüler.')
async def level(ctx):
    guild_id = str(ctx.guild.id)
    if guild_id in rank_data:
        await ctx.send(f'*Level*: **{rank_data[guild_id].get(str(ctx.author.id), DEFAULT_LEVEL)}**')
    else:
        await ctx.send('Level sistemi bu sunucuda kapalı!')

@bot.command(name='profil', help='Profil bilgilerinizi gösterir.')
async def profil(ctx):
    user = ctx.author


    username = user.name
    user_id = user.id

    
    roles = [role.name for role in user.roles]

    

    
    account_created_at = user.created_at.strftime('%Y-%m-%d %H:%M:%S')

    
    joined_at = user.joined_at.strftime('%Y-%m-%d %H:%M:%S')

    
    await ctx.send(f"**Profil Bilgileri**\n"
                   f"Kullanıcı Adı: {username}\n"
                   f"Kullanıcı ID: {user_id}\n"
                   f"Hesap Oluşturulma Tarihi: {account_created_at}\n"
                   f"Sunucuya Katılma Tarihi: {joined_at}")



def save_antiraid_data():
    with open(ANTIRAID_FILE, 'w') as f:
        json.dump(antiraid_data, f)


def load_antiraid_data():
    try:
        with open(antiraid_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


antiraid_data = load_antiraid_data()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    with open(afk_file, "r") as f:
        afk_data = json.load(f)

    if message.mentions:
        for member in message.mentions:
            if str(member.id) in afk_data:
                afk_info = afk_data[str(member.id)]
                await message.channel.send(f"**{member.display_name}** {afk_info['reason']} sebebi ile {afk_info['time']} zamandır afk.")
    if str(message.author.id) in afk_data:
        del afk_data[str(message.author.id)]
        with open(afk_file, "w") as f:
            json.dump(afk_data, f, indent=4)
        await message.channel.send(f"**{message.author.display_name}**, artık afk modundan çıktınız.")

    await bot.process_commands(message)

    if str(message.author.id) in afk_data:
        del afk_data[str(message.author.id)]
        with open(afk_file, "w") as f:
            json.dump(afk_data, f, indent=4)

    await bot.process_commands(message)

@bot.command(name="afk", help='Afk modunu açar/kapatır.')
async def afk(ctx, *, reason: str):
    with open(afk_file, "r") as f:
        afk_data = json.load(f)

    afk_data[str(ctx.author.id)] = {"reason": reason, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


    with open(afk_file, "w") as f:
        json.dump(afk_data, f, indent=4)

    await ctx.send(f"**{ctx.author.display_name}**, artık afk modundasın. Sebep: {reason}")


plastik_el_isleri = [
    "Boş plastik şişeleri dekoratif vazolara dönüştürün.",
    "Plastik kaşıklarla birlikte rengarenk bir çiçek saksısı yapın.",
    "Eski plastik bardakları keyifli mumluklar haline getirin.",
    "Plastik atıkları kullanarak renkli bir duvar sanatı oluşturun.",
    "Plastik şişelerden şeffaf bir lamba gölgesi yapın.",
    "Eski plastik tabakları rengarenk birer masa altlığına dönüştürün."
]



@bot.command(name="plastikelisleri")
async def on_message(message):
    
    fikir = random.choice(plastik_el_isleri)
    await message.channel.send(f"İşte promt : {fikir}")

@bot.command(name="capsengel", help='Caps-Engel açar/kapatır.')
async def capsengel(ctx, option: str):
    global caps_filter_enabled
    if option.lower() == "aç":
        caps_filter_enabled = True
        await ctx.send("Caps engelleme sistemi başarıyla açıldı.")
    elif option.lower() == "kapat":
        caps_filter_enabled = False
        await ctx.send("Caps engelleme sistemi başarıyla kapatıldı.")
    else:
        await ctx.send("Geçersiz seçenek. Lütfen 'aç' veya 'kapat' seçeneklerinden birini kullanın.")


@bot.event
async def on_message(message):
    if message.author.bot:
        return  

    
    if caps_filter_enabled and contains_caps(message.content):
        author_id = str(message.author.id)
        warnings[author_id] = warnings.get(author_id, 0) + 1  

        
        if warnings[author_id] >= 10:
            await message.author.add_roles(discord.utils.get(message.guild.roles, name="Muted"))
            await message.channel.send(f"{message.author.mention} 10 kere büyük harf kullanımı yaptığı için susturuldu.")

        save_warnings()  
    await bot.process_commands(message)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="EvolveX"))

@bot.event
async def on_member_join(member):
    await check_action('member_join', member)

@bot.event
async def on_member_remove(member):
    await check_action('member_remove', member)

@bot.event
async def on_guild_channel_delete(channel):
    await check_action('channel_delete', channel)

@bot.event
async def on_guild_channel_create(channel):
    await check_action('channel_create', channel)

@bot.event
async def on_guild_role_create(role):
    await check_action('role_create', role)

@bot.event
async def on_guild_role_delete(role):
    await check_action('role_delete', role)

async def check_action(action, obj):
    with open('antiraidsys.json', 'r') as file:
        antiraid_settings = json.load(file)
    
    server_id = str(obj.guild.id)
    if server_id in antiraid_settings and antiraid_settings[server_id]['enabled']:
        now = datetime.now()
        if 'last_action_time' in antiraid_settings[server_id]:
            last_action_time = datetime.fromisoformat(antiraid_settings[server_id]['last_action_time'])
            diff = now - last_action_time
            if diff.seconds < antiraid_settings[server_id]['cooldown']:
                antiraid_settings[server_id]['action_count'] += 1
            else:
                antiraid_settings[server_id]['action_count'] = 1
        else:
            antiraid_settings[server_id]['action_count'] = 1
        
        antiraid_settings[server_id]['last_action_time'] = now.isoformat()

        if antiraid_settings[server_id]['action_count'] >= antiraid_settings[server_id]['threshold']:
            guild = obj.guild
            if action in ['member_join', 'member_remove']:
                user = obj
                if action == 'member_join':
                    action_str = 'üye katılma'
                else:
                    action_str = 'üye ayrılma'
                await guild.owner.send(f"Dikkat! Kurucusu olduğunuz **{guild.name}** sunucusunda **{action_str}** eylemi belirlenen süre içinde birden fazla kez yaşandı! Lütfen kontrol edin.")
            elif action in ['channel_delete', 'channel_create']:
                channel = obj
                if action == 'channel_delete':
                    action_str = 'kanal silme'
                else:
                    action_str = 'kanal oluşturma'
                await guild.owner.send(f"Dikkat! Kurucusu olduğunuz **{guild.name}** sunucusunda **{action_str}** eylemi belirlenen süre içinde birden fazla kez kullanıldı! Lütfen kontrol edin.")
            elif action in ['role_create', 'role_delete']:
                role = obj
                if action == 'role_create':
                    action_str = 'rol oluşturma'
                else:
                    action_str = 'rol silme'
                await guild.owner.send(f"Dikkat! Kurucusu olduğunuz **{guild.name}** sunucusunda **{action_str}** eylemi belirlenen süre içinde birden fazla kez kullanıldı! Lütfen kontrol edin.")
            antiraid_settings[server_id]['action_count'] = 0

        with open('antiraidsys.json', 'w') as file:
            json.dump(antiraid_settings, file)

@bot.command(name="antiraid", help='Anti-Raid sistemini açar/kapatır.')
async def antiraid(ctx, action: str = None, cooldown: int = None):
    if action is None:
        await ctx.send("Lütfen bir eylem belirtin (`on` veya `off`). Örneğin: `antiraid on 60`")
        return

    server_id = str(ctx.guild.id)
    with open('antiraidsys.json', 'r') as file:
        antiraid_settings = json.load(file)

    if action.lower() == "off":
        if server_id in antiraid_settings:
            antiraid_settings.pop(server_id)
            with open('antiraidsys.json', 'w') as file:
                json.dump(antiraid_settings, file)
            await ctx.send("Antiraid sistemi kapatıldı.")
        else:
            await ctx.send("Antiraid sistemi zaten kapalı.")
    elif action.lower() == "on":
        if cooldown is None:
            await ctx.send("Lütfen bir cooldown süresi belirtin.")
            return
        antiraid_settings[server_id] = {
            'enabled': True,
            'cooldown': cooldown,
            'threshold': 3,
            'action_count': 0
        }
        with open('antiraidsys.json', 'w') as file:
            json.dump(antiraid_settings, file)
        await ctx.send(f"Antiraid sistemi {cooldown} saniye olarak ayarlandı.")
    else:
        await ctx.send("Geçersiz eylem. Lütfen `on <saniye>` veya `off` olarak belirtin.")

@bot.command(name="setavatar", help='Owner özel komutudur.')
async def setavatar(ctx):
    attachment = ctx.message.attachments[0] if ctx.message.attachments else None
    if not attachment:
        await ctx.send("Lütfen bir dosya ekleyin!")
        return

    if not attachment.filename.endswith(('.gif', '.png', '.jpg', '.jpeg')):
        await ctx.send("Geçersiz dosya türü!")
        return

    response = requests.get(attachment.url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        await bot.user.edit(avatar=image_bytes.read())
        await ctx.send("Profil resmi güncellendi!")
    else:
        await ctx.send("Bir hata oluştu, lütfen daha sonra tekrar deneyin!")


bot.run(TOKEN)