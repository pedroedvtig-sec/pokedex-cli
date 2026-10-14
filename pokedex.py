import requests

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

pokedex = carregar_pokes()

def get_pokemon():
    while True:
        pokemon = input("Digite o nome do pokemon que você busca:\n").lower().strip()
        if not pokemon:
            print("Não deixe o campo vazio.")
            continue
        resposta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if resposta.status_code == 200:
            return resposta.json()

        else:
            print("Pokemon não encontrado! Digite novamente")



def capturar_pokemon():
    info_pokemon = get_pokemon()
    print(f"pokemón capturado")
    primeiro_apelido = input("Digite um apelido para o pokemón:\n").lower().strip()

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
    return {'nome': nome, 'peso': peso, 'habilidades': habilidades, 'tipos': tipos, 'movimentos': movimentos, 'apelido': primeiro_apelido}

def listar_pokemon():
    print("Pokemóns capturados")
    linhas = []
    for i in pokedex:
        apelido = i.get('apelido') or 'sem apelido'
        linhas.append(f"Nome do pokemón: {i['nome']}\nApelido: {apelido}\nTipo: {', '.join(i['tipos'])}\nPeso: {i['peso']/10} kg\n")
    print("\n".join(linhas))

def deletar_pokemon():

    while pokedex:
        listar_pokemon()
        nomes_poke = []
        for i in pokedex:
            nomes_poke.append(i['nome'])
        qual_del = input("Digite qual pokemon deve ser deletado:\n").lower().strip()
        if qual_del in nomes_poke:
            for d in pokedex:
                if qual_del == d['nome']:
                    pokedex.remove(d)
                    print(f"Pokemon {qual_del} deletado!")
                    return
        else:
            print("Digite um pokemón que esteja na pokedex!")
    print("Sua pokedéx esta vazia, capture um pokemón para poder excluir")

def editar_pokemon():
    while pokedex:
        listar_pokemon()
        qualedit = input("Digite qual pokemón deve ser editado:\n").lower().strip()
        nomes_poke = []
        for i in pokedex:
            nomes_poke.append(i['nome'])
        if qualedit in nomes_poke:
            apelido = input("Digite um apelido para seu pokemón:\n").lower().strip()
            for a in pokedex:
                if qualedit == a['nome']:
                    a['apelido'] = apelido
                    print(f" segue o nome e o apelido do pokemon {a['nome']}, {a['apelido']}")
                    return

        else:
            print("Digite um pokemón que esteja na pokedex!")

    print("Capture um pokemón! Sua pokedéx está vazia")


while True:
    print("=== Pokedex === \n1 - Listar Pokemóns capturados \n2 - Capturar Pokemón \n3 - Remover Pokemón \n4 - Editar Pokemón \n5 - Sair")
    try:
        opcao = int(input("Selecione uma opção:\n"))

    except ValueError:
        print("Digite apenas número, nem letra ou caractere especial")
        continue
    if opcao == 1:
        listar_pokemon()

    elif opcao == 2:
        pokedex.append(capturar_pokemon())
        salvar_pokes(pokedex)

    elif opcao == 3:
        deletar_pokemon()
        salvar_pokes(pokedex)

    elif opcao == 4:
        editar_pokemon()
        salvar_pokes(pokedex)

    elif opcao == 5:
        print("Finalizando programa...")
        break
    else:
        print("Digite outro número!")
