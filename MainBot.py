#!/usr/bin/env python3
# coding: UTF-8
# ライブラリのインポート
import sys
import random
import discord
from discord.ext import commands
from discord import app_commands

#TOKENを設定
TOKEN = 'TOKENを入力してください'
#チャンネルIDを設定
CHANNEL_ID = 1234567890    #あそびばチャンネル
CHANNEL_ID2 = 2345678901   #実験用チャンネル
#鯖管理人のユーザーIDを設定
user_id = '123456781237890'

# 初期化・インスタンス作成
intents = discord.Intents.all()
intents.reactions = True
intents.messages = True
intents.guilds = True
# discord.py Ver2.0 以降は必要
intents.message_content = True
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

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
    if message.channel.id == CHANNEL_ID2:
        if message.attachments:
            for attachment in message.attachments:
                if 'スピカちゃん' in message.content:
                    string = 'スピカ'
                if 'ミラちゃん' in message.content:
                    string = 'ミラ'
                if 'ユウちゃん' in message.content:
                    string = 'ユウ'
                if 'リルちゃん' in message.content:
                    string = 'リル'
                if 'ミルちゃん' in message.content:
                    string = 'ミル'
                if 'ティナちゃん' in message.content:
                    string = 'ティナ'
                if 'レイちゃん' in message.content:
                    string = 'レイ'
                if 'リリカちゃん' in message.content:
                    string = 'リリカ'
                if 'になちゃん' in message.content:
                    string = 'にな'
                await message.channel.send(f'アバター名:{string}ちゃん\n')
                await message.channel.send(attachment.url)
                print(f'メッセージ内容: {message.content.strip().replace(" ","")}\n')
                print(f'アバター名:{string}')
                print(attachment.url)
                #if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                #    await message.channel.send(f'{attachment.url}')
                #    print('画像が検出されました')
                #    print(attachment.url)
    ##########################################################################################################

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
    await tree.sync()

# Discord Botを実行
client.run(TOKEN)