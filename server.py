from flask import Flask, request, jsonify
import requests
import random
import time
import logging
import numpy as np

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Параметры системы
THRESHOLD = 50  # Пороговое значение освещенности
LAMP_URL = "http://localhost:5001/lamp"  # URL фонаря
UPDATE_INTERVAL = 10  # Интервал обновления в секундах

def simulate_sensor():
    """Симуляция датчика освещенности с нормальным распределением."""
    # Нормальное распределение со средним значением 50 и стандартным отклонением 20
    light_level = int(np.random.normal(50, 20))
    # Ограничиваем значения от 0 до 100
    light_level = max(0, min(100, light_level))
    return light_level

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    state = data.get('state')
    logging.info(f"Получена команда: {'включить' if state else 'выключить'} фонарь")
    response = requests.post(LAMP_URL, json={'state': state})
    return response.text, response.status_code

@app.route('/control', methods=['GET'])
def get_control_state():
    light_level = simulate_sensor()
    state = light_level < THRESHOLD
    return jsonify({'state': state, 'light_level': light_level})

def main():
    logging.info("Симуляция работы контроллера началась.")
    while True:
        # Симуляция измерения освещенности
        light_level = simulate_sensor()
        logging.info(f"Измеренный уровень освещенности: {light_level}")

        # Принятие решения о включении/выключении фонаря
        if light_level < THRESHOLD:
            requests.post('/control', json={'state': True})
        else:
            requests.post('/control', json={'state': False})

        # Имитация задержки
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    app.run(port=5000)
    main()
