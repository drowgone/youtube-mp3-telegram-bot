# GitHub Token Setup Guide

Repository yaratildi, lekin kod yuklash uchun Personal Access Token kerak.

## GitHub'ga kod yuklash uchun:

### 1. Personal Access Token yarating

1. GitHub'da o'ting: https://github.com/settings/tokens
2. **"Generate new token (classic)"** tugmasini bosing
3. Token nomini kiriting: **"YouTube MP3 Bot"**
4. Expiration: **90 days** (yoki istalgan muddat)
5. **Scopes** - quyidagini belgilang:
   - ☑️ **repo** (Full control of private repositories)
6. **"Generate token"** tugmasini bosing
7. Token nusxalang (u `ghp_` bilan boshlanadi)

### 2. Tokenni ishlatib kod yuklash

Terminal'da quyidagi buyruqni ishga tushiring:

```bash
cd /home/donegrow/.gemini/antigravity/scratch/youtube-mp3-bot
git push -u origin main
```

Username so'raganda: `drowgone`
Password so'raganda: **GitHub tokenni** kiriting (parol emas!)

Yoki bir buyruq bilan:

```bash
git remote set-url origin https://drowgone:YOUR_TOKEN_HERE@github.com/drowgone/youtube-mp3-telegram-bot.git
git push -u origin main
```

`YOUR_TOKEN_HERE` o'rniga GitHub tokenni qo'ying.

---

## Muqobil: SSH Key ishlatish

Agar SSH key sozlangan bo'lsa:

```bash
git remote set-url origin git@github.com:drowgone/youtube-mp3-telegram-bot.git
git push -u origin main
```

---

**Repository URL**: https://github.com/drowgone/youtube-mp3-telegram-bot
