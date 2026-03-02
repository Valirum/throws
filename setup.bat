@echo off
setlocal

set PROJECT_NAME=dice_service
set VENV_DIR=venv
set SERVER_SCRIPT=app.py
set REQUIREMENTS_FILE=requirements.txt

echo Инициализация подсистемы для %PROJECT_NAME%...

rem Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не обнаружен в системе.
    exit /b 1
)

rem Создание виртуального окружения
if not exist "%VENV_DIR%" (
    echo Создание виртуального окружения...
    python -m venv %VENV_DIR%
) else (
    echo Виртуальное окружение уже существует.
)

rem Активация окружения
echo Активация окружения...
call %VENV_DIR%\Scripts\activate.bat

rem Проверка зависимостей
if not exist "%REQUIREMENTS_FILE%" (
    echo Файл зависимостей не найден. Создание нового с Flask...
    echo flask > %REQUIREMENTS_FILE%
) else (
    echo Файл зависимостей найден.
)

rem Установка зависимостей
echo Установка пакетов из %REQUIREMENTS_FILE%...
python -m pip install --upgrade pip
pip install -r %REQUIREMENTS_FILE%

rem Запуск сервера
echo Запуск %SERVER_SCRIPT%...
python %SERVER_SCRIPT%

rem Деактивация
deactivate
echo Сессия завершена.

endlocal
