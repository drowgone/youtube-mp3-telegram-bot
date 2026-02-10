"""
YouTube MP3 Telegram Bot
"""
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ParseMode, ChatAction

from config import BOT_TOKEN, MESSAGES, MAX_FILE_SIZE_MB
from youtube_handler import YouTubeHandler
from utils import (
    logger,
    is_valid_youtube_url,
    format_file_size,
    get_file_size,
    cleanup_file,
    cleanup_directory
)


class TelegramBot:
    """Telegram Bot asosiy klassi"""
    
    def __init__(self):
        if not BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN topilmadi! .env faylni tekshiring.")
        
        self.youtube_handler = YouTubeHandler()
        self.app = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlarni qo'shish
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /start command handler
        """
        message = MESSAGES['start'].format(max_size=MAX_FILE_SIZE_MB)
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /help command handler
        """
        await update.message.reply_text(
            MESSAGES['help'],
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Xabarlarni qayta ishlash (URL tekshirish va yuklab olish)
        """
        url = update.message.text.strip()
        user_id = update.effective_user.id
        
        # URL validatsiyasi
        if not is_valid_youtube_url(url):
            await update.message.reply_text(MESSAGES['invalid_url'])
            return
        
        # Processing xabari
        processing_msg = await update.message.reply_text(
            MESSAGES['processing'],
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            # "Typing..." ko'rsatish
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING
            )
            
            # Playlist/video ma'lumotlarini olish
            logger.info(f"User {user_id}: Playlist/video ma'lumotlari yuklanmoqda...")
            playlist_info = self.youtube_handler.get_playlist_info(url)
            
            if not playlist_info or not playlist_info.get('videos'):
                await processing_msg.edit_text(MESSAGES['no_videos'])
                return
            
            video_count = playlist_info['count']
            playlist_title = playlist_info['title']
            
            # Foydalanuvchiga ma'lumot berish
            info_text = f"📋 *{playlist_title}*\n\n"
            info_text += f"Jami: {video_count} ta audio\n"
            info_text += f"Yuklab olinmoqda... ⏳"
            
            await processing_msg.edit_text(info_text, parse_mode=ParseMode.MARKDOWN)
            
            # Har bir videoni yuklab olish va yuborish
            for index, video in enumerate(playlist_info['videos'], 1):
                video_url = video['url']
                video_title = video['title']
                
                # Yuklanayotgan videoni ko'rsatish
                status_text = f"📥 [{index}/{video_count}] {video_title[:50]}..."
                await processing_msg.edit_text(status_text, parse_mode=ParseMode.MARKDOWN)
                
                # "Upload audio" ko'rsatish
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id,
                    action=ChatAction.UPLOAD_VOICE
                )
                
                # Yuklab olish va konvertatsiya qilish
                file_path = self.youtube_handler.download_and_convert(video_url)
                
                if not file_path:
                    # Xatolik
                    error_text = f"❌ [{index}/{video_count}] {video_title[:50]}... - Yuklab olinmadi"
                    await update.message.reply_text(error_text)
                    continue
                
                # Fayl hajmini tekshirish
                file_size = get_file_size(file_path)
                file_size_mb = float(format_file_size(file_size))
                
                if file_size_mb > MAX_FILE_SIZE_MB:
                    # Fayl juda katta
                    warning_text = MESSAGES['file_too_large'].format(
                        file_size_mb,
                        MAX_FILE_SIZE_MB
                    )
                    await update.message.reply_text(warning_text)
                    cleanup_file(file_path)
                    continue
                
                # Faylni yuborish
                try:
                    with open(file_path, 'rb') as audio_file:
                        await update.message.reply_audio(
                            audio=audio_file,
                            title=video_title,
                            filename=f"{video_title}.mp3",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    
                    logger.info(f"✓ [{index}/{video_count}] Yuborildi: {video_title}")
                
                except Exception as e:
                    logger.error(f"Faylni yuborishda xatolik: {e}")
                    await update.message.reply_text(
                        f"❌ Yuborishda xatolik: {video_title[:50]}..."
                    )
                
                finally:
                    # Faylni o'chirish
                    cleanup_file(file_path)
            
            # Yakuniy xabar
            await processing_msg.edit_text(
                f"✅ Tayyor! {video_count} ta audio yuborildi.\n\nYana playlist yuborishingiz mumkin! 🎵",
                parse_mode=ParseMode.MARKDOWN
            )
        
        except Exception as e:
            logger.error(f"Xatolik: {e}")
            error_message = MESSAGES['error'].format(str(e))
            await processing_msg.edit_text(error_message)
    
    def run(self):
        """
        Botni ishga tushirish
        """
        logger.info("Bot ishga tushmoqda...")
        logger.info(f"Bot token: {BOT_TOKEN[:10]}...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main funksiya"""
    try:
        bot = TelegramBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi (Ctrl+C)")
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")


if __name__ == "__main__":
    main()
