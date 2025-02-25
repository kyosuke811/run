import discord
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_A_ID = 1229641594722975754  # チャンネルAのID
CHANNEL_B_ID = 1229546386685427732  # チャンネルBのID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # チャンネルAからのメッセージが5桁の数字の場合
    if message.channel.id == CHANNEL_A_ID and message.content.isdigit() and len(message.content) == 5:
        
        # チャンネルBにメッセージを送信
        channel_b = bot.get_channel(CHANNEL_B_ID)
        if channel_b:
            await channel_b.send(message.content)  # チャンネルAのメッセージをチャンネルBに送信
        
        # チャンネルBを取得し、チャンネル名を変更
        if channel_b:
            # 【】内の数字を受信した5桁の数字に変更
            modified_message = re.sub(r'【\d{5}】', f'【{message.content}】', channel_b.name)

            # チャンネル名を変更（Botに適切な権限が必要）
            await channel_b.edit(name=modified_message)
            print(f'チャンネル名を変更しました: {modified_message}')
    
    # コマンド処理を適切に行う（コマンドがあればここで処理）
    await bot.process_commands(message)

bot.run('MTI0NDUwNzI2MzcyMTQxMDYzMA.Gze9xn.vHfdguuwnhzb2ejGxIEOQmo_xzKf9NL_uvn3RE')  # Botのトークンを入力
