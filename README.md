# WeatherApp — веб-приложение прогноза погоды на Django

## Описание

Это простое и удобное веб-приложение, позволяющее пользователю вводить название города и получать актуальный прогноз погоды на ближайшее время. Приложение использует API Open-Meteo для получения данных о погоде.

## Реализованный функционал

- Получение прогноза погоды в удобночитаемом формате
- Автодополнение при вводе города

## Использованные технологии

- Python 3.12
- Django (веб-фреймворк)
- Django REST Framework для реализации API
- Requests для работы с внешним API Open-Meteo
- JavaScript (минимально) для автодополнения
- SQLite (по умолчанию) для хранения данных
- Стандартные шаблоны Django для фронтенда


## Запуск проекта

```bash
# Клонировать репозиторий и перейти в папку проекта
git clone https://github.com/rvllvd/weather_project

# Создать виртуальнле окружение: 
python -m venv

# Активировать виртуальное окружение: 
source ./venv/bin/activate

# Установить зависимости из requirements.txt: 
pip install -r requirements.txt

# Добавить в переменные окруженния SECRET_KEY (обычно не хранится в репозитории)
echo "SECRET_KEY='b90k6h+463z64bk0h#e5n3zi@04)emn05e#yja&br1(^8e_89'" > .env

# Создать миграции:
python manage.py makemigrate

# Провести миграции: 
python manage.py migrate

# Запустить тесты:
python manage.py test

# Поднять сервер с сайтом:
python manage.py runserver
```
