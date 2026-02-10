"""
Yordamchi funksiyalar
"""
import os
import re
import logging
from pathlib import Path

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def is_valid_youtube_url(url: str) -> bool:
    """
    YouTube URL validatsiyasi
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=|playlist\?list=)?([^&=%\?]{11}|[^&=%\?]{34})'
    )
    return bool(re.match(youtube_regex, url))


def format_file_size(size_bytes: int) -> str:
    """
    Fayl hajmini formatlash (MB formatda)
    """
    size_mb = size_bytes / (1024 * 1024)
    return f"{size_mb:.2f}"


def get_file_size(filepath: str) -> int:
    """
    Fayl hajmini olish (baytlarda)
    """
    return os.path.getsize(filepath)


def cleanup_file(filepath: str) -> None:
    """
    Faylni o'chirish
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Fayl o'chirildi: {filepath}")
    except Exception as e:
        logger.error(f"Faylni o'chirishda xatolik: {e}")


def cleanup_directory(directory: str, keep_dir: bool = True) -> None:
    """
    Papkadagi barcha fayllarni o'chirish
    """
    try:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            if not keep_dir:
                os.rmdir(directory)
            
            logger.info(f"Papka tozalandi: {directory}")
    except Exception as e:
        logger.error(f"Papkani tozalashda xatolik: {e}")


def ensure_directory(directory: str) -> None:
    """
    Papka mavjudligini ta'minlash
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Fayl nomini tozalash (xavfsiz belgilar)
    """
    # Xavfli belgilarni olib tashlash
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Oxirgi va boshidagi bo'sh joylarni olib tashlash
    sanitized = sanitized.strip()
    # Agar fayl nomi bo'sh bo'lsa, default nom berish
    if not sanitized:
        sanitized = "audio"
    return sanitized
