from armazenamento import carregar_pokes
from armazenamento import salvar_pokes
from api import capturar_pokemon
from voz import falar
from hectogramas_para_kg import calculo
from listas_pokemons import nomes_pokemon
from listas_pokemons import apelido_poke

def listar_pokemon(pokedex):
    linhas = []
    for pokemon in pokedex:
        peso = calculo(pokemon['peso'])
        apelido = pokemon.get('apelido') or 'sem apelido'
        linhas.append(f"Nome do pokemón: {pokemon['nome']}\nApelido: {apelido}\nTipo: {', '.join(pokemon['tipos'])}\nPeso: {peso} kg\n")
    if linhas:
        print("Pokemóns capturados:")
        print("\n".join(linhas))
    else:
        print("Sem pokemóns na pokedéx! Capture")


def deletar_pokemon(pokedex):
    while pokedex:
        listar_pokemon(pokedex)
        nomes_poke = nomes_pokemon(pokedex)
        repeticao_pokemon = 0
        lista_repetidos = []
        qual_del = input("Digite qual pokemon deve ser deletado:\n").lower().strip()
        if qual_del in nomes_poke:
            for pokemon_contador in pokedex:
                if pokemon_contador['nome'] == qual_del:
                    lista_repetidos.append(pokemon_contador)
                    repeticao_pokemon += 1
            if repeticao_pokemon >= 2:
                print(f"Você tem {repeticao_pokemon} iguais na pokedex:\n")
                for numero, pokemon in enumerate(lista_repetidos, start=1):
                    print(f"{numero} - {pokemon['nome']} Apelido: {pokemon['apelido']}")
                while True:
                    try:
                        escolha = int(input("Escolha um id para remover o pokemon desejado!\n"))
                    except ValueError:
                        print("numeros apenas")
                        continue
                    if escolha <= repeticao_pokemon and escolha >= 1:
                        break
                    else:
                        print("Número inválido")
                pokemon_escolhido = lista_repetidos[escolha-1]
                pokedex.remove(pokemon_escolhido)
                print(f"Pokemón {pokemon_escolhido['nome']} removido!")
                return
            for pokemon in pokedex:
                if qual_del == pokemon['nome']:
                    pokedex.remove(pokemon)
                    print(f"Pokemon {qual_del} deletado!")
                    return
        else:
            print("Digite um pokemón que esteja na pokedex!")
    print("Sua pokedéx esta vazia, capture um pokemón para poder excluir")

def editar_pokemon(pokedex):
    while pokedex:
        listar_pokemon(pokedex)
        qualedit = input("Digite qual pokemón deve ser editado:\n").lower().strip()
        nomes_poke = nomes_pokemon(pokedex)
        apelidos = apelido_poke(pokedex)
        if qualedit in nomes_poke:
            apelido = input("Digite um apelido para seu pokemón:\n").lower().strip()
            while apelido in apelidos:
                apelido = input("digite outro apelido, este já está em uso:\n").lower().strip()
            for pokemon in pokedex:
                if qualedit == pokemon['nome']:
                    pokemon['apelido'] = apelido
                    print(f" segue o nome e o apelido do pokemon {pokemon['nome']}, {pokemon['apelido']}")
                    return

        else:
            print("Digite um pokemón que esteja na pokedex!")

    print("Capture um pokemón! Sua pokedéx está vazia")


def main():
    pokedex = carregar_pokes()
    while True:
        print(
            "=== Pokedex === \n1 - Listar Pokemóns capturados \n2 - Capturar Pokemón \n3 - Remover Pokemón \n4 - Editar Pokemón \n5 - Falar a pokedéx \n6 - Sair")
        try:
            opcao = int(input("Selecione uma opção:\n"))

        except ValueError:
            print("Digite apenas número, nem letra ou caractere especial")
            continue
        match opcao:
            case 1:
                listar_pokemon(pokedex)

            case 2:
                novo_pokemon = capturar_pokemon()
                if novo_pokemon is None:
                    continue
                pokedex.append(novo_pokemon)
                salvar_pokes(pokedex)

            case 3:
                deletar_pokemon(pokedex)
                salvar_pokes(pokedex)

            case 4:
                editar_pokemon(pokedex)
                salvar_pokes(pokedex)

            case 5:
                falar(pokedex)

            case 6:
                print("Finalizando programa...")
                break

            case _:
                print("Digite outro número!")

if __name__ == "__main__":
    main()