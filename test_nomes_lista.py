from lista_nomes import nomes_pokemon

def test_varios_pokemons():
    pokedex_teste = [{'nome': 'pikachu'}, {'nome': 'squirtle'}, {'nome': 'charizard'}]
    assert nomes_pokemon(pokedex_teste) == ['pikachu', 'squirtle', 'charizard']

def test_um_pokemon():
    pokemon_teste = [{'nome': 'jigglypuff'}]
    assert nomes_pokemon(pokemon_teste) == ['jigglypuff']

def test_pokedex_vazia():
    vazio_teste = []
    assert nomes_pokemon(vazio_teste) == []