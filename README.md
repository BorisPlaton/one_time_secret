# One time secret

Решение [тестового задания](https://github.com/avito-tech/mi-trainee-task) сервиса одноразовых секретов.

## Запуск
### Docker
Проект имеет `Dockerfile` и `docker-compose.yml`. Можно написать следующую команду, чтоб запустить приложение.
```
$ docker-compose up
```
### venv
Установить и запустите приложение можно следующими командами:
```
$ virtualenv venv --python 3.10
$ . venv/bin/activate
$ pip install -r requirements/prod.txt
$ python src/main.py
```
Папка `requirements/` имеет два файла:
- `prod.txt` - Зависимости для запуска приложения
- `dev.txt` - Зависимости для разработки (`flake8`, `pytest`, `coverage`)

## Настройки проекта
### .env
Проект имеет настройки по-умолчанию, но вы можете их изменить или через файл `.env`. Файл `.env.dist` содержит переменные для конфигурации проекта.
### ProjectSettings
Перейдите в `src/config/settings.py`, где есть класс `ProjectSettings`. Можно поменять значения атрибутов данного класса, но они будут перезаписаны переменными окружения, если таковы есть.

## Секретный ключ
Чтоб создать секретный ключ можно использовать следующие команды:
```
$ python
>>> from cryptography.fernet import Fernet
>>> Fernet.generate_key().decode()
'NxVTxQw0HNz3-pZ-a3S3X4wiq1ZPSC_F9T10YfLIUdc='
```
И скопировать результат работы метода класс `Fernet`. 

Создать секретный ключ вы можете сами другими способами, но учитывайте следующее:
> "Fernet key must be 32 url-safe base64-encoded bytes."

## Тесты
Если вы установили все необходимые зависимости для разработки (файл `dev.txt`), то выполните следующую команду:
```
$ pytest
```



