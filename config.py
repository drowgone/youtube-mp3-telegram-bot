"""
Bot konfiguratsiyasi va sozlamalar
"""
import os
from dotenv import load_dotenv

# .env fayldan environment variables yuklash
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Maksimal fayl hajmi (baytlarda)
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Yuklab olish papkasi
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')

# yt-dlp sozlamalari
YT_DLP_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'quiet': False,
    'no_warnings': False,
}

# Bot xabarlari
MESSAGES = {
    'start': """
🎵 *YouTube MP3 Bot*

Salom! Men YouTube playlist'laridan audiolarni yuklab olaman va sizga MP3 formatda yuboraman.

*Qanday foydalanish:*
1. YouTube playlist linkini yuboring
2. Men barcha audiolarni yuklab olaman
3. Har birini MP3 formatda sizga yuboraman

*Cheklovlar:*
• Maksimal fayl hajmi: {max_size} MB
• Faqat audio yuklab olinadi

Playlist linkini yuboring! 🚀
""",
    'help': """
*Yordam*

Bu bot YouTube playlist'laridan audiolarni yuklab oladi.

*Qo'llab-quvvatlanadigan formatlar:*
• YouTube playlist URL
• YouTube video URL
• YouTube Music playlist

*Misol:*
`https://www.youtube.com/playlist?list=...`
`https://youtube.com/watch?v=...`

*Commandalar:*
/start - Botni ishga tushirish
/help - Yordam
""",
    'invalid_url': "❌ Noto'g'ri YouTube URL. Iltimos, to'g'ri playlist yoki video linkini yuboring.",
    'processing': "⏳ Qayta ishlanmoqda... Kuting.",
    'downloading': "📥 Yuklab olinmoqda: *{}*",
    'converting': "🔄 MP3 ga konvertatsiya qilinmoqda...",
    'sending': "📤 Yuborilmoqda...",
    'complete': "✅ Tayyor! Yana playlist yuborishingiz mumkin.",
    'file_too_large': "❌ Fayl juda katta ({} MB). Maksimal hajm: {} MB",
    'error': "❌ Xatolik yuz berdi: {}",
    'no_videos': "❌ Playlist bo'sh yoki videolar topilmadi.",
}
