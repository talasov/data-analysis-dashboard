# Импорт данных в HTTP сервис

Этот HTTP сервис разработан для загрузки и работы с импортируемыми данными, предоставляемыми в формате CSV. Структура файлов может изменяться, и сервис обрабатывает их динамически.

## Функциональность

Сервис предоставляет следующие функции:

- Авторизация пользователя
- Загрузка данных в формате CSV.
- Получение списка файлов с информацией о колонках.
- Получение данных из конкретного файла с опциональной фильтрацией и сортировкой по одному или нескольким столбцам.
- Удаление данных

## Технологии и зависимости

Сервис разработан с использованием следующих технологий и библиотек:

- Python 3.9
- Django REST framework
- PostgreSQL 
- Docker 
- pandas
- simplejwt
- postman

## Установка и запуск

Для запуска сервиса выполните следующие шаги:

1. Установите Docker и Docker Compose, если они еще не установлены.

2. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/talasov/data-analysis-dashboard.git

3. Создайте файл .env внесите данные, шаблон в файле .env.example

    ```bash
    DEBUG=True
    SECRET_KEY=mysecretkey
    DJANGO_DB_HOST=db
    DJANGO_DB_PORT=5432
    DJANGO_DB_NAME=mydatabase
    DJANGO_DB_USER=myuser
    DJANGO_DB_PASSWORD=mypassword

4. Запустите Docker Compose для создания контейнеров и запуска приложения
    ```bash
    docker-compose up

5. После успешного запуска, сервис будет доступен по адресу http://localhost:8000/.

6. Можно скачать уже готовую Postman коллекцию в директории `DataManagement/Postman_collections`

## Использование

1 . Отправьте POST-запрос на `api/accounts/register/`
- в теле запроса укажите данные для регестрации

    ```bash
    {
    "username": "user",
    "password": "pasword",
    "email": "user@user.ru"
    }
- Пользователь зарегестестрируеться - ему присвоеться JWT token

2. Отправьте POST-запрос на `/api/upload/`
- прикрепив файл CSV в теле запроса.
- добавьте jwt token для отправки POST запроса
- файл загрузиться на сервер, с информацией о колонках в файле `column_info`

3. Для получения списка загруженных файлов, отправьте GET-запрос на `/api/files/`
- Вы получите список всех загруженных файлов с `column_info`


4. Для получения информации о конкретном файле отправте запрос с id файла `/api/files/file_id/`

5. Для получения данных из конкретного файла, отправьте POST-запрос на `/api/all_data/`
   - в теле письма укажите id файла и колонки данныее из которых хотите отфильтровать
       ```bash 
     Пример:
     {
     "file_id": 2,
     "columns": ["cache", "Month"]
       }
    - Выведуться данные из выбраного файла, из указаных колонок с фильтрацией 
    - (в данном случаи отсеиваются данные в которых присутсвуют символы или заглавные буквы)
6. Для удаления данных отправьте запрос на адрес `api/files/file_id/delete/`

