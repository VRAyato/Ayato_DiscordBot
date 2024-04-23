#!/usr/bin/env python3
# coding: UTF-8
# ライブラリのインポート
import sys
import random
import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector
from mysql.connector import Error

#TOKENを設定
TOKEN = 'トークンを設定してください。'
#チャンネルIDを設定
CHANNEL_ID = 1234567890987654321    #あそびばチャンネル
CHANNEL_ID2 = 1234567890987654321   #実験用チャンネル
#鯖管理人のユーザーIDを設定
user_id = '23456789012345678'

# 初期化・インスタンス作成
intents = discord.Intents.all()
intents.reactions = True
intents.messages = True
intents.guilds = True
# discord.py Ver2.0 以降は必要
intents.message_content = True
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

# MySQL接続情報
MYSQL_HOST = 'Host名を設定してください。'
MYSQL_USER = 'ユーザー名を設定してください。'
MYSQL_PASSWORD = 'パスワードを設定してください。'
MYSQL_DATABASE = ' データベース名を設定してください。'
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
        select_deta()
        # MySQLから取得した要素を一つずつ出して格納する（リスト内包表記）最後に「ちゃん」を付ける
        result = 'ちゃん、'.join([item for item in avatar_list])
        result = result + 'ちゃん'
        await message.channel.send('登録可能アバターは以下の通りです')
        await message.channel.send(f'{result}')

#スラッシュコマンドの定義
@tree.command(name="hello",description="挨拶するコマンドです。")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!",ephemeral=False)   #ephemeral=True →「自分だけに表示するかどうか」の設定

@tree.command(name="testapp",description="これは実験用コマンドです。他の人には見えません！")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)

@tree.command(name="info",description="DiscordBOTの情報を表示するコマンドです。")
async def test_command2(interaction: discord.Interaction):
    python_version = sys.version
    await interaction.response.send_message(f"当BOTは以下の構成で動いています。\n RaspberryPi 4B(4GB)\n UbuntuServer 22.04.4LTS\n Python {python_version}\n discord.py v2.3.2\n 問い合せ：<@{user_id}>",ephemeral=False)

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
    channel = client.get_channel(CHANNEL_ID2)
    await channel.send('DiscordBOTが起動しました。')
    await channel.send(Connect_flag)
    await tree.sync()

# Discord Botを実行
client.run(TOKEN)