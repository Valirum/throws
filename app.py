#!/usr/bin/env python3

import argparse
import json
from flask import Flask, request, jsonify, render_template

# Импорт функции обработки броска из модуля dice
# Убедитесь, что файл dice.py находится в той же папке
from dice import handle_line

app = Flask(__name__)

@app.route('/')
def serve_frontend():
    """Возвращает священный интерфейс броска костей"""
    return render_template('index.html')

@app.route('/roll', methods=['GET', 'POST'])
def roll_dice():
    """
    Эндпоинт для выполнения броска кубиков.
    Принимает параметр 'query' через GET или JSON поле 'query' через POST.
    """
    query = None
    
    # Получение строки запроса из разных источников
    if request.method == 'GET':
        query = request.args.get('query')
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            query = data.get('query')
    
    if not query:
        return jsonify({"error": "Отсутствует параметр query"}), 400

    # Предварительная обработка строки
    line = query.replace(' ', '').lower().replace("к", "d")

    try:
        # Вызов функции обработки из модуля dice
        # Функция возвращает кортеж (result, min, max)
        res, mn, mx = handle_line(line)
        
        # Округление или приведение к int для чистоты данных
        if res == int(res): res = int(res)
        if mn == int(mn): mn = int(mn)
        if mx == int(mx): mx = int(mx)

        response_data = {
            "query": line,
            "result": res,
            "min": mn,
            "max": mx
        }
        
        return jsonify(response_data), 200

    except Exception as e:
        # Обработка ошибок формата строки
        return jsonify({"error": "Ошибка обработки запроса", "details": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Эндпоинт для проверки работоспособности сервиса."""
    return jsonify({"status": "ok"}), 200

def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Микросервис для бросков кубиков")
    parser.add_argument('-p', '--port', type=int, default=6767, 
                        help='Порт для запуска сервера (по умолчанию 6767)')
    parser.add_argument('--host', type=str, default='0.0.0.0', 
                        help='Хост для запуска сервера')
    
    args = parser.parse_args()

    # Запуск сервера Flask
    print(f"Запуск сервера на {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
