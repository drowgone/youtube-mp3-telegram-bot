# 🎵 YouTube MP3 Telegram Bot

YouTube playlist'laridan audiolarni yuklab olib, MP3 formatda Telegram orqali yubora oladigan bot.

## ✨ Xususiyatlar

- ✅ YouTube playlist'larni qo'llab-quvvatlaydi
- ✅ Yakka videolarni ham yuklab oladi
- ✅ Avtomatik MP3 formatga konvertatsiya qiladi
- ✅ 50MB gacha fayllarni yuboradi
- ✅ Yuklanish jarayonini ko'rsatadi
- ✅ Xatolarni boshqaradi

## 🚀 O'rnatish

### 1. Repozitoriyani clone qiling
```bash
git clone https://github.com/drowgone/youtube-mp3-telegram-bot.git
```

### 2. Virtual environment yarating

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# yoki
venv\Scripts\activate  # Windows
```

### 3. Dependencies o'rnating

```bash
pip install -r requirements.txt
```

### 4. FFmpeg o'rnating (agar o'rnatilmagan bo'lsa)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**MacOS:**
```bash
brew install ffmpeg
```

**Windows:**
FFmpeg saytidan yuklab oling: https://ffmpeg.org/download.html

### 5. Telegram Bot yarating

1. Telegram'da [@BotFather](https://t.me/BotFather) ni oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ini kiriting
4. Bot tokenini saqlang

### 6. Environment sozlash

`.env` faylini yarating:

```bash
cp .env.example .env
```

`.env` faylida bot tokenini kiriting:

```env
TELEGRAM_BOT_TOKEN=sizning_bot_tokeningiz
MAX_FILE_SIZE_MB=50
DOWNLOAD_DIR=downloads
```

## 🎮 Ishlatish

### Botni ishga tushirish

```bash
python bot.py
```

### Bot commandalari

- `/start` - Botni ishga tushirish
- `/help` - Yordam

### Misol

1. Botni Telegram'da oching
2. `/start` ni bosing
3. YouTube playlist yoki video linkini yuboring:
   ```
   https://www.youtube.com/playlist?list=PLxxxxxx
   ```
4. Bot barcha audiolarni yuklab olib, sizga yuboradi!

## 📝 Texnik Cheklovlar

- **Maksimal fayl hajmi**: 50 MB (Telegram Bot API cheklovi)
- **Format**: MP3 (192 kbps)
- **Mualliflik huquqlari**: Faqat shaxsiy foydalanish uchun

## ⚠️ Ogohlantirishlar

> **Mualliflik Huquqlari**: YouTube'dan kontent yuklab olish YouTube Terms of Service'ni buzishi mumkin. Bu botdan faqat shaxsiy va ta'lim maqsadida foydalaning.

> **Xavfsizlik**: Bot tokenini hech qachon oshkor qilmang yoki GitHub'ga yuklamang!

## 🛠️ Texnologiyalar

- **Python** 3.8+
- **python-telegram-bot** - Telegram Bot API
- **yt-dlp** - YouTube yuklab olish
- **FFmpeg** - Audio konvertatsiya

## 📁 Loyiha Strukturasi

```
youtube-mp3-bot/
├── bot.py              # Asosiy bot
├── config.py           # Konfiguratsiya
├── youtube_handler.py  # YouTube handler
├── utils.py            # Yordamchi funksiyalar
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore          # Git ignore
└── downloads/          # Vaqtincha yuklamalar
```

## 🐛 Muammolarni hal qilish

### Bot ishga tushmayapti

1. Bot tokenini tekshiring (`.env` faylda)
2. Dependencies o'rnatilganligini tekshiring: `pip list`
3. FFmpeg o'rnatilganligini tekshiring: `ffmpeg -version`

### Video yuklab olinmayapti

1. URL to'g'riligini tekshiring
2. Internet ulanishini tekshiring
3. Video mavjudligini va ochiqligini tekshiring

### Fayl yuborilmayapti

1. Fayl hajmi 50 MB dan kichik ekanligini tekshiring
2. Bot loglarini ko'ring

## 📜 License

MIT License - Shaxsiy foydalanish uchun

## 🤝 Hissa qo'shish

Pull request'lar qabul qilinadi!

---

**Muallif**: Antigravity AI Assistant
**Versiya**: 1.0.0
**Sana**: 2026-02-10
