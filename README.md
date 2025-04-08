# System-for-determination-BBK-UDK-code-of-science-project-and-etc.
	Глава 1. Функциональные возможности модуля
	Разработанный модуль предоставляет удобные инструменты для работы с классификацией ББК и УДК. Основные функциональные возможности включают:
1. Поиск классификаций по ключевым словам
Пользователь может искать коды ББК и УДК, вводя ключевые слова или категории.
Реализован фильтр, позволяющий находить записи, содержащие заданное слово в категории или описании.
Поддержка нечувствительности к регистру (поиск работает независимо от регистра букв).
Пример интерфейса:





2. Добавление новых классификаций
В веб-интерфейсе доступны формы для добавления новых записей ББК и УДК.
Для каждой записи указываются:
Код ББК/УДК
Категория
Ключевые слова для быстрого поиска
Данные сохраняются в базе SQLite.
Пример интерфейса:



3. Редактирование существующих записей
Возможность обновления информации по любой существующей классификации.
Редактирование кода, категории и ключевых слов без необходимости удаления записи.
Пример интерфейса:

4. Удаление записей
Возможность удаления устаревших или некорректных записей ББК и УДК.
Подтверждение удаления перед выполнением операции для предотвращения случайных действий.
5. Веб-интерфейс на Flask
Приложение работает через веб-браузер, обеспечивая удобный доступ к функционалу.
Страницы поиска, добавления, редактирования и удаления данных реализованы в шаблонах HTML.
Простая навигация между разделами.
6. Управление базой данных
Использование SQLAlchemy для взаимодействия с базой данных.
Автоматическое создание структуры базы при первом запуске приложения.
Гибкое расширение функционала за счет ORM.

			     Глава 2. Структура проекта
	Проект представляет собой веб-приложение на Flask, которое позволяет управлять записями ББК (Библиотечно-Библиографическая Классификация) и УДК (Универсальная Десятичная Классификация). В нем реализованы аутентификация пользователей, работа с базой данных и CRUD-операции.

1. Основные файлы проекта
app.py – главный файл приложения. В нем находятся:
Настройки приложения (Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt).
Определение моделей базы данных (User, BBK, UDK).
Определение маршрутов (роутов) и обработчиков запросов.
Логика аутентификации пользователей.
templates/ – папка с HTML-шаблонами.
bbk_index.html – отображение списка записей ББК.
udk.html – отображение списка записей УДК.
add_bbk.html и add_udk.html – формы для добавления новых записей.
edit_bbk.html и edit_udk.html – формы для редактирования существующих записей.
login.html и register.html – страницы входа и регистрации пользователей.
static/ – папка для статических файлов (CSS, JS, изображения).

2. Компоненты кода
2.1. Настройка Flask и зависимостей
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
Подключены библиотеки:
Flask – основной фреймворк.
Flask-SQLAlchemy – ORM для работы с базой данных.
Flask-Login – управление пользователями (вход/выход, защита страниц).
Flask-Bcrypt – хеширование паролей.
2.2. Настройки приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbk_udk.db'
app.config['SECRET_KEY'] = 'your_secret_key'
Используется база данных SQLite.
SECRET_KEY – секретный ключ для защиты сессий.

2.3. Модели базы данных
Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
Модель пользователя с полями id, username, password_hash.
Наследуется от UserMixin, чтобы использовать Flask-Login.
Модель ББК
class BBK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bbk_code = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)
Модель ББК с полями bbk_code, category, keywords.
Модель УДК
class UDK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    udk_code = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)
Аналогичная модель для УДК.
2.4. Аутентификация пользователей
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
Flask-Login загружает пользователя по id.

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверные данные", "danger")
    return render_template("login.html")
Пользователь вводит логин и пароль.
Проверяется хеш пароля.
В случае успеха вызывается login_user(user), и происходит перенаправление.

2.5. CRUD-операции для ББК и УДК
Добавление записи
@app.route("/add_bbk", methods=["GET", "POST"])
@login_required
def add_bbk():
    if request.method == "POST":
        bbk_code = request.form["bbk_code"]
        category = request.form["category"]
        keywords = request.form["keywords"]
        new_bbk = BBK(bbk_code=bbk_code, category=category, keywords=keywords)
        db.session.add(new_bbk)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_bbk.html")
Проверяется, авторизован ли пользователь.
Если метод POST, данные формы считываются и добавляются в базу.
Редактирование записи
@app.route("/edit_bbk/<int:id>", methods=["GET", "POST"])
@login_required
def edit_bbk(id):
    bbk = BBK.query.get_or_404(id)
    if request.method == "POST":
        bbk.bbk_code = request.form["bbk_code"]
        bbk.category = request.form["category"]
        bbk.keywords = request.form["keywords"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_bbk.html", bbk=bbk)
По id ищется запись в базе.
Если метод POST, вносятся изменения.


Удаление записи
@app.route("/delete_bbk/<int:id>", methods=["POST"])
@login_required
def delete_bbk(id):
    bbk = BBK.query.get_or_404(id)
    db.session.delete(bbk)
    db.session.commit()
    return redirect(url_for("index"))
Запись ищется в базе и удаляется.
2.6. Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)
Запускается веб-сервер в режиме отладки.
Глава 3. Python библиотеки,  использованные при создании веб-приложения  
Flask – веб-фреймворк
Библиотека: Flask Назначение: Позволяет создавать веб-приложения, управлять маршрутами (роутами), обрабатывать запросы и рендерить HTML-шаблоны.
Использование в коде:
from flask import Flask, render_template, request, redirect, url_for, flash
Flask – основной класс, создающий веб-приложение.
render_template – функция, загружающая HTML-шаблоны для отображения страниц.
request – объект для работы с HTTP-запросами (например, получение данных из формы).
redirect – перенаправление пользователя на другой маршрут.
url_for – генерация URL-адресов по именам маршрутов.
flash – механизм отправки временных сообщений пользователям.
Пример использования:
app = Flask(__name__)
@app.route("/")
def index():
    return "Привет, мир!"  # Простая веб-страница с текстом


2. Flask-SQLAlchemy – объектно-реляционное отображение (ORM)
Библиотека: Flask-SQLAlchemy Назначение: Позволяет работать с базой данных, используя объектно-ориентированную модель вместо написания SQL-запросов.
Использование в коде:
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
SQLAlchemy – объект базы данных, связанный с приложением.
Пример создания модели базы данных:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
db.Model – базовый класс для моделей.
db.Column – определение столбца в таблице базы данных.
db.Integer, db.String(80) – типы данных.
primary_key=True – определение первичного ключа.
nullable=False – запрет на пустые значения.
unique=True – требование уникальности значений.
Создание таблиц в базе данных:
with app.app_context():
    db.create_all()
Этот вызов создаст таблицы, если они еще не существуют.

3. Flask-Login – управление пользователями
Библиотека: Flask-Login Назначение: Управляет процессом аутентификации пользователей (вход, выход, защита страниц).
Использование в коде:
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
login_manager = LoginManager()
login_manager.init_app(app)
LoginManager – отвечает за управление сессиями пользователей.
UserMixin – добавляет к модели пользователя методы (is_authenticated, is_active и т. д.).
login_user(user) – выполняет вход пользователя.
logout_user() – завершает сессию пользователя.
login_required – декоратор, защищающий страницы от неавторизованных пользователей.
current_user – объект текущего пользователя.
Пример загрузки пользователя:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Загружает пользователя по ID



Пример защиты маршрута:
@app.route("/add_bbk", methods=["GET", "POST"])
@login_required  # Доступен только для авторизованных пользователей
def add_bbk():
    ...
4. Flask-Bcrypt – хеширование паролей
Библиотека: Flask-Bcrypt Назначение: Позволяет безопасно хранить пароли, хешируя их перед записью в базу данных.
Использование в коде:
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
Bcrypt.generate_password_hash(password).decode("utf-8") – хеширует пароль.
Bcrypt.check_password_hash(hashed_password, password) – проверяет соответствие пароля хешу.
Пример проверки пароля при входе:
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверные данные", "danger")
    return render_template("login.html")
5. Дополнительные функции Flask
Обработка данных из форм:
request.form["username"]  # Получение данных из формы
Использование flash-сообщений:
flash("Ошибка входа", "danger")  # Отправка уведомления пользователю

Перенаправление пользователей:
return redirect(url_for("index"))  # Перенаправление на главную страницу
