from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

# Obtener Pokémon desde la PokeAPI
def obtener_pokemon(nombre_o_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon = {
            "id": data["id"],
            "nombre": data["name"].capitalize(),
            "tipo": [t["type"]["name"].capitalize() for t in data["types"]],
            "imagen": data["sprites"]["front_default"],
            "altura": f"{data['height'] / 10} m",
            "peso": f"{data['weight'] / 10} kg",
            "habilidades": [h["ability"]["name"].capitalize() for h in data["abilities"]],
            "estadisticas": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        }
        return pokemon
    else:
        return None

# 🟡 /pokemon → muestra 10 Pokémon aleatorios
@app.route("/pokemon")
def mostrar_10():
    pokemones = []
    ids = random.sample(range(1, 152), 10)  # 10 Pokémon únicos del 1 al 151
    for i in ids:
        pokemon = obtener_pokemon(i)
        if pokemon:
            pokemones.append(pokemon)
    return render_template("pokemon.html", pokemones=pokemones)

# 🔵 /pokemon/<nombre_o_id> → por nombre o ID
@app.route("/pokemon/<nombre_o_id>")
def mostrar_pokemon(nombre_o_id):
    if nombre_o_id.startswith("cantidad"):
        return render_template("404.html"), 404

    pokemon = obtener_pokemon(nombre_o_id.lower())
    if pokemon:
        return render_template("pokemon.html", pokemones=[pokemon])
    else:
        return render_template("404.html"), 404

# 🟣 /pokemon/cantidad/<int:num> → muestra N Pokémon aleatorios
@app.route("/pokemon/cantidad/<int:num>")
def mostrar_cantidad(num):
    num = min(num, 151)  # evitar pedir más de 151
    ids = random.sample(range(1, 152), num)
    pokemones = []

    for i in ids:
        pokemon = obtener_pokemon(i)
        if pokemon:
            pokemones.append(pokemon)
    return render_template("pokemon.html", pokemones=pokemones)

# 🔴 Página de error
@app.errorhandler(404)
def pagina_no_encontrada(_):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
