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
        'preferredquality': '128',  # 192 dan 128 ga tushirildi (tezlik uchun)
    }],
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'quiet': True,
    'no_warnings': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    # FFmpeg uchun tezlikni oshirish
    'postprocessor_args': [
        '-threads', '4',
        '-preset', 'ultrafast'
    ],
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
    'file_too_large': "❌ Fayl juda katta ({} MB). Telegram orqali faqat 50 MB gacha fayllarni yuborish mumkin.",
    'error': "❌ Xatolik yuz berdi: {}",
    'no_videos': "❌ Playlist bo'sh yoki videolar topilmadi.",
    'age_restricted': "🔞 Bu video yosh chekloviga ega yoki avtorizatsiya talab qiladi.",
    'not_available': "🚫 Bu video endi mavjud emas (o'chirilgan yoki yopiq).",
    'copyright_error': "⚖️ Mualliflik huquqi tufayli bu videoni yuklab bo'lmadi.",
    'download_failed': "📥 Yuklab olishda xatolik yuz berdi. YouTube cheklovlari bo'lishi mumkin.",
    'conversion_failed': "🔄 MP3 formatga o'tkazishda xatolik yuz berdi.",
}
