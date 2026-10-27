import requests
from listas_pokemons import apelido_poke
import random
import time

def get_pokemon():
    while True:
        pokemon = input("Digite o nome do pokemon que você busca ou digite 'n' para não capturar nada:\n").lower().strip()
        if not pokemon:
            print("Não deixe o campo vazio.")
            continue
        elif pokemon == "n":
            print("cancelando captura")
            return
        try:
            resposta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")

        except requests.exceptions.ConnectionError:
            print("Sem internet, conecte a uma rede")
            return
        if resposta.status_code == 200:
            return resposta.json()
        else:
            print("Pokemon não encontrado! Digite novamente")


def capturar_pokemon(pokedex):
    info_pokemon = get_pokemon()
    if info_pokemon is None:
        return
    dado = random.randint(1,5)
    chance = 2
    shiny = dado == chance
    if shiny:
        print("✨ Este é um pokemon Shiny!✨")
    tentativas = 3
    while tentativas > 0:
        print("Você jogou a pokebola...")
        time.sleep(1.5)
        sorteio = random.random()
        if sorteio <= 0.6:
            print("pokemón capturado")
            apelidos = apelido_poke(pokedex)
            primeiro_apelido = input("Digite um apelido para o pokemón:\n").lower().strip()
            while primeiro_apelido in apelidos:
                primeiro_apelido = input("digite outro apelido, este já está em uso:\n").lower().strip()
            nome = info_pokemon['name']
            peso = info_pokemon['weight']
            habilidades = []
            for a in info_pokemon['abilities'][:3]:
                habilidades.append(a['ability']['name'])
            movimentos = []
            for m in info_pokemon['moves'][:5]:
                movimentos.append(m['move']['name'])
            tipos = []
            for t in info_pokemon['types'][:5]:
                tipos.append(t['type']['name'])
            return {'nome': nome, 'peso': peso, 'habilidades': habilidades, 'tipos': tipos, 'movimentos': movimentos, 'apelido': primeiro_apelido, 'shiny': shiny}
        elif sorteio > 0.6:
            tentativas -=1
            print(f"Restam {tentativas} tentativa(s)")
    print("Acabaram suas tentativas, tente capturar novamente")
    return