from armazenamento import carregar_pokes
from armazenamento import salvar_pokes
from api import capturar_pokemon
from voz import falar
from hectogramas_para_kg import calculo
from lista_nomes import nomes_pokemon

pokedex = carregar_pokes()


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

#Código	                            Como ler
#def deletar_pokemon(pokedex):	    “Para deletar um pokémon, eu preciso receber uma pokédex.”
#deletar_pokemon(pokedex)	        “Deleta um pokémon desta pokédex aquiss.”
#deletar_pokemon(lista_de_teste)	“Deleta um pokémon desta outra pokédex.”


def deletar_pokemon(pokedex):

    while pokedex:
        listar_pokemon(pokedex)
        nomes_poke = nomes_pokemon(pokedex)
        qual_del = input("Digite qual pokemon deve ser deletado:\n").lower().strip()
        if qual_del in nomes_poke:
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
        if qualedit in nomes_poke:
            apelido = input("Digite um apelido para seu pokemón:\n").lower().strip()
            for pokemon in pokedex:
                if qualedit == pokemon['nome']:
                    pokemon['apelido'] = apelido
                    print(f" segue o nome e o apelido do pokemon {pokemon['nome']}, {pokemon['apelido']}")
                    return

        else:
            print("Digite um pokemón que esteja na pokedex!")

    print("Capture um pokemón! Sua pokedéx está vazia")

if __name__ == "__main__":
    while True:
        print("=== Pokedex === \n1 - Listar Pokemóns capturados \n2 - Capturar Pokemón \n3 - Remover Pokemón \n4 - Editar Pokemón \n5 - Falar a pokedéx \n6 - Sair")
        try:
            opcao = int(input("Selecione uma opção:\n"))

        except ValueError:
            print("Digite apenas número, nem letra ou caractere especial")
            continue
        if opcao == 1:
            listar_pokemon(pokedex)

        elif opcao == 2:
            novo_pokemon = capturar_pokemon()
            if novo_pokemon is None:
                continue
            pokedex.append(novo_pokemon)
            salvar_pokes(pokedex)

        elif opcao == 3:
            deletar_pokemon(pokedex)
            salvar_pokes(pokedex)

        elif opcao == 4:
            editar_pokemon(pokedex)
            salvar_pokes(pokedex)


        elif opcao == 5:
            falar(pokedex)

        elif opcao == 6:
            print("Finalizando programa...")
            break

        else:
            print("Digite outro número!")
