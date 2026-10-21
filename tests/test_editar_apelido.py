from pokedex import editar_pokemon
from test_api import respostas_do_usuario

def test_editar_errando_nome(monkeypatch):
    lista = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']}]
    respostas_do_usuario(monkeypatch, 'mewtwo', ' pikachu ', 'choque2')
    editar_pokemon(lista)

    assert lista == [
        { 'apelido': 'choque2', 'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']}]

def test_editar_vazio(monkeypatch):
    lista = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']}]
    respostas_do_usuario(monkeypatch, ' ', ' pikachu ', ' ')
    editar_pokemon(lista)

    assert lista == [
        { 'apelido': '', 'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']},
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying']}]