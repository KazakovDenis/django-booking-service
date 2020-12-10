# Сервис записи клиентов
![Python version](https://img.shields.io/badge/python-3.7%2B-blue)
[![Build Status](https://travis-ci.com/KazakovDenis/booking-service.svg?branch=main)](https://travis-ci.com/KazakovDenis/booking-service)

[Техническое задание](https://github.com/KazakovDenis/booking-service/blob/main/task.txt)  

## Использованный технологический стек
* Django 3.1.4
* Docker

## Запуск сервиса
* Для запуска в docker-контейнере необходимо:  
  
    1). добавить следующие данные в переменные окружения:  
    ```
    export BOOKING_SECRET="ваш_секретный_ключ"
    ```
    2). запустить сервис  
    ```
    docker-compose up -d --build
    ```
    3). создать администратора  
    ```
    docker-compose exec booking python3 manage.py createsuperuser
    ```
    4). проверить работу сервиса: http://localhost:8000/
