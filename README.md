````markdown
# 🎬 Kino Bot UZ

O'zbek kinolari haqida ma'lumot beruvchi Telegram boti.

## ✨ Funksiyalari

✅ **Film Qidirish** - Nomи bo'yicha film qidiring  
✅ **Reyting** - Eng yaxshi filmlarni ko'ring (Top 5)  
✅ **Janr Filterlash** - Janr bo'yicha filmlarni ko'ring  
✅ **Tasodifiy Taklif** - Random film taklifi olish  
✅ **To'liq Ma'lumot** - Film haqida batafsil ma'lumot  
✅ **24/7 Ishlash** - Har doim aktiv

## 🎭 Janrlar

- Jangari (Action)
- Fantastika (Fantasy)
- Drama
- Komediya (Comedy)
- Melodrama
- Thriller
- Oilasiy (Family)

## 📊 Film Ma'lumotlari

Botda 15+ O'zbek filmi mavjud:
- Film nomi
- Yili
- Reyting (1-10)
- Janri
- Davlati
- Rejissyori
- Yosh chegarasi
- Tavsifi

## 🚀 Ishga tushirish

### Rekvisitlar

- Python 3.8+
- Telegram Bot Token

### O'rnatish

1. Repository klonlash:
```bash
git clone https://github.com/kenjayevj557-glitch/kino-bot-uz.git
cd kino-bot-uz
```

2. Dependencies o'rnatish:
```bash
pip install -r requirements.txt
```

3. Bot tokenini o'rnatish (bot.py da 485-qatorda):
```python
application = Application.builder().token("YOUR_TOKEN_HERE").build()
```

4. Botni ishga tushirish:
```bash
python bot.py
```

## 🔧 Konfiguratsiya

Bot token olish:
1. Telegramda [@BotFather](https://t.me/botfather) ga murojaat qiling
2. `/newbot` komandasini yuboring
3. Bot nomini kiriting: `KinoBotUz`
4. Username kiriting: `kino_bot_uz` (yoki boshqa)
5. Tokenni nusxalang

## 📱 Telegram Bot

Bot: [@KinoBotUz](https://t.me/KinoBotUz)

## 🎯 Tugmalar

- 🔍 **Qidirish** - Film nomini yozing va qidiring
- ⭐ **Reyting** - Eng yaxshi 5 filmni ko'ring
- 🎭 **Janr** - Janr tanlang va filmlarni ko'ring
- 🎲 **Tasodifiy** - Random film taklifi olish
- 📋 **Barcha** - Barcha filmlar ro'yxati
- ℹ️ **Haqida** - Bot haqida ma'lumot

## 🌐 Hosting

Replit/Glitch da 24/7 ishga tushirish uchun:

1. [Replit.com](https://replit.com) da ro'yxatdan o'ting
2. Repository importlab qiling
3. `python bot.py` ishga tushiring
4. UptimeRobot yoki shunga o'xshash xizmat bilan pinglab turing

## 📄 Fayl Struktura

```
kino-bot-uz/
├── bot.py              # Asosiy bot kodi
├── requirements.txt    # Dependencies
├── README.md          # Bu fayl
└── .gitignore         # Git ignor file
```

## 🛠️ Texnik Tafsilotlar

- **Dasturlash Tili:** Python 3.8+
- **Kutubxona:** python-telegram-bot 20.7
- **Baza:** JSON (Memory)
- **Hosting:** Replit/Glitch (24/7)

## 📝 Filmlar Qo'shish

`bot.py` dagi `FILMS` arrayga yangi film qo'shish:

```python
{
    "id": 16,
    "name": "Film Nomi",
    "year": 2024,
    "rating": 8.5,
    "genre": ["Jangari", "Drama"],
    "country": "O'zbekiston",
    "director": "Rejissyor Ismi",
    "age": "16+",
    "description": "Film tavsifi..."
}
```

## 🤝 Hissa Qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. Commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## 📧 Aloqa

- GitHub: [@kenjayevj557-glitch](https://github.com/kenjayevj557-glitch)
- Email: kenjayevj557@gmail.com
- Telegram Bot: [@KinoBotUz](https://t.me/KinoBotUz)

## 📄 Litsenziya

MIT License - [LICENSE](LICENSE) fayl ko'ring

## ⭐ Stars

Agar bot sizga yoqdigan bo'lsa, ⭐ star bering!

---

*Yaratilgan: 2026*  
*Bot: Kino Bot UZ v1.0*  
*Til: O'zbek 🇺🇿*
````
