from flask import Flask, render_template, request, session, flash, redirect
from main import addUser, addedUsers, removeUser, clearDatabase, tillChristmas, roll
from flask_session import Session
from tinydb import TinyDB, Query

app = Flask(__name__, static_folder="css")

#Session configuration
app.config['SECRET_KEY'] = 'r4d0m5k1'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


#Database configuration
db_users = TinyDB('db_users.json')


@app.route('/')
def home():
    if 'username' in session:
        if session['username'] == "admin":
            return redirect('users_config')
        else:
            return redirect('/lottery')
    else:
        return render_template('home.html', remainingDays=tillChristmas())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Sprawdzanie użytkownika w bazie TinyDB
        get = Query()
        user = db_users.get(get.participant == username)
        if user and user['password'] == password:
            # Zapisanie użytkownika w sesji
            session['username'] = username
            if username == 'admin':
                return redirect('/users_config')
            else:
                return redirect('/lottery')
        else:
            response = 'Niepoprawna nazwa użytkownika lub hasło'
            return render_template('login.html', result=response)
    else:
        return render_template('login.html')

@app.route('/lottery', methods=['GET', 'POST'])
def lottery():
    if request.method == 'POST':
        action = request.form.get("action")
        if action == "logout":
            session.clear()
            return redirect('/')
        if action == "roll":
            user = session['username']
            result = roll(user)
            return render_template('lottery.html', response=user, chosen=result, remainingDays=tillChristmas(), factor=True)
    else:
        user = session['username']
        get = Query()
        record = db_users.get(get.participant == user)
        if record['chosen'] != '':
            result = record['chosen']
            return render_template('lottery.html', response=user, chosen=result, factor=True, remainingDays=tillChristmas())
        else:
            return render_template('lottery.html', response=user, remainingDays=tillChristmas())


@app.route('/users_config', methods=['GET', 'POST'])
def modify_user():
    if request.method == 'POST':
        action = request.form.get("action")
        if action == "add":
            participant = request.form["inputName"]
            response = addUser(participant)
            added_users = addedUsers()
            return render_template('users_config.html', added_users=added_users, result=response)
        elif action == "remove":
            participant = request.form["inputName"]
            response = removeUser(participant)
            added_users = addedUsers()
            return render_template('users_config.html', added_users=added_users, result=response)
        elif action == "clear":
            response = clearDB()
            added_users = addedUsers()
            return render_template('users_config.html', added_users=added_users, result=response)
    else:
        added_users = addedUsers()
        return render_template('users_config.html', added_users=added_users)

def clearDB():
    clearDatabase()
    return "Baza danych została wyczyszczona"


if __name__ == '__main__':
     app.run(debug=True)