import json

from armazenamento import carregar_pokes, salvar_pokes


# As funções de armazenamento gravam e leem o "pokemon.json" da pasta atual.
# Para não mexer na sua pokédex de verdade, cada teste roda dentro de uma
# pasta temporária vazia que o pytest cria e apaga sozinho:
#   - tmp_path: a pasta temporária (fixture do pytest)
#   - monkeypatch.chdir(tmp_path): "entra" nessa pasta só durante o teste


def test_carregar_sem_arquivo_devolve_lista_vazia(tmp_path, monkeypatch):
    # Primeiro uso do programa: o pokemon.json ainda não existe
    monkeypatch.chdir(tmp_path)
    assert carregar_pokes() == []


def test_salvar_e_carregar_devolve_a_mesma_pokedex(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pokedex_teste = [
        {'nome': 'pikachu', 'peso': 60, 'tipos': ['electric'], 'apelido': 'pika'},
        {'nome': 'ivysaur', 'peso': 130, 'tipos': ['grass', 'poison'], 'apelido': ''},
    ]
    salvar_pokes(pokedex_teste)
    assert carregar_pokes() == pokedex_teste


def test_salvar_pokedex_vazia(tmp_path, monkeypatch):
    # Ex.: o usuário removeu o último pokémon
    monkeypatch.chdir(tmp_path)
    salvar_pokes([])
    assert carregar_pokes() == []


def test_salvar_sobrescreve_o_arquivo_anterior(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    salvar_pokes([{'nome': 'pikachu'}, {'nome': 'squirtle'}])
    salvar_pokes([{'nome': 'squirtle'}])  # como depois de deletar o pikachu
    assert carregar_pokes() == [{'nome': 'squirtle'}]


def test_acentos_ficam_legiveis_no_arquivo(tmp_path, monkeypatch):
    # ensure_ascii=False: "Pokémon" fica "Pokémon" no arquivo, e não "Pokémon"
    monkeypatch.chdir(tmp_path)
    salvar_pokes([{'nome': 'flabébé', 'apelido': 'florzinha'}])
    texto = (tmp_path / "pokemon.json").read_text(encoding="utf-8")
    assert "flabébé" in texto
    assert json.loads(texto) == [{'nome': 'flabébé', 'apelido': 'florzinha'}]
