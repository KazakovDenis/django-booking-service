# Сервис записи клиентов
![Python version](https://img.shields.io/badge/python-3.7%2B-blue)
[![Build Status](https://travis-ci.com/KazakovDenis/booking-service.svg?branch=main)](https://travis-ci.com/KazakovDenis/booking-service)

Сервис реализован для поликлиники.  
[Техническое задание](https://github.com/KazakovDenis/booking-service/blob/main/task.txt)  

## Использованный технологический стек
* Python, Javascript
* Django 3.1.4
* Docker

## Запуск сервиса
Для запуска в docker-контейнере необходимо:  
  
1). добавить следующие данные в переменные окружения:  
```
export BOOKING_SECRET="ваш_секретный_ключ"
```
2). запустить сервис  
```
docker-compose up -d --build
```
  
Далее вы можете приступить к работе с сервисом по адресу: http://localhost:8000/  
Войти в административную часть можно по логину и паролю "admin". Смените их после первого входа.
  
Если вам необходимо наполнить базу демонстрационными данными, выполните команду:
```
docker-compose exec booking python manage.py create_demo
```

## Тестирование
Клонируйте репозиторий, подготовьте окружение
```
git clone https://github.com/KazakovDenis/booking-service.git
cd booking-service
python3 -m venv venv
source venv/bin/activate
pip install -U pip && pip install -r requirements/base.txt
```
  
и выполните следующую команду в директории
```
cd booking_service && ./manage.py test
```