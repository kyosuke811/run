
# Discord Bot - チャンネル名更新・リマインダー・スプレッドシート検索

このDiscord Botは以下の3つの機能を持っています：

1. **部屋番号のチャンネル名更新**
2. **時間指定によるリマインダー通知**
3. **Googleスプレッドシートからの値検索**

## 🔧 使用技術

- Python 3.10+
- discord.py
- asyncio
- re（正規表現）
- datetime
- gspread（Google Sheets API）
- google-auth（認証）

## 📦 インストール

必要なパッケージをインストール：

```bash
pip install discord.py gspread google-auth
````

## 🗂 構成ファイル

* `main.py`（このBotの全体コード）
* `credentials.json`（Google Service Account の秘密鍵ファイル）
* `.env`（セキュリティのためにDiscordのトークンを管理）

## 🚀 起動方法

```bash
python main.py
```

または `.env` ファイルを使う場合：

```bash
DISCORD_TOKEN=あなたのトークン
```

## ✨ 各機能の説明

### 1. 部屋番号をチャンネル名に反映

* **監視対象チャンネル（CHANNEL\_A\_ID）** に5桁の数字を投稿すると、
* **別のチャンネル（CHANNEL\_B\_ID）** の名前中の5桁の数字が自動で置き換わります。

### 2. リマインダー機能

```text
!remind YYYY:MM:DD:HH:MM メッセージ内容
```

指定した日時になったら、Botがメッセージ内容を送信します。

例：

```text
!remind 2025:06:14:20:00 イベント開始です！
```

### 3. Googleスプレッドシート検索

```text
!serch 検索語
```

* スプレッドシート全体から一致する値を検索
* スコア範囲（行ヘッダー）や編成（列ヘッダー）を表示
* 最大10件まで表示

## 📄 スプレッドシート設定

* URLで指定されたスプレッドシートを読み込む
* 事前にService Accountに閲覧権限を付与してください


## 📝 作者

* GitHub: [kyosuke811](https://github.com/kyosuke811)
