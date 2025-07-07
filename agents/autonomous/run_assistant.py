from agents.autonomous.assistant import AutonomousAssistant
import threading

def start_telegram_bot():
    from agents.autonomous.telegram_interface import bot
    bot.infinity_polling()

if __name__ == "__main__":
    # Инициализация помощника
    assistant = AutonomousAssistant()
    
    # Добавляем тестовые данные
    assistant.add_project("Киберспортивный прогнозист", "2024-12-01")
    assistant.add_task("Киберспортивный прогнозист", "Разработка парсера данных HLTV.org", 1)
    assistant.allocate_resources("Киберспортивный прогнозист", "GPU-hours", 500)
    
    # Запускаем автономный цикл в отдельном потоке
    autonomous_thread = threading.Thread(
        target=assistant.autonomous_loop,
        kwargs={"interval_minutes": 60}
    )
    autonomous_thread.daemon = True
    autonomous_thread.start()
    
    # Запускаем Telegram-бот
    start_telegram_bot()