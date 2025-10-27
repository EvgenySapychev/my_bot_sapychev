# bot.py
import os
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Читаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не задана. Выполни: export BOT_TOKEN='тут_токен'")

# Настройка словаря магазинов -> локальные файлы (в папке images/)
BASE_IMG_DIR = Path(__file__).parent / "image"
STORES = {
    "X5": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/X5.jpg",
    "Магнит": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/MAGNIT.jpg",
    "Фамилия": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/FAMILIA.jpg",
    "GJ": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/GJ.jpg",
    "Kari": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/KARI.jpg",
    "METRO": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/METRO.jpg",
    "Подружка": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/PODRUS.jpg",
    "Rendez-vous": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/RANDEV.jpg",
    "Рив Гош": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/RIVGOSH.jpg",
    "Улыбка Радуги": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/ULIBKA_RADUGI.jpg",
    "Винлаб": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/VINLAB.jpg",
    "Зарина": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/ZARINA.jpg",
    "Здрав Сити": BASE_IMG_DIR / "/Users/esapychev/PycharmProjects/my_telegram_bot/image/ZDRAVSI.jpg",
    "Алёнка": BASE_IMG_DIR / "https://disk.yandex.ru/i/cRyad4sQCU6AgA"
}

def get_main_menu():
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in STORES.keys()]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери магазин:", reply_markup=get_main_menu())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    store_name = query.data

    img_path = STORES.get(store_name)
    if img_path and img_path.exists():
        # открываем файл в режиме rb и отправляем
        with open(img_path, "rb") as f:
            await query.message.reply_photo(photo=f, caption=f"Это магазин {store_name} 🛍️")
    else:
        # если файл отсутствует — отправим сообщение об ошибке
        await query.message.reply_text(f"Картинка для {store_name} не найдена. Проверь папку images/")

    # снова присылаем меню
    await query.message.reply_text("Выбери другой магазин:", reply_markup=get_main_menu())

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Бот запущен. Открой чат и напиши /start")
    app.run_polling()

if __name__ == "__main__":
    main()
