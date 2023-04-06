# salary_data_aggregation

# Запуск проекта

##### 1) Клонировать репозиторий

    https://github.com/AlSh65/salary_data_aggregation.git

##### 2) Указать в .env параметры токена бота и базы данных. 
По умолчанию выставлены параметры для локальной базы данных и для бота @test_aggregate_bot

##### 3) Создать и активировать виртульное окружение

    source venv/bin/activate
    
##### 4) Устанавливить зависимости:
    pip install -r requirements.txt
##### 5) Установить статическую коллекцию в MongoDB :
    Расположение: ./bot/database/static_collection/load_static_collection.py

##### 6) Запустить бота

    python3 run.py
    