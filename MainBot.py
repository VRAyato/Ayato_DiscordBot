#!/usr/bin/env python3
# coding: UTF-8
# ライブラリのインポート
import asyncio
import sys
import random
import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector
from mysql.connector import Error

#TOKENを設定
TOKEN = 'トークンを入力してください。'
#チャンネルIDを設定
CHANNEL_ID = 1234567890    #あそびばチャンネル
CHANNEL_ID2 = 1234567890   #実験用チャンネル
#鯖管理人のユーザーIDを設定
user_id = '1234567890'

# 初期化・インスタンス作成
intents = discord.Intents.all()
intents.reactions = True
intents.messages = True
intents.guilds = True
# discord.py Ver2.0 以降は必要
intents.message_content = True
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)
##########
reaction_history = {}
##########
# MySQL接続情報
MYSQL_HOST = 'HOST名を入力'
MYSQL_USER = 'ユーザー名を入力'
MYSQL_PASSWORD = 'パスワードを入力'
MYSQL_DATABASE = ' データベース名を入力'
###################################
###################################
# MySQL接続の作成
mysql_config = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE
}

#MySQL接続関数
def connect_mysql():
    global Connect_flag
    try:
        connection = mysql.connector.connect(**mysql_config)
        print("Connected to MySQL database")
        Connect_flag = "MySQLに接続しました。"
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        Connect_flag = "MySQLに接続できませんでした。"
        return None

#MySQLインサート関数
def insert_data():
    global avatar_id
    global avatar_name
    global avatar_url
    global mysql_flag
    try:
        connection = connect_mysql()
        if connection:
            connection.start_transaction()  #トランザクション開始
            cursor = connection.cursor()
            insert_query = "INSERT INTO image_tbl(image_url) VALUES (%s)"
            data = (avatar_url,)
            cursor.execute(insert_query, data)
            last_insert_id = cursor.lastrowid
            print("Last insert ID:", last_insert_id)
            # 中間テーブルへの挿入
            insert_query = "INSERT INTO avatar_image_tbl(avatar_id,image_id) VALUES (%s, %s)"
            data = (avatar_id, last_insert_id)
            cursor.execute(insert_query, data)
            # コミット
            connection.commit()
            print("Record inserted successfully")
            mysql_flag = "画像を登録しました。"
    except Error as e:
        print("Error while connecting to MySQL", e)
        mysql_flag = "MySQLに接続できませんでした。"
        if connection:
            # ロールバック
            connection.rollback()
            print("Transaction rolled back")
            mysql_flag = "MySQLでロールバックが発生しました。"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#MySQLセレクト関数
def select_deta():
    global avatar_list
    try:
        connection = connect_mysql()
        if connection:
            cursor = connection.cursor()
            select_query = "SELECT * FROM avatar_tbl;"
            cursor.execute(select_query) #実行
            avatar_list = [row[1] for row in cursor.fetchall()]
            print(avatar_list)
            return avatar_list
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
###########################################################################################################
# メッセージ関係
@client.event
async def on_message(message):
    # 自分自身には反応しない。
    if message.author == client.user:
        return
    # おみくじのリスト
    message_unsei = [
        '大吉',
        '吉',
        '中吉',
        '小吉',
        '半吉',
        '末吉',
        '末小吉',
        '凶',
        '大凶'
        ]
    yuu_image_list = [
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-01_18-58-53.137_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-01_18-59-27.831_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-01_19-00-28.347_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-01_19-01-25.273_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-09_00-34-38.819_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-09_00-38-32.209_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-20_02-16-04.353_2160x3840.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-20_02-16-26.910_2160x3840.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-20_02-18-16.742_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-20_02-19-11.835_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-20_02-25-16.176_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-28_23-43-48.517_2160x3840.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-03-30_02-30-12.558_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-04-04_00-20-04.821_3840x2160.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-04-04_00-21-21.692_2160x3840.png',
        'https://hub.ayatovr.jp/webdav/yuu/VRChat_2024-04-04_00-25-02.566_3840x2160.png'
    ]
    ##########################################################################################################
    # 以下はあそびばチャンネルでのみ反応する
    if message.channel.id == CHANNEL_ID:
        if "おみくじ" in message.content or "占い" in message.content or "うらない" in message.content:
            print('おみくじが引かれました')
            result = random.choice(message_unsei)
            await message.channel.send(f'あなたの運勢は....{result}です！')

        if "ユウちゃん" in message.content:
            print('ゆうが呼ばれました')
            yuu_result = random.choice(yuu_image_list)
            await message.channel.send(f'{yuu_result}')
    ##########################################################################################################
    # 以下は実験用チャンネルでのみ反応する（BOT管理権限がある人のみ利用）
    global avatar_id
    global avatar_name
    global avatar_url
    global mysql_flag
    if message.channel.id == CHANNEL_ID2:
        if message.attachments:
            for attachment in message.attachments:
                if 'スピカちゃん' in message.content:
                    string = 'スピカ'
                    avatar_name = 'スピカ'
                    avatar_id = 1
                elif 'ミラちゃん' in message.content:
                    string = 'ミラ'
                    avatar_id = 2
                elif 'ユウちゃん' in message.content:
                    string = 'ユウ'
                    avatar_name = 'ユウ'
                    avatar_id = 3
                elif 'リルちゃん' in message.content:
                    string = 'リル'
                    avatar_name = 'リル'
                    avatar_id = 4
                elif 'ミルちゃん' in message.content:
                    string = 'ミル'
                    avatar_name = 'ミル'
                    avatar_id = 5
                elif 'ティナちゃん' in message.content:
                    string = 'ティナ'
                    avatar_name = 'ティナ'
                    avatar_id = 6
                elif 'レイちゃん' in message.content:
                    string = 'レイ'
                    avatar_name = 'レイ'
                    avatar_id = 7
                elif 'リリカちゃん' in message.content:
                    string = 'リリカ'
                    avatar_name = 'リリカ'
                    avatar_id = 8
                elif 'になちゃん' in message.content:
                    string = 'にな'
                    avatar_name = 'にな'
                    avatar_id = 9
                elif 'ちゃやねこ' in message.content:
                    string = 'ちゃやねこ'
                    avatar_name = 'ちゃやねこ'
                    avatar_id = 0
                else:
                    string = '名前不明'
                ##########################################################################################################
                if string == '名前不明':
                    print('登録されたアバター以外の名前が検出されました')
                else:
                    await message.channel.send(f'アバター名:{string}ちゃん\n')
                    await message.channel.send(attachment.url)
                    print(f'メッセージ内容: {message.content.strip().replace(" ","")}\n')
                    print(f'アバター名:{string}')
                    print(attachment.url)
                    avatar_url = attachment.url
                    insert_data()
                    await message.channel.send(f'{mysql_flag}')
                #if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                #    await message.channel.send(f'{attachment.url}')
                #    print('画像が検出されました')
                #    print(attachment.url)
    ##########################################################################################################
    global avatar_list
    if "登録可能アバター"  in message.content:
        username = message.author.name
        print("Username:", username)
        select_deta()
        # MySQLから取得した要素を一つずつ出して格納する（リスト内包表記）最後に「ちゃん」を付ける
        result = 'ちゃん、'.join([item for item in avatar_list])
        result = result + 'ちゃん'
        await message.channel.send('登録可能アバターは以下の通りです')
        await message.channel.send(f'{result}')
    ##########################################################################################################
    # グローバル変数の定義
    global sent_message_id
    global author_message
    global reacted_message_id
        #戻り値の定義
    global count_rollback
    global r_sum
    # 変数の初期化
    count_rollback = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    r_sum = ''

    if "dice" in message.content:
        sent_message = await message.channel.send('サイコロを振る回数を選択してください。（1回、2回、3回）\n 1️⃣:1回 2️⃣:2回 3️⃣:3回')
        author_message = message.author
        await asyncio.sleep(1)
        # メッセージにリアクションをつける
        await sent_message.add_reaction('1️⃣')
        await sent_message.add_reaction('2️⃣')
        await sent_message.add_reaction('3️⃣')
        sent_message_id = sent_message.id
        await message.channel.send('https://cdn.discordapp.com/attachments/1230023086850572300/1234352822594830398/image.png?ex=66306c26&is=662f1aa6&hm=511d7678d1c6737bf8d8f28a930c8254ac838ab5b910f30548db07d10827be04&')
    ##########################################################################################################
# リアクション関係（リアクション追加/削除）
@client.event
async def on_reaction_add(reaction, user):
    # グローバル変数の定義
    global sent_message_id
    global author_message
    global reacted_message_id
    global dice_flag
    global count_123
    # 変数の初期化
    dice_flag = 0

    if user.bot:
        return
    #################################################
    if reaction.message.channel.id == CHANNEL_ID2:
        reacted_message_id = reaction.message.id
        if reacted_message_id == sent_message_id:
            if user.id == author_message.id:
                if author_message.display_name is not None:
                    nickname = author_message.display_name
                else:
                    nickname = author_message.name
                #####################################################
                if str(reaction.emoji) == '1️⃣' and dice_flag == 0:
                    dice_flag = 1
                    count_123 = 1
                    await reaction.message.clear_reactions()
                elif str(reaction.emoji) == '2️⃣' and dice_flag == 0:
                    dice_flag = 1
                    count_123 = 2
                    await reaction.message.clear_reactions()
                elif str(reaction.emoji) == '3️⃣' and dice_flag == 0:
                    dice_flag = 1
                    count_123 = 3
                    await reaction.message.clear_reactions()
                else:
                    await reaction.message.channel.send('同じメッセージにリアクションは2回以上できません。')
                ## リアクションが押されたら処理を実行(最後にフラグを初期化する)
                dice_count()
                if dice_flag == 1:
                    await reaction.message.channel.send(f'{count_back}します。')
                    for i in range(1, count_123+1):
                        await reaction.message.channel.send(f'{count_rollback[i]}')
                    await reaction.message.channel.send(f'{nickname}の{r_sum}')

@client.event
async def on_reaction_remove(reaction, user):
    # グローバル変数の定義
    global dice_flag
    global sent_message_id
    global reacted_message_id

    if user.bot:
        return
    if reaction.message.channel.id == CHANNEL_ID2:
        reacted_message_id = reaction.message.id
        if reacted_message_id == sent_message_id:
            if str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣':
                dice_flag = 2
                #await reaction.message.channel.send('リアクションが削除されました')

def dice_count():
    # サイコロの目のリスト
    dice_list = {
        "<:dice_01:1232580450816622622>":"1","<:dice_02:1232580479312723968>":"2","<:dice_03:1232580502054109185>":"3",
        "<:dice_04:1232580522375385178>":"4","<:dice_05:1232580554260480012>":"5","<:dice_06:1232580570907934772>":"6"
        }
    # グローバル変数の定義
    global dice_flag
    global dice_sum
        #戻り値の定義
    global count_back
    global count_rollback
    global r_sum
    # 変数の初期化
    count_rollback = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    count_back = ''
    r_sum = ''
    count_123
    dice_sum = 0
    dice_flag = 1

    if count_123 == 1:
        count_back = '1投'
    elif count_123 == 2:
        count_back = '2投'
    elif count_123 == 3:
        count_back = '3投'

    for i in range(1, count_123+1):
        dice1 = random.choice(list(dice_list.keys()))
        dice2 = random.choice(list(dice_list.keys()))
        dice3 = random.choice(list(dice_list.keys()))
        if dice1 == dice2 == dice3:
            kekka = '全部そろいました'
            if count_123 == 1:  #1投
                dice_sum += 20
            elif count_123 ==2:  #2投
                dice_sum += 30
            elif count_123 == 3:  #3投
                dice_sum += 60
        elif dice1 == dice2 or dice1 == dice3 or dice2 == dice3:
            kekka = '2つそろいました'
            if count_123 == 1:  #1投
                dice_sum += 30
            elif count_123 ==2:  #2投
                dice_sum += 15
            elif count_123 == 3:  #3投
                dice_sum += 10
        else:
            kekka = '揃いませんでした'
            if count_123 == 1:  #1投
                dice_sum += 6
            elif count_123 ==2:  #2投
                dice_sum += 3
            elif count_123 == 3:  #3投
                dice_sum += 2
        count_rollback[i] = (f'{dice1} {dice2} {dice3}')

    r_sum = (f'得点：{dice_sum}点')
    dice_sum = 2
    return count_back, count_rollback, r_sum
################################################################################################################################################################
#スラッシュコマンドの定義
@tree.command(name="hello",description="挨拶するコマンドです。")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!",ephemeral=False)   #ephemeral=True →「自分だけに表示するかどうか」の設定

@tree.command(name="testapp",description="これは実験用コマンドです。他の人には見えません！")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)

@tree.command(name="info",description="DiscordBOTの情報を表示するコマンドです。")
async def info_command(interaction: discord.Interaction):
    python_version = sys.version
    await interaction.response.send_message(f"当BOTは以下の構成で動いています。\n RaspberryPi 4B(4GB)\n UbuntuServer 22.04.4LTS\n Python {python_version}\n discord.py v2.3.2\n 問い合せ：<@{user_id}>",ephemeral=False)
################################################################################
# Discord Botが起動したときの処理
@client.event
async def on_ready():
    print('--------------------------------------------------')
    print('DiscordBOTにログインしました。')
    print(f'{client.user}')
    print(f'{client.user.name} has connected to Discord!')
    print('--------------------------------------------------')
    #起動したら実験用チャンネルに起動メッセージを送信する。
    global Connect_flag
    connect_mysql()
    #channel = client.get_channel(CHANNEL_ID2)
    #await channel.send('DiscordBOTが起動しました。')
    #await channel.send(Connect_flag)
    await tree.sync()

# Discord Botを実行
client.run(TOKEN)
