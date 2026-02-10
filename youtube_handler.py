"""
YouTube bilan ishlash uchun funksiyalar
"""
import os
import yt_dlp
from typing import List, Dict, Optional, Callable
from config import YT_DLP_OPTIONS, MAX_FILE_SIZE_BYTES, DOWNLOAD_DIR
from utils import logger, ensure_directory, get_file_size, sanitize_filename, cleanup_file


class YouTubeHandler:
    """YouTube videolarni yuklab olish va MP3 ga konvertatsiya qilish"""
    
    def __init__(self):
        ensure_directory(DOWNLOAD_DIR)
        self.current_download = None
    
    def get_playlist_info(self, url: str) -> Optional[Dict]:
        """
        Playlist yoki video haqida ma'lumot olish
        """
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': 'in_playlist',
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Agar bitta video bo'lsa
                if 'entries' not in info:
                    return {
                        'type': 'video',
                        'title': info.get('title', 'Unknown'),
                        'count': 1,
                        'videos': [{'title': info.get('title'), 'url': url}]
                    }
                
                # Agar playlist bo'lsa
                videos = []
                for entry in info['entries']:
                    if entry:
                        videos.append({
                            'title': entry.get('title', 'Unknown'),
                            'url': entry.get('url') or entry.get('webpage_url') or f"https://youtube.com/watch?v={entry.get('id')}"
                        })
                
                return {
                    'type': 'playlist',
                    'title': info.get('title', 'Unknown Playlist'),
                    'count': len(videos),
                    'videos': videos
                }
        
        except Exception as e:
            logger.error(f"Playlist ma'lumotlarini olishda xatolik: {e}")
            return None
    
    def download_and_convert(
        self, 
        url: str, 
        progress_callback: Optional[Callable] = None
    ) -> Optional[str]:
        """
        Videoni yuklab olish va MP3 ga konvertatsiya qilish
        
        Returns:
            MP3 fayl yo'li yoki None (xatolik bo'lsa)
        """
        try:
            # Progress hook
            def progress_hook(d):
                if d['status'] == 'downloading' and progress_callback:
                    progress_callback('downloading', d)
                elif d['status'] == 'finished' and progress_callback:
                    progress_callback('converting', d)
            
            # yt-dlp sozlamalari
            ydl_opts = YT_DLP_OPTIONS.copy()
            ydl_opts['progress_hooks'] = [progress_hook]
            
            # Video ma'lumotlarini olish (fayl nomi uchun)
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'audio')
            
            # Fayl nomini tozalash
            safe_title = sanitize_filename(video_title)
            output_path = os.path.join(DOWNLOAD_DIR, f"{safe_title}.mp3")
            
            # Agar fayl allaqachon mavjud bo'lsa, o'chirish
            if os.path.exists(output_path):
                cleanup_file(output_path)
            
            # Yuklab olish va konvertatsiya qilish
            ydl_opts['outtmpl'] = os.path.join(DOWNLOAD_DIR, f"{safe_title}.%(ext)s")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # MP3 faylni tekshirish
            if not os.path.exists(output_path):
                logger.error(f"MP3 fayl topilmadi: {output_path}")
                return None
            
            # Fayl hajmini tekshirish
            file_size = get_file_size(output_path)
            if file_size > MAX_FILE_SIZE_BYTES:
                logger.warning(f"Fayl juda katta: {file_size} bytes")
                cleanup_file(output_path)
                return None
            
            logger.info(f"Muvaffaqiyatli yuklab olindi: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Yuklab olishda xatolik: {e}")
            return None
    
    def download_playlist(
        self,
        url: str,
        progress_callback: Optional[Callable] = None
    ) -> List[str]:
        """
        Playlist'dagi barcha audiolarni yuklab olish
        
        Returns:
            MP3 fayllar ro'yxati
        """
        downloaded_files = []
        
        try:
            # Playlist ma'lumotlarini olish
            playlist_info = self.get_playlist_info(url)
            
            if not playlist_info or not playlist_info['videos']:
                logger.error("Playlist bo'sh yoki topilmadi")
                return downloaded_files
            
            total_videos = len(playlist_info['videos'])
            logger.info(f"Jami {total_videos} ta video topildi")
            
            # Har bir videoni yuklab olish
            for index, video in enumerate(playlist_info['videos'], 1):
                video_url = video['url']
                video_title = video['title']
                
                logger.info(f"[{index}/{total_videos}] Yuklab olinmoqda: {video_title}")
                
                if progress_callback:
                    progress_callback('video_start', {
                        'index': index,
                        'total': total_videos,
                        'title': video_title
                    })
                
                # Yuklab olish
                file_path = self.download_and_convert(video_url, progress_callback)
                
                if file_path:
                    downloaded_files.append(file_path)
                    logger.info(f"✓ Tayyor: {video_title}")
                else:
                    logger.warning(f"✗ Yuklab olinmadi: {video_title}")
            
            logger.info(f"Jami yuklab olindi: {len(downloaded_files)}/{total_videos}")
            return downloaded_files
        
        except Exception as e:
            logger.error(f"Playlist yuklab olishda xatolik: {e}")
            return downloaded_files
