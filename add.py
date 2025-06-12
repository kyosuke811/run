import discord
from discord.ext import commands
import asyncio
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# Discord Bot の初期設定
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents = intents
)

# 起動時に表示されるログ
@bot.event
async def on_ready():
    print(f"? Logged in as {bot.user} (ID:{bot.user.id})")


# -----------------------------
# チャンネル設定
# -----------------------------
CHANNEL_A_ID = 1382252044475170866 # 入力を受け付けるチャットチャンネル
CHANNEL_B_ID = 1381699284776390767 # 名前を変更する対象のチャンネル


# -----------------------------
# 部屋番号をチャンネル名に反映する関数
# -----------------------------
async def update_room_name(room_number: str):
    channel = bot.get_channel(CHANNEL_B_ID)

    if channel is None:
        print("? チャンネルが見つかりません")
        return

    await channel.send(room_number)
    pattern = r'\d{5}' # 5桁の数字を検索
    new_name = re.sub(pattern,room_number,channel.name) # 名前中の5桁を置換

    await channel.edit(name = new_name)


# -----------------------------
# メッセージ受信時の処理
# -----------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_A_ID:
        return
    if message.content.isdigit() and len(message.content)== 5:
        await  update_room_name(message.content)
    await bot.process_commands(message)


# -----------------------------
# リマインダー機能
# 使用例: !remind 2025:06:12:18:30 メッセージ内容
# -----------------------------
@bot.command()
async def remind(ctx,timestring:str,*,message:str):
    parts = timestring.split(":")
    year,month,day,hour,minute = map(int,parts)
    t = datetime(year,month,day,hour,minute)
    now = datetime.now()
    if t <= now:
        await ctx.send("過去の時刻です")
        return 
    else:
        await ctx.send(f"リマインダーを設定しました")

    delay_seconds = (t - now).total_seconds()
    asyncio.create_task(remind_later(ctx.channel, delay_seconds, message))

# 非同期で指定時間後にメッセージ送信
async def remind_later(channel,delay,message):
    await asyncio.sleep(delay)
    await channel.send(message)
    
# --------------------------------------------------
# 以下は以前の Excelファイル読み込みの検索処理（未使用）
# --------------------------------------------------
# @bot.command()
# async def serch(ctx, word: str):
#     workbook = openpyxl.load_workbook("spreadsheet.xlsx")
#     sheet = workbook.active
#     for row in sheet.iter_rows():
#         for cell in row:
#             if str(cell.value) == word:
#                 row_num = cell.row
#                 col_num = cell.column
#                 row_header = sheet.cell(row=row_num, column=1).value
#                 col_header = sheet.cell(row=2, column=col_num).value
#                 await ctx.send(f"? 見つかりました！\n行: {row_header}\n列: {col_header}")
#                 return

# -----------------------------
# Google Sheets 認証と取得
# -----------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "/home/ec2-user/discordbot1-462615-88e7eb0f2472.json"



# 認証情報を取得
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

# 認証してGoogle Sheets APIクライアントを生成
gc = gspread.authorize(credentials)


# 対象のスプレッドシートを取得（URL指定）
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1vfTOKrwKWdjhWegG286UrOAxvLboMzTe8wxEhJ36TUo/edit?usp=sharing")
sheet = spreadsheet.sheet1  # 最初のシート

# -----------------------------
# スプレッドシート検索コマンド
# 使用例: !serch value
# -----------------------------
@bot.command()
async def serch(ctx, word: str):
    values = sheet.get_all_values()  # 全体データを2次元配列で取得
    n = 0    # ? 件数カウンターの初期化
    found = False

    for r, row in enumerate(values):
        for c, cell in enumerate(row):
            if cell == word:
                # 第4列のスコア値と第2行の編成割合を取得
                row_header = values[r][3] if len(row) > 0 else "不明"
                col_header = values[1][c] if len(values) > 1 else "不明"  # 2行目（index=1）
                await ctx.send(f"? 見つかりました！\n スコア範囲:{int(row_header)-19999}～ {row_header}pt\n 編成: {col_header}%")
                found = True
                n += 1
                if n >= 10:
                    return
    if not found:
        await ctx.send("? 見つかりませんでした")

# -----------------------------
# Bot起動
# -----------------------------
bot.run('DISCORD_TOKEN')