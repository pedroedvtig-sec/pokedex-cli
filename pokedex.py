import wave
import subprocess
from piper import PiperVoice

from armazenamento import carregar_pokes
from armazenamento import salvar_pokes
from api import capturar_pokemon

pokedex = carregar_pokes()


def falar():
    if pokedex:
        motor = PiperVoice.load("pt_BR-jeff-medium.onnx")
        for i in pokedex:
            apelido = i.get('apelido') or 'sem apelido'
            with wave.open("pokedex.wav", "wb") as arquivo:
                motor.synthesize_wav(f"Pokemón: {i['nome']} Apelido: {apelido} Tipo: {', '.join(i['tipos'])} Peso: {i['peso']/10} kg", arquivo)
            subprocess.run(["paplay", "pokedex.wav"])
    else:
        print("A pokedex está vazia, capture um pokemón para que o programa possa ler e falar.")

def listar_pokemon():
    linhas = []
    for i in pokedex:
        apelido = i.get('apelido') or 'sem apelido'
        linhas.append(f"Nome do pokemón: {i['nome']}\nApelido: {apelido}\nTipo: {', '.join(i['tipos'])}\nPeso: {i['peso'] / 10} kg\n")
    if linhas:
        print("Pokemóns capturados:")
        print("\n".join(linhas))
    else:
        print("Sem pokemóns na pokedéx! Capture")

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
    print("=== Pokedex === \n1 - Listar Pokemóns capturados \n2 - Capturar Pokemón \n3 - Remover Pokemón \n4 - Editar Pokemón \n5 - Falar a pokedéx \n6 - Sair")
    try:
        opcao = int(input("Selecione uma opção:\n"))

    except ValueError:
        print("Digite apenas número, nem letra ou caractere especial")
        continue
    if opcao == 1:
        listar_pokemon()

    elif opcao == 2:
        novo_pokemon = capturar_pokemon()
        if novo_pokemon is None:
            continue
        pokedex.append(novo_pokemon)
        salvar_pokes(pokedex)

    elif opcao == 3:
        deletar_pokemon()
        salvar_pokes(pokedex)

    elif opcao == 4:
        editar_pokemon()
        salvar_pokes(pokedex)


    elif opcao == 5:
        falar()

    elif opcao == 6:
        print("Finalizando programa...")
        break

    else:
        print("Digite outro número!")
