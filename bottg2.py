import telegram
import openai
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Устанавливаем API-ключ OpenAI
openai.api_key = "YOUR_API_KEY"

# Создаем экземпляр бота телеграм
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Создаем словарь языковых кодов и соответствующих моделей OpenAI
LANGUAGES = {
    "en": "text-davinci-002",
    "es": "text-davinci-002",
    "ru": "text-davinci-002",
    # Добавьте другие языки здесь
}

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который готов общаться с тобой. Просто отправь мне сообщение!")

# Обработчик команды /setlang
def setlang(update, context):
    lang = context.args[0]
    if lang in LANGUAGES:
        context.user_data["language"] = lang
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Язык установлен на {lang}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Этот язык не поддерживается")

# Обработчик сообщений
def reply(update, context):
    # Получаем языковой код пользователя
    language = context.user_data.get("language", "en")
    
    # Получаем сообщение пользователя
    user_message = update.message.text
    
    # Определяем модель OpenAI для выбранного языка
    model = LANGUAGES[language]
    
    # Отправляем сообщение в OpenAI API и получаем ответ
    try:
        response = openai.Completion.create(
          engine=model,
          prompt=user_message,
          max_tokens=150,
          n=1,
          stop=None,
          temperature=0.7
        )
        
        # Извлекаем ответ из JSON-ответа OpenAI API
        bot_response = response.choices[0].text
        
        # Отправляем ответ обратно пользователю
        context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)
    except Exception as e:
        # Обрабатываем ошибку и сообщаем ее пользователю
        context.bot.send_message(chat_id=update.effective_chat.id, text="Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз или обратитесь в службу поддержки.")
        print(f"Произошла ошибка: {e}")

# Создаем экземпляр обновления и добавляем обработчики команд и сообщений
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("setlang", setlang))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

# Запускаем бота
updater.start_polling()
updater.idle()