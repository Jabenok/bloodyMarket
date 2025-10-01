from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User
from database import db
import config

app = Flask(__name__)
app.secret_key = config.Config.SECRET_KEY

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_value = request.form["username"]
        password = request.form["password"]

        user = User.get_by_credentials(login_value, password)

        if user:
            login_user(user)
            session["user_id"] = user.id
            session["login"] = user.name
            flash("Вы успешно вошли!", "success")
            return redirect(url_for("index"))
        else:
            flash("Неверный логин или пароль", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_value = request.form["username"]
        password = request.form["password"]

        if User.get_by_username(login_value):
            flash("Пользователь с таким логином уже существует", "error")
            return redirect(url_for("register"))

        User.create(login_value, password)
        flash("Регистрация прошла успешно!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Вы вышли из системы", "success")
    return redirect(url_for("index"))

# Тестовые данные аккаунтов
ACCOUNTS = [
    {"server": "Firemaw (EU)", "faction": "Альянс", "class": "Воин", "race": "Человек", "level": 60, "desc": "Эпический гир, готов к рейдам", "seller": "PlayerOne", "price": 3000},
    {"server": "Gehennas (EU)", "faction": "Орда", "class": "Маг", "race": "Орк", "level": 60, "desc": "Рейдовый шмот, MC/BWL", "seller": "BestSeller", "price": 4500},
]

@app.route("/accounts")
def accounts():
    # Получаем фильтры из запроса
    server = request.args.get("server", "")
    faction = request.args.get("faction", "")
    player_class = request.args.get("class", "")
    race = request.args.get("race", "")
    level_min = request.args.get("level_min", type=int)
    level_max = request.args.get("level_max", type=int)

    # Фильтрация
    filtered_accounts = []
    for acc in ACCOUNTS:
        if server and server not in acc["server"]:
            continue
        if faction and faction != acc["faction"]:
            continue
        if player_class and player_class != acc["class"]:
            continue
        if race and race != acc["race"]:
            continue
        if level_min and acc["level"] < level_min:
            continue
        if level_max and acc["level"] > level_max:
            continue
        filtered_accounts.append(acc)

    return render_template("accounts.html", accounts=filtered_accounts)

@app.route("/gold")
def gold():
    return render_template("gold.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug=True)