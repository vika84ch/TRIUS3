from flask import Flask, request
import logging

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Настройка логирования с уровнем INFO и форматом, который включает время и сообщение
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Состояние фонаря (изначально выключен)
LAMP_STATE = False

# Обработчик POST-запроса для управления состоянием фонаря
@app.route('/lamp', methods=['POST'])
def lamp():
    global LAMP_STATE
    # Извлекаем состояние фонаря из JSON-тела запроса
    data = request.json
    state = data.get('state')
    # Если новое состояние отличается от текущего, обновляем его
    if state != LAMP_STATE:
        LAMP_STATE = state
        # Логируем новое состояние фонаря
        logging.info(f"Фонарь {'включен' if state else 'выключен'}")
    # Возвращаем ответ "OK" с кодом 200
    return "OK", 200

# Запуск сервера
if __name__ == "__main__":
    # Запускаем сервер Flask на порту 5001
    app.run(port=5001)
