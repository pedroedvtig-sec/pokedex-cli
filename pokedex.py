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
        pokemon = input("Digite o nome do pokemon que você busca:\n")
        resposta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if resposta.status_code == 200:
            return resposta.json()

        else:
            print("Pokemon não encontrado! Digite novamente")



def capturar_pokemon():
    info_pokemon = get_pokemon()
    print(f"pokemón capturado")
    apelido_nao = True
    while apelido_nao:
        apelido_nao = False
        verifi = input("Quer apelidar seu Pokemón? Digite s ou n:\n").lower()
        if verifi == 's':
            primeiro_apelido = input("Digite um apelido para o pokemón:\n").lower()
            for i in pokedex:
                if i == info_pokemon['name']:
                    i['apelido'] = primeiro_apelido
        elif verifi == 'n':
            continue
        else:
            apelido_nao = True
            print("Digite s ou n")

    nome = info_pokemon['name']
    peso = info_pokemon['weight']
    habilidades = []
    for a in info_pokemon['abilities'][:3]:
        habilidades.append(a['ability']['name'])
    #print(f"{', '.join(habilidades)}")
    movimentos = []
    for m in info_pokemon['moves'][:5]:
        movimentos.append(m['move']['name'])
    #print(f"{', '.join(movimentos)}")
    tipos = []
    for t in info_pokemon['types'][:5]:
        tipos.append(t['type']['name'])
    #print(f"{', '.join(tipos)}")
    return {'nome': nome, 'peso': peso, 'habilidades': habilidades, 'tipos': tipos, 'movimentos': movimentos, 'apelido': primeiro_apelido}

def listar_pokemon():
    print("Pokemóns capturados")
    nomes_poke = []
    apelidos_poke = []
    for i in pokedex:
        nomes_poke.append(i['nome'])
        apelidos_poke.append(i['nome'])
        apelidos_poke.append(i['apelido'])
    #print(", ".join(nomes_poke))
    print(", apelido do pokemón: ".join(apelidos_poke))
    # peso_poke = []
    # for p in pokedex:
    # peso_poke.append(p['peso'])
    # print(f"{', '.join(peso_poke)}")
    # terminar

def deletar_pokemon():

    while pokedex:
        listar_pokemon()
        nomes_poke = []
        for i in pokedex:
            nomes_poke.append(i['nome'])
        qual_del = input("Digite qual pokemon deve ser deletado:\n").lower()
        if qual_del in nomes_poke:
            for d in pokedex:
                if qual_del == d['nome']:
                    pokedex.remove(d)  #preciso fazer com que o computador entenda que eu quero excluir o qual_id do d['nome'], não todos os pokemons
                    print(f"Pokemon {qual_del} deletado!")
                    return
        else:
            print("Digite um pokemón que esteja na pokedex!")
    print("Sua pokedéx esta vazia, capture um pokemón para poder excluir")

def editar_pokemon():
    while pokedex:
        listar_pokemon()
        qualedit = input("Digite qual pokemón deve ser editado:\n").lower()
        nomes_poke = []
        for i in pokedex:
            nomes_poke.append(i['nome'])
        if qualedit in nomes_poke:
            apelido = input("Digite um apelido para seu pokemón:\n").lower()
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

    elif opcao == 6:
        lista = []
        lista.append(111)
        dicio = [{"nome" : "oi"}]
        print(lista)
        print(dicio[0]['nome'])
        print(pokedex['apelido'])

    elif opcao == 5:
        print("Finalizando programa...")
        break
    else:
        print("Digite outro número!")
