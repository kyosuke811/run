import discord
from discord.ext import commands
import asyncio
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# Discord Bot �̏����ݒ�
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents = intents
)

# �N�����ɕ\������郍�O
@bot.event
async def on_ready():
    print(f"? Logged in as {bot.user} (ID:{bot.user.id})")


# -----------------------------
# �`�����l���ݒ�
# -----------------------------
CHANNEL_A_ID = 1382252044475170866 # ���͂��󂯕t����`���b�g�`�����l��
CHANNEL_B_ID = 1381699284776390767 # ���O��ύX����Ώۂ̃`�����l��


# -----------------------------
# �����ԍ����`�����l�����ɔ��f����֐�
# -----------------------------
async def update_room_name(room_number: str):
    channel = bot.get_channel(CHANNEL_B_ID)

    if channel is None:
        print("? �`�����l����������܂���")
        return

    await channel.send(room_number)
    pattern = r'\d{5}' # 5���̐���������
    new_name = re.sub(pattern,room_number,channel.name) # ���O����5����u��

    await channel.edit(name = new_name)


# -----------------------------
# ���b�Z�[�W��M���̏���
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
# ���}�C���_�[�@�\
# �g�p��: !remind 2025:06:12:18:30 ���b�Z�[�W���e
# -----------------------------
@bot.command()
async def remind(ctx,timestring:str,*,message:str):
    parts = timestring.split(":")
    year,month,day,hour,minute = map(int,parts)
    t = datetime(year,month,day,hour,minute)
    now = datetime.now()
    if t <= now:
        await ctx.send("�ߋ��̎����ł�")
        return 
    else:
        await ctx.send(f"���}�C���_�[��ݒ肵�܂���")

    delay_seconds = (t - now).total_seconds()
    asyncio.create_task(remind_later(ctx.channel, delay_seconds, message))

# �񓯊��Ŏw�莞�Ԍ�Ƀ��b�Z�[�W���M
async def remind_later(channel,delay,message):
    await asyncio.sleep(delay)
    await channel.send(message)
    
# --------------------------------------------------
# �ȉ��͈ȑO�� Excel�t�@�C���ǂݍ��݂̌��������i���g�p�j
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
#                 await ctx.send(f"? ������܂����I\n�s: {row_header}\n��: {col_header}")
#                 return

# -----------------------------
# Google Sheets �F�؂Ǝ擾
# -----------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "/home/ec2-user/discordbot1-462615-88e7eb0f2472.json"



# �F�؏����擾
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

# �F�؂���Google Sheets API�N���C�A���g�𐶐�
gc = gspread.authorize(credentials)


# �Ώۂ̃X�v���b�h�V�[�g���擾�iURL�w��j
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1vfTOKrwKWdjhWegG286UrOAxvLboMzTe8wxEhJ36TUo/edit?usp=sharing")
sheet = spreadsheet.sheet1  # �ŏ��̃V�[�g

# -----------------------------
# �X�v���b�h�V�[�g�����R�}���h
# �g�p��: !serch value
# -----------------------------
@bot.command()
async def serch(ctx, word: str):
    values = sheet.get_all_values()  # �S�̃f�[�^��2�����z��Ŏ擾
    n = 0    # ? �����J�E���^�[�̏�����
    found = False

    for r, row in enumerate(values):
        for c, cell in enumerate(row):
            if cell == word:
                # ��4��̃X�R�A�l�Ƒ�2�s�̕Ґ��������擾
                row_header = values[r][3] if len(row) > 0 else "�s��"
                col_header = values[1][c] if len(values) > 1 else "�s��"  # 2�s�ځiindex=1�j
                await ctx.send(f"? ������܂����I\n �X�R�A�͈�:{int(row_header)-19999}�` {row_header}pt\n �Ґ�: {col_header}%")
                found = True
                n += 1
                if n >= 10:
                    return
    if not found:
        await ctx.send("? ������܂���ł���")

# -----------------------------
# Bot�N��
# -----------------------------
bot.run('DISCORD_TOKEN')