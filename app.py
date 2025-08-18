from flask import Flask, render_template, request

app = Flask(__name__)

# Тестовые данные аккаунтов
ACCOUNTS = [
    {"server": "Firemaw (EU)", "faction": "Альянс", "class": "Воин", "race": "Человек", "level": 60, "desc": "Эпический гир, готов к рейдам", "seller": "PlayerOne", "price": 3000},
    {"server": "Gehennas (EU)", "faction": "Орда", "class": "Маг", "race": "Орк", "level": 60, "desc": "Рейдовый шмот, MC/BWL", "seller": "BestSeller", "price": 4500},
    {"server": "Mirage Raceway (EU)", "faction": "Альянс", "class": "Жрец", "race": "Эльф", "level": 45, "desc": "Хороший хил для данжей", "seller": "HealerPro", "price": 2000},
    {"server": "Firemaw (EU)", "faction": "Орда", "class": "Разбойник", "race": "Нежить", "level": 50, "desc": "PvP шмот, готов к BG", "seller": "StealthMaster", "price": 2500},
]

@app.route("/")
def index():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)
