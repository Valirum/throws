#!/bin/bash

# Настройка строгого режима: остановка при ошибке
set -e

PROJECT_NAME="dice_service"
VENV_DIR="venv"
SERVER_SCRIPT="app.py"
REQUIREMENTS_FILE="requirements.txt"

echo "Инициализация подсистемы для ${PROJECT_NAME}..."

# Проверка наличия Python 3
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не обнаружен в системе."
    exit 1
fi

# Создание виртуального окружения, если оно отсутствует
if [ ! -d "${VENV_DIR}" ]; then
    echo "Создание священного виртуального окружения..."
    python3 -m venv ${VENV_DIR}
else
    echo "Виртуальное окружение уже существует."
fi

# Активация окружения
echo "Активация окружения..."
source ${VENV_DIR}/bin/activate

# Проверка и создание файла зависимостей
if [ ! -f "${REQUIREMENTS_FILE}" ]; then
    echo "Файл зависимостей не найден. Создание нового с Flask..."
    echo "flask" > ${REQUIREMENTS_FILE}
else
    echo "Файл зависимостей найден."
fi

# Установка зависимостей
echo "Установка пакетов из ${REQUIREMENTS_FILE}..."
pip install --upgrade pip
pip install -r ${REQUIREMENTS_FILE}

# Запуск сервера
echo "Запуск ${SERVER_SCRIPT}..."
# Сервер поддерживает аргументы, например: python server.py --port 6767
python ${SERVER_SCRIPT}

# Деактивация окружения (если скрипт завершится)
deactivate
echo "Сессия завершена."
