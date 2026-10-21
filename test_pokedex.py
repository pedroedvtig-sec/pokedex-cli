from pokedex import deletar_pokemon
from test_api import respostas_do_usuario


def test_deletar_depois_de_errar_o_nome(monkeypatch):
    #entendi que essa parte é o que imita a lista de dicionario pokedex
    lista_de_teste = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']},
    ]
    #essa prepara a fila que o input do usuário vai receber
    respostas_do_usuario(monkeypatch, 'mewtwo', 'charizard')
    #chama a função de delete e o argumento é a lista que criei acima, chama uma vez pra cada argumento e a lista anda conforme a chamada
    deletar_pokemon(lista_de_teste)
    #essa é a saida esperada, se eu colocar charizard, dá erro
    assert lista_de_teste == [{'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']}]

def test_deletar_pokemon_pokedex_vazia(monkeypatch):
    lista_vazia = []
    respostas_do_usuario(monkeypatch)
    deletar_pokemon(lista_vazia)

    assert lista_vazia == []