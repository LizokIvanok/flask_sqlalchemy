# sqlalchemy
# базы данных нужны для хранения какой-либо информации
# есть много видов баз данных, например MySQL, PostgreSQL, SQLite, Oracle и тд
# будем пользоваться SQLite, тк она уже встроена в питон

# план работы над сервисом регистрации
# 1. создание структуры веб-сервиса (не сайт!!)
# 2. создание html-шаблонов для веб-сервиса и стилей
# 3. создание базы данных
# 4. создание механизма авторизации

# ORM - технология, которая позволяет создавать объекты в таблице в виде объектов, а не строк

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static') # веб-сервис (приложение)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
database = SQLAlchemy(app) # база данных
locked = True

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True) # порядковый номер пользователя
    email = database.Column(database.String(50), unique=True) # электронный адрес пользователя
    password = database.Column(database.String(50), nullable=True) # пароль пользователя
    date = database.Column(database.DateTime, default=datetime.utcnow) # дата регистрации

        #represent
    def __repr__(self):
        return f"users {self.id}"

class Profiles(database.Model):
    id = database.Column(database.Integer, primary_key=True) # порядковый номер пользователя
    name = database.Column(database.String(100), nullable=True) # имя пользователя
    old = database.Column(database.Integer) # возраст пользователя
    city = database.Column(database.String(100)) # город пользователя

    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def __repr__(self):
        return f"profiles {self.id}"

with app.app_context(): 
    database.create_all() # создание базы данных

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        try:
            user = Users(email=request.form['email'], password=request.form['password'])
            print(1)
            database.session.add(user)
            print(2)
            database.session.flush()
            print(3)

            profile = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id=user.id)
            print(4)
            database.session.add(profile)
            
            print(5)
            print(user, profile)
            database.session.commit()
            print(6)
        except:
            database.session.rollback()
            print('Ошибка бд')

    return render_template('index.html')

@app.route("/second")
def second():
    global locked
    if locked == False:
        return render_template('page.html')
    else:
        return redirect('/login')

@app.route("/skam")
def skam():
    return redirect('https://youtu.be/dQw4w9WgXcQ?si=GAxn7pYQ3jmzmc7I')

@app.route('/login', methods=('GET', 'POST'))
def login():
    global locked
    if request.method == 'POST':
        # система смотрит в базу данных и находит первое совпадение по email и паролю
        user = Users.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            locked = False
            return redirect('/second')
        else:
            return render_template('login.html', result='неправильный логин или пароль')
    return render_template('login.html', result='не вошёл :(((')

if __name__ == '__main__':
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/second', 'page', second)
    app.add_url_rule('/skam', 'skam', skam)
    app.add_url_rule('/login', 'login', login)
    app.run(debug=True, port=8080)
