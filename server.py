from flask import Flask, request, jsonify
import requests
import random
import time
import logging
import numpy as np

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Настройка логирования с уровнем INFO и форматом, который включает время и сообщение
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Параметры системы
THRESHOLD = 50  # Пороговое значение освещенности
LAMP_URL = "http://localhost:5001/lamp"  # URL фонаря
UPDATE_INTERVAL = 10  # Интервал обновления в секундах

# Функция симуляции датчика освещенности
def simulate_sensor():
    """Симуляция датчика освещенности с нормальным распределением."""
    # Нормальное распределение со средним значением 50 и стандартным отклонением 20
    light_level = int(np.random.normal(50, 20))
    # Ограничиваем значения от 0 до 100
    light_level = max(0, min(100, light_level))
    return light_level

# Обработчик POST-запроса для управления фонарем
@app.route('/control', methods=['POST'])
def control():
    # Извлекаем состояние фонаря из JSON-тела запроса
    data = request.json
    state = data.get('state')
    # Логируем команду
    logging.info(f"Получена команда: {'включить' if state else 'выключить'} фонарь")
    # Отправляем POST-запрос на LAMP_URL с новым состоянием фонаря
    response = requests.post(LAMP_URL, json={'state': state})
    # Возвращаем ответ от сервера фонаря
    return response.text, response.status_code

# Обработчик GET-запроса для получения состояния фонаря
@app.route('/control', methods=['GET'])
def get_control_state():
    # Генерируем уровень освещенности с помощью simulate_sensor
    light_level = simulate_sensor()
    # Определяем состояние фонаря (включен или выключен)
    state = light_level < THRESHOLD
    # Возвращаем JSON с состоянием и уровнем освещенности
    return jsonify({'state': state, 'light_level': light_level})

# Основная функция для симуляции работы контроллера
def main():
    # Логируем начало симуляции работы контроллера
    logging.info("Симуляция работы контроллера началась.")
    # Бесконечный цикл для симуляции работы контроллера
    while True:
        # Симуляция измерения освещенности
        light_level = simulate_sensor()
        # Логируем измеренный уровень освещенности
        logging.info(f"Измеренный уровень освещенности: {light_level}")

        # Принятие решения о включении/выключении фонаря
        if light_level < THRESHOLD:
            # Отправляем POST-запрос на /control с состоянием True (включить фонарь)
            requests.post('/control', json={'state': True})
        else:
            # Отправляем POST-запрос на /control с состоянием False (выключить фонарь)
            requests.post('/control', json={'state': False})

        # Имитация задержки
        time.sleep(UPDATE_INTERVAL)

# Запуск сервера
if __name__ == "__main__":
    # Запускаем сервер Flask на порту 5000
    app.run(port=5000)
    # Вызываем функцию main для симуляции работы контроллера
    main()
