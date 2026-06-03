import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import json
from datetime import datetime

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Films database
FILMS = [
    {
        "id": 1,
        "name": "Alov",
        "year": 2023,
        "rating": 8.5,
        "genre": ["Jangari", "Drama"],
        "country": "O'zbekiston",
        "director": "Javlon Mardonov",
        "age": "16+",
        "description": "Milliy qahramon haqida kimyo filmi"
    },
    {
        "id": 2,
        "name": "Hamsa",
        "year": 2022,
        "rating": 7.8,
        "genre": ["Oilasiy", "Drama"],
        "country": "O'zbekiston",
        "director": "Abror Abdullayev",
        "age": "12+",
        "description": "Oila munosabatlari haqida film"
    },
    {
        "id": 3,
        "name": "Shuhrat",
        "year": 2021,
        "rating": 8.2,
        "genre": ["Jangari", "Fantastika"],
        "country": "O'zbekiston",
        "director": "Mirza Juraev",
        "age": "18+",
        "description": "Shuhrat va xizmat haqida epik film"
    },
    {
        "id": 4,
        "name": "Sevgi",
        "year": 2023,
        "rating": 7.5,
        "genre": ["Melodrama", "Drama"],
        "country": "O'zbekiston",
        "director": "Dilmurod Rahimov",
        "age": "12+",
        "description": "Haqiqiy sevgi haqida tarixiy film"
    },
    {
        "id": 5,
        "name": "Voqea",
        "year": 2022,
        "rating": 8.0,
        "genre": ["Thriller", "Jangari"],
        "country": "O'zbekiston",
        "director": "Aziz Mirzioyev",
        "age": "16+",
        "description": "Hayratlarikrik voqealar haqida film"
    },
    {
        "id": 6,
        "name": "Orzu",
        "year": 2021,
        "rating": 7.3,
        "genre": ["Komediya", "Drama"],
        "country": "O'zbekiston",
        "director": "Feruz Rahmonov",
        "age": "12+",
        "description": "Orzu va orzularni amalga oshirish haqida"
    },
    {
        "id": 7,
        "name": "Taqdim",
        "year": 2023,
        "rating": 8.7,
        "genre": ["Fantastika", "Jangari"],
        "country": "O'zbekiston",
        "director": "Ravshan Shodiev",
        "age": "14+",
        "description": "Kelajak dunyasi haqida fantastika filmi"
    },
    {
        "id": 8,
        "name": "Qalbim",
        "year": 2022,
        "rating": 7.9,
        "genre": ["Melodrama", "Oilasiy"],
        "country": "O'zbekiston",
        "director": "Almaz Xaitov",
        "age": "12+",
        "description": "Qalbdan chiqgan sevgi hikoyasi"
    },
    {
        "id": 9,
        "name": "Xurriyet",
        "year": 2021,
        "rating": 8.4,
        "genre": ["Jangari", "Drama"],
        "country": "O'zbekiston",
        "director": "Oybek Sardarov",
        "age": "16+",
        "description": "Xurriyet uchun kurashshlar haqida"
    },
    {
        "id": 10,
        "name": "Rasm",
        "year": 2023,
        "rating": 7.6,
        "genre": ["Drama", "Oilasiy"],
        "country": "O'zbekiston",
        "director": "Bobur Salimov",
        "age": "12+",
        "description": "San'at va ijod haqida film"
    },
    {
        "id": 11,
        "name": "Tarbiya",
        "year": 2022,
        "rating": 8.1,
        "genre": ["Drama", "Oilasiy"],
        "country": "O'zbekiston",
        "director": "Zokir Xolmirzoev",
        "age": "12+",
        "description": "Avlodlarni tarbiya qilish haqida"
    },
    {
        "id": 12,
        "name": "Kun",
        "year": 2021,
        "rating": 7.4,
        "genre": ["Komediya", "Oilasiy"],
        "country": "O'zbekiston",
        "director": "Sardor Bekmurodov",
        "age": "12+",
        "description": "Kundalik hayot va xursilari haqida"
    },
    {
        "id": 13,
        "name": "Sadoqat",
        "year": 2023,
        "rating": 8.3,
        "genre": ["Drama", "Jangari"],
        "country": "O'zbekiston",
        "director": "Uktam Qudratov",
        "age": "16+",
        "description": "Watan va sadoqat haqida milliy film"
    },
    {
        "id": 14,
        "name": "Ilm",
        "year": 2022,
        "rating": 7.7,
        "genre": ["Drama", "Oilasiy"],
        "country": "O'zbekiston",
        "director": "Bakhodir Rahimov",
        "age": "14+",
        "description": "Ilm va ma'rifat yo'li haqida"
    },
    {
        "id": 15,
        "name": "Umid",
        "year": 2021,
        "rating": 8.0,
        "genre": ["Drama", "Melodrama"],
        "country": "O'zbekiston",
        "director": "Karim Sharipov",
        "age": "12+",
        "description": "Umid va ishonch haqida ilhomlantiruvchi film"
    }
]

GENRES = ["Jangari", "Fantastika", "Drama", "Komediya", "Melodrama", "Thriller", "Oilasiy"]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"""
🎬 *Kino Bot Uz ga xush kelibsiz!*

Assalomu alekum, {user.first_name}! 👋

Bizda 15+ O'zbek filmi bor. Siz qidirish, reyting ko'rish, janr bo'yicha filterlash va boshqalarni qila olasiz.

*Asosiy tugmalar:*
🔍 Qidirish - Filmni nomi bo'yicha qidiring
⭐ Reyting - Eng yaxshi filmlarni ko'ring
🎭 Janr - Janr bo'yicha filmlarni ko'ring
🎲 Tasodifiy - Random film taklifi olish
📋 Barcha - Barcha filmlar ro'yxati
ℹ️ Haqida - Bot haqida
    """
    
    keyboard = [
        [KeyboardButton("🔍 Qidirish"), KeyboardButton("⭐ Reyting")],
        [KeyboardButton("🎭 Janr"), KeyboardButton("🎲 Tasodifiy")],
        [KeyboardButton("📋 Barcha"), KeyboardButton("ℹ️ Haqida")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# Handle buttons
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    if text == "🔍 Qidirish":
        await update.message.reply_text("🔍 Film nomini yozing:\n\nMasalan: Alov, Hamsa, Shuhrat")
        context.user_data['mode'] = 'search'
    
    elif text == "⭐ Reyting":
        sorted_films = sorted(FILMS, key=lambda x: x['rating'], reverse=True)[:5]
        response = "*⭐ Eng Yaxshi Filmlar (Top 5):*\n\n"
        for i, film in enumerate(sorted_films, 1):
            response += f"{i}. *{film['name']}* ⭐ {film['rating']}/10\n"
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    
    elif text == "🎭 Janr":
        keyboard = [[KeyboardButton(genre)] for genre in GENRES]
        keyboard.append([KeyboardButton("◀️ Orqaga")])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("🎭 Janr tanlang:", reply_markup=reply_markup)
        context.user_data['mode'] = 'genre'
    
    elif text == "🎲 Tasodifiy":
        import random
        film = random.choice(FILMS)
        await show_film_details(update, film)
    
    elif text == "📋 Barcha":
        response = "*📋 Barcha Filmlar:*\n\n"
        for film in FILMS:
            response += f"• *{film['name']}* ({film['year']}) - ⭐ {film['rating']}/10\n"
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    
    elif text == "ℹ️ Haqida":
        about = """
*ℹ️ Bot Haqida:*

🎬 Kino Bot Uz - O'zbek kinolari haqida ma'lumot beruvchi bot

*Funksiyalari:*
✅ Film qidirish
✅ Reyting ko'rish
✅ Janr bo'yicha filterlash
✅ Tasodifiy taklif
✅ To'liq ma'lumot

*Yaratilgan:* 2026-yil
*Til:* O'zbek
*Dasturi:* Python + Telegram

Savollar bo'lsa: @KinoBotUz_support
        """
        await update.message.reply_text(about, parse_mode=ParseMode.MARKDOWN)
    
    elif text == "◀️ Orqaga":
        keyboard = [
            [KeyboardButton("🔍 Qidirish"), KeyboardButton("⭐ Reyting")],
            [KeyboardButton("🎭 Janr"), KeyboardButton("🎲 Tasodifiy")],
            [KeyboardButton("📋 Barcha"), KeyboardButton("ℹ️ Haqida")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text("🎬 Asosiy menyuga qaytdingiz:", reply_markup=reply_markup)
        context.user_data['mode'] = None
    
    elif context.user_data.get('mode') == 'search':
        search_term = text.lower()
        results = [f for f in FILMS if search_term in f['name'].lower()]
        
        if results:
            for film in results:
                await show_film_details(update, film)
        else:
            await update.message.reply_text(f"❌ '{text}' nomli film topilmadi. Boshqa nom yozing.")
        context.user_data['mode'] = None
    
    elif context.user_data.get('mode') == 'genre':
        if text in GENRES:
            results = [f for f in FILMS if text in f['genre']]
            if results:
                response = f"*🎭 {text} janri filmlar:*\n\n"
                for film in results:
                    response += f"• *{film['name']}* ({film['year']}) - ⭐ {film['rating']}/10\n"
                await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(f"❌ {text} janrida film topilmadi.")
        context.user_data['mode'] = None

async def show_film_details(update: Update, film: dict) -> None:
    details = f"""
*🎬 {film['name']}*

📅 *Yil:* {film['year']}
⭐ *Reyting:* {film['rating']}/10
🎭 *Janr:* {', '.join(film['genre'])}
🌍 *Davlat:* {film['country']}
👨‍🎬 *Rejissyor:* {film['director']}
🔞 *Yosh chegarasi:* {film['age']}

📝 *Tavsifi:*
{film['description']}

━━━━━━━━━━━━━━━━
ID: {film['id']}
    """
    await update.message.reply_text(details, parse_mode=ParseMode.MARKDOWN)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token("8783160802:AAHKYVvDZS3KR9Rh34tNHng9jXc3XLFkotU").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    
    # Handle all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
