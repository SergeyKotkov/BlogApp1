Технические требования:
Python 3.8+
Django 3+
DRF 3.10+
PostgreSQL 10+
Структура приложения
Задача 1
МОДЕЛИ

 

Модель пользователя

логин
пароль
номер
дата рождения
дата создания
дата редактирования
Модель поста

заголовок
текст
изображение (если есть)
автор
комментарии
дата создания
дата редактирования
Модель комментария

автор
текст
дата создания
дата редактирования
 

Примечание: связи между моделями определите самостоятельно.

Задача 2
ЭНДПОИНТЫ

Реализуйте CRUD для каждой модели.

Пользователь:

CREATE: все пользователи (регистрация).
READ: администратор/авторизованные пользователи.
UPDATE: администратор/пользователь может редактировать только себя./
DELETE: администратор.
Пост:

CREATE: авторизованные пользователи.
READ: все пользователи.
UPDATE: администратор/пользователь может редактировать только себя.
DELETE: администратор/пользователь может удалять свои посты.
Комментарий:

CREATE: авторизованные пользователи.
READ: все пользователи.
UPDATE: администратор/пользователь может редактировать только себя.
DELETE: администратор/пользователь может удалять свои комментарии.
Задача 3
ВАЛИДАТОРЫ

Модель пользователя

Реализуйте валидатор для пароля (должен быть не менее 8 символов, должен включать цифры).

Реализуйте валидатор для почты (разрешены домены: mail.ru, yandex.ru).

Модель поста

Реализуйте проверку того, что автор поста достиг возраста 18 лет.

Реализуйте проверку, что автор в заголовок не вписал запрещенные слова: ерунда, глупость, чепуха.

Задача 4
АДМИН. ПАНЕЛЬ

Добавьте в объекте поста ссылку на автора.

Добавьте фильтр по дате создания поста.

Критерии приемки
Все три модели описаны.
Все эндпоинты реализованы.
Все описанные валидации настроены.
Админка настроена.
Описанные права доступа заложены в проект.
Решение выложено на github.com.