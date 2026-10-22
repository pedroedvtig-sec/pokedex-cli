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

def test_sem_apelido_e_recusado(monkeypatch):
    lista = [{'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']}]
    respostas_do_usuario(monkeypatch, 'pikachu', 'sem_apelido', 'teste')
    editar_pokemon(lista)
    assert lista == [{'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'],'apelido': 'teste'}]

def test_apelido_duplicado(monkeypatch):
    lista = [
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying'], 'apelido': 'fogo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric']}]
    respostas_do_usuario(monkeypatch, 'pikachu', 'fogo', 'choque')
    editar_pokemon(lista)
    assert lista == [
        {'nome': 'charizard', 'peso': 120, 'tipos': ['fire', 'flying'],'apelido': 'fogo'},
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'choque'}]