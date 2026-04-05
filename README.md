# HasLili Discord Bots

HasLili 多機器人專案，每個 bot 負責不同頻道與任務。

## 專案架構

```
haslili-bots/
├── README.md
├── shared/
│   ├── __init__.py
│   ├── utils.py            # 共用 Discord 發送函數
│   └── scheduler.py        # 排程模組
├── dd_bot/                 # 幣價播報（DD）
│   ├── bot.py
│   ├── config.example.py   # 設定範例，複製為 config.py 填入 Token
│   └── requirements.txt
├── gg_bot/                 # 每日問候（GG）
├── ryn_bot/                # 資安預警（Ryn）
└── rico_bot/               # 財經播報（Rico）
```

## Bot 說明

| Bot | 角色 | 功能 | 每日發送時間 |
|-----|------|------|------------|
| dd_bot | DD（幣價獵手） | BTC/ETH/SOL/BNB/S 價格 + 恐懼貪婪指數 | 20:00 |
| gg_bot | GG（社群牧羊人） | 每日問候、鼓勵語 | 09:00 |
| ryn_bot | Ryn（資安守門人） | The Hacker News 資安要聞 | 08:00 |
| rico_bot | Rico（現實策略師） | 美股/台股/匯率/大宗商品 | 07:30 |

## 啟動方式

```bash
# 安裝依賴
pip install -r dd_bot/requirements.txt

# 各 bot 獨立啟動（需要 4 個終端機視窗）
python dd_bot/bot.py
python gg_bot/bot.py
python ryn_bot/bot.py
python rico_bot/bot.py
```

## 設定方式

每個 bot 資料夾內有 `config.example.py`，複製並重命名為 `config.py`，填入：
- `DISCORD_TOKEN`：從 Discord Developer Portal 取得
- `CHANNEL_ID`：目標頻道的 ID（右鍵頻道 → 複製 ID）

> `config.py` 已加入 `.gitignore`，不會被推上 GitHub。
