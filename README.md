# scraping_proxies (Test Assignment)
Parsing proxies and uploading them to the server

Парсинг прокси и загрузка на сервер

## Description / Описание
scraping_proxies is a Scrapy-based parser that scrapes the first 150 proxies (IP, port, protocols) from advanced.name, saves the data to proxies.json, and uploads the parsed (IP and port) data in batches of 25 to a form at test-rg8.ddns.net.
The returned save_id values from the server are associated with the uploaded proxies and saved in results.json. The entire process is logged, and execution time is recorded in time.txt.

scraping_proxies — это парсер на Scrapy, который парсит первые 150 прокси (IP, порт, протоколы) с advanced.name, сохраняет данные в файл proxies.json, загружает спарсенные данные (IP, порт) в форму на test-rg8.ddns.net. Загрузка реализована батчами по 25 записей. Полученные save_id от сервера ассоциируются с прокси и сохраняются в файл results.json. Время выполнения сохраняется в time.txt.

## Technologies / Технологии
* Python 3.12
* Scrapy 2.13
* python-dotenv 1.1.1

## Installation and Run / Установка и запуск проекта
Clone the repository / Клонировать репозиторий
```
git clone https://github.com/KonstantinSKS/scraping_proxies.git
```
or with SSH / или по SSH:
```
git clone git@github.com:KonstantinSKS/scraping_proxies.git
```

Enter the project folder / Перейти в папку с проектом:
```
cd scraping_proxies
```

Create .env file in the root directory and fill it using .env.template — you will need a personal token for test-rg8.ddns.net.

В корне проекта создать файл .env и заполнить по образцу .env.template — нужен персональный токен для test-rg8.ddns.net.

Create and activate a virtual environment / Создать и активировать виртуальное окружение

For Windows:
```
py -3.12 -m venv venv
```
```
source venv/Scripts/activate
```

For macOS / Linux:
```
python3.12 -m venv venv
```
```
source venv/bin/activate
```

Install dependencies / Установить зависимости
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Run the spider / Запустить паука
```
scrapy crawl proxy
```

This will:
* parse proxies
* save data to proxies.json
* upload to test-rg8.ddns.net
* save the response to results.json
* log execution time to time.txt

Это выполнит:
* парсинг прокси
* сохранение в proxies.json
* загрузку данных на test-rg8.ddns.net
* сохранение ответа в results.json
* логирование времени в time.txt

## Author / Автор
Konstantin Steblev / Стеблев Константин