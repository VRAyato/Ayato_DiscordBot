
# ライブラリのインポート
import discord
import random
#TOKENを設定
TOKEN = 'ここにDiscordBOTのTOKENを入力してください。'
#チャンネルIDを設定
CHANNEL_ID = 'ここにチャンネルIDを入力してください。'
# 初期化・インスタンス作成
intents = discord.Intents.all()
intents.reactions = True
intents.guilds = True
# discord.py Ver2.0 以降は必要
intents.message_content = True
client = discord.Client(intents = discord.Intents.default())

@client.event
async def on_ready():
    print('DiscordBOTにログインしました。')
    print(f'{client.user}')

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

    # 特定のチャンネルで発言した場合のみ反応する
    if message.channel.id == CHANNEL_ID:
        if "おみくじ" in message.content or "占い" in message.content or "うらない" in message.content:
            print('おみくじが引かれました')
            result = random.choice(message_unsei)
            await message.channel.send(f'あなたの運勢は....{result}です！')
        #######################################################

        # メンションにのみ反応する
        #if client.user.mentioned_in(message):
            #await message.reply(message.content)

# BOTをDiscordに接続
client.run(TOKEN)