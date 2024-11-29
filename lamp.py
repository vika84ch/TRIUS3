from flask import Flask, request
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

LAMP_STATE = False  # Состояние фонаря (изначально выключен)

@app.route('/lamp', methods=['POST'])
def lamp():
    global LAMP_STATE
    data = request.json
    state = data.get('state')
    if state != LAMP_STATE:
        LAMP_STATE = state
        logging.info(f"Фонарь {'включен' if state else 'выключен'}")
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5001)