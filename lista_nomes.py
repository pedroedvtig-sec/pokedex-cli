def nomes_pokemon(pokedex):
    nomes_poke = []
    for i in pokedex:
        nomes_poke.append(i['nome'])
    return nomes_poke