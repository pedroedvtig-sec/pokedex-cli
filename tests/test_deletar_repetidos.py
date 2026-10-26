from pokedex import deletar_pokemon
from test_api import respostas_do_usuario


def test_deletar_repetido_escolhendo_o_segundo(monkeypatch):
    lista = [
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogoooooo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'},
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
    ]
    respostas_do_usuario(monkeypatch, 'charizard', '2')
    deletar_pokemon(lista)

    assert lista == [
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogoooooo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'},
    ]


def test_deletar_repetido_escolhendo_o_primeiro(monkeypatch):
    lista = [
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogoooooo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'},
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
    ]
    respostas_do_usuario(monkeypatch, 'charizard', '1')
    deletar_pokemon(lista)

    assert lista == [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'},
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
    ]


def test_deletar_tres_repetidos_escolhendo_o_do_meio(monkeypatch):
    lista = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'a'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'b'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'c'},
    ]
    respostas_do_usuario(monkeypatch, 'pikachu', '2')
    deletar_pokemon(lista)

    assert lista == [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'a'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'c'},
    ]


def test_deletar_sem_repetido_nao_pede_numero(monkeypatch):
    lista = [
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'},
    ]
    respostas_do_usuario(monkeypatch, 'pikachu')
    deletar_pokemon(lista)

    assert lista == [
        {'nome': 'charizard', 'peso': 905, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
    ]

def test_deletar_repetidos_letras_em_int_e_numeros_invalidos(monkeypatch):
    lista = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'a'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'b'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'c'}
    ]
    respostas_do_usuario(monkeypatch, 'pikachu', 'a', '0', '-122', '999', '2')
    deletar_pokemon(lista)

    assert lista == [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'a'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'c'},
    ]
