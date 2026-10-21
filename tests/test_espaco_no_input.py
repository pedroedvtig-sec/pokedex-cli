from pokedex import deletar_pokemon
from test_api import respostas_do_usuario

def test_so_espaco(monkeypatch):
    lista_de_teste = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']}
    ]
    respostas_do_usuario(monkeypatch, ' ', ' charizard')
    deletar_pokemon(lista_de_teste)
    assert lista_de_teste == [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
    ]

