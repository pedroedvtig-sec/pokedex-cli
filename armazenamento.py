import json

def salvar_pokes(pokedex):
    with open("pokemon.json", "w", encoding="utf-8") as arquivo:
        json.dump(pokedex, arquivo, ensure_ascii=False, indent=4)

def carregar_pokes():
    try:
        with open("pokemon.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []