import telebot
from assistant import AutonomousAssistant
import json

bot = telebot.TeleBot("ВАШ_API_ТОКЕН")
assistant = AutonomousAssistant()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ Автономный помощник ProjectGuardian активирован!\nКоманды:\n/report - отчёт\n/add_project - добавить проект")

@bot.message_handler(commands=['report'])
def send_report(message):
    report = assistant.generate_report()
    bot.send_message(message.chat.id, f"📊 Отчёт проектов:\n{json.dumps(report, indent=2, ensure_ascii=False)}")

@bot.message_handler(commands=['add_project'])
def add_project(message):
    msg = bot.reply_to(message, "Введите название проекта и срок (формат: Название;ГГГГ-ММ-ДД)")
    bot.register_next_step_handler(msg, process_project)

def process_project(message):
    try:
        name, deadline = message.text.split(';')
        result = assistant.add_project(name, deadline)
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()