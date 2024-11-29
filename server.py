from flask import Flask, request
import requests
import random
import time
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Параметры системы
THRESHOLD = 50  # Пороговое значение освещенности
LAMP_URL = "http://localhost:5001/lamp"  # URL фонаря

def simulate_sensor():
    """Симуляция датчика освещенности."""
    return random.randint(0, 100)

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    state = data.get('state')
    logging.info(f"Получена команда: {'включить' if state else 'выключить'} фонарь")
    response = requests.post(LAMP_URL, json={'state': state})
    return response.text, response.status_code

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
        time.sleep(5)

if __name__ == "__main__":
    app.run(port=5000)
    main()