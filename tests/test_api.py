import requests

import api
from api import capturar_pokemon, get_pokemon


# Estas funções usam input() e a internet, duas coisas que um teste
# automático não pode usar. Então os testes trocam as duas por versões
# de mentira, só durante o teste, com o monkeypatch do pytest:
#   - input(): vira uma função que devolve respostas prontas, em ordem
#   - requests.get(): vira uma função que devolve uma resposta falsa,
#     sem acessar a PokéAPI de verdade


def respostas_do_usuario(monkeypatch, *respostas):
    """Faz o input() devolver estas respostas, uma por vez, em ordem."""
    fila = iter(respostas)
    monkeypatch.setattr("builtins.input", lambda mensagem="": next(fila))


class RespostaFalsa:
    """Imita o objeto que o requests.get() devolve."""

    def __init__(self, status_code, dados=None):
        self.status_code = status_code
        self._dados = dados

    def json(self):
        return self._dados


# Um pokémon no formato que a PokéAPI devolve (só com as chaves que o api.py usa)
PIKACHU_DA_API = {
    'name': 'pikachu',
    'weight': 60,
    'abilities': [
        {'ability': {'name': 'static'}},
        {'ability': {'name': 'lightning-rod'}},
        {'ability': {'name': 'habilidade-3'}},
        {'ability': {'name': 'habilidade-4'}},  # a 4ª deve ser ignorada ([:3])
    ],
    'moves': [{'move': {'name': f'movimento-{n}'}} for n in range(1, 8)],  # 7 movimentos
    'types': [{'type': {'name': 'electric'}}],
}


def api_que_conhece(monkeypatch, *nomes_existentes):
    """Faz o requests.get() responder 200 para estes nomes e 404 para o resto."""
    urls_pedidas = []

    def get_falso(url, *args, **kwargs):
        urls_pedidas.append(url)
        nome = url.rstrip("/").split("/")[-1]
        if nome in nomes_existentes:
            return RespostaFalsa(200, PIKACHU_DA_API)
        return RespostaFalsa(404)

    monkeypatch.setattr(api.requests, "get", get_falso)
    return urls_pedidas


def pokebola_que_cai(monkeypatch, *sorteios):
    """Faz cada random.random() devolver estes números, um por tentativa, em ordem.

    Também troca o time.sleep() por um que não espera nada,
    para os testes não ficarem 1,5 segundo parados em cada pokébola.
    Lembrete: no api.py, sorteio <= 0.6 pega; maior que 0.6 escapa.
    """
    fila = iter(sorteios)
    monkeypatch.setattr(api.random, "random", lambda: next(fila))
    monkeypatch.setattr(api.time, "sleep", lambda segundos: None)


# ---------- get_pokemon() ----------

def test_cancelar_com_n_devolve_none(monkeypatch):
    urls = api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "n")
    assert get_pokemon() is None
    assert urls == []  # cancelou antes de chamar a API


def test_campo_vazio_pede_de_novo(monkeypatch, capsys):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "", "   ", "n")
    assert get_pokemon() is None
    # capsys captura o que foi impresso com print()
    assert capsys.readouterr().out.count("Não deixe o campo vazio.") == 2


def test_nome_errado_pede_de_novo_ate_acertar(monkeypatch, capsys):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachuu", "pikachu")
    assert get_pokemon() == PIKACHU_DA_API
    assert "Pokemon não encontrado!" in capsys.readouterr().out


def test_maiusculas_e_espacos_sao_normalizados(monkeypatch):
    urls = api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "  PiKaChU  ")
    assert get_pokemon() == PIKACHU_DA_API
    assert urls == ["https://pokeapi.co/api/v2/pokemon/pikachu"]


def test_sem_internet_devolve_none(monkeypatch, capsys):
    def get_sem_internet(url, *args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(api.requests, "get", get_sem_internet)
    respostas_do_usuario(monkeypatch, "pikachu")
    assert get_pokemon() is None
    assert "Sem internet" in capsys.readouterr().out


# ---------- capturar_pokemon() ----------

def test_capturar_monta_o_dicionario_da_pokedex(monkeypatch):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu", "Pika")
    monkeypatch.setattr(api.random, "randint", lambda a, b: 2)
    pokebola_que_cai(monkeypatch, 0.1)  # pega de primeira
    assert capturar_pokemon([]) == {
        'nome': 'pikachu',
        'peso': 60,
        'habilidades': ['static', 'lightning-rod', 'habilidade-3'],  # só 3
        'tipos': ['electric'],
        'movimentos': ['movimento-1', 'movimento-2', 'movimento-3',
                       'movimento-4', 'movimento-5'],  # só 5
        'apelido': 'pika', 'shiny': True
    }


def test_capturar_sem_apelido(monkeypatch):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu", "")
    pokebola_que_cai(monkeypatch, 0.1)  # pega de primeira
    assert capturar_pokemon([])['apelido'] == ''


def test_capturar_cancelado_devolve_none(monkeypatch):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "n")
    assert capturar_pokemon([]) is None


def test_apelido_igual(monkeypatch):
    lista = [{'nome': 'pikachu','apelido': 'fogo'}]
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, 'pikachu', 'fogo', 'foguinho')
    pokebola_que_cai(monkeypatch, 0.1)  # pega de primeira

    novo_pokemon = capturar_pokemon(lista)

    assert novo_pokemon['apelido'] == 'foguinho'


def test_capturar_sem_shiny(monkeypatch):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu", "Pika")
    monkeypatch.setattr(api.random, "randint", lambda a, b: 4)
    pokebola_que_cai(monkeypatch, 0.1)  # pega de primeira
    assert capturar_pokemon([])['shiny'] is False


# ---------- chance de captura (3 tentativas) ----------

def test_pega_na_segunda_tentativa(monkeypatch, capsys):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu", "Pika")
    pokebola_que_cai(monkeypatch, 0.9, 0.3)  # 1ª escapa, 2ª pega

    novo_pokemon = capturar_pokemon([])

    assert novo_pokemon['nome'] == 'pikachu'
    saida = capsys.readouterr().out
    assert saida.count("Você jogou a pokebola") == 2
    assert "Restam 2 tentativas" in saida


def test_foge_depois_de_3_falhas(monkeypatch, capsys):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu")  # só o nome: fugiu, não pede apelido
    pokebola_que_cai(monkeypatch, 0.9, 0.7, 0.8)  # as 3 escapam

    assert capturar_pokemon([]) is None
    saida = capsys.readouterr().out
    assert saida.count("Você jogou a pokebola") == 3
    assert "Acabaram suas tentativas" in saida


def test_sorteio_exatamente_0_6_pega(monkeypatch):
    api_que_conhece(monkeypatch, "pikachu")
    respostas_do_usuario(monkeypatch, "pikachu", "Pika")
    pokebola_que_cai(monkeypatch, 0.6)  # a ponta da régua: <= 0.6 pega

    assert capturar_pokemon([]) is not None
