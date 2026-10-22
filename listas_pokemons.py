def nomes_pokemon(pokedex):
    nomes_poke = []
    for i in pokedex:
        nomes_poke.append(i['nome'])
    return nomes_poke

def apelido_poke(pokedex):
    apelido_poke = []
    for pokemon in pokedex:
        apelido = pokemon.get('apelido') or 'sem_apelido'
        apelido_poke.append(apelido)
    return apelido_poke