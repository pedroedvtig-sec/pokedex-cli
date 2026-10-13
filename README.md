# Pokédex CLI

Pokédex de terminal em Python que consome a [PokéAPI](https://pokeapi.co/). É possível buscar um Pokémon pelo nome, capturá-lo com um apelido e listar, editar ou remover os capturados. Os dados ficam salvos em um arquivo JSON entre uma execução e outra.

Este projeto é parte dos meus estudos de Python. Com ele pratiquei consumo de API REST, persistência em JSON e as quatro operações de um CRUD.

## Funcionalidades

- **Capturar (Create):** busca o Pokémon na PokéAPI e salva nome, peso, tipos, até 3 habilidades e até 5 movimentos, além de um apelido opcional.
- **Listar (Read):** mostra os Pokémon capturados e seus apelidos.
- **Editar (Update):** troca o apelido de um Pokémon capturado.
- **Remover (Delete):** apaga um Pokémon da Pokédex.
- **Persistência:** tudo fica gravado em `pokemon.json`, que é carregado automaticamente ao iniciar.
- Tratamento de entrada: o menu aceita só números; buscas vazias são recusadas; maiúsculas e espaços extras são normalizados; nomes inexistentes na API pedem uma nova tentativa. Pokémon sem apelido aparecem como “sem apelido”.

## Como rodar

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/pedroedvtig-sec/pokedex-cli.git
cd pokedex-cli
pip install -r requirements.txt
python pokedex.py
```

## Exemplo de uso

```
=== Pokedex ===
1 - Listar Pokemóns capturados
2 - Capturar Pokemón
3 - Remover Pokemón
4 - Editar Pokemón
5 - Sair
Selecione uma opção:
2
Digite o nome do pokemon que você busca:
pikachu
```

## Tecnologias

- Python
- [requests](https://pypi.org/project/requests/) para as chamadas HTTP
- `json` (biblioteca padrão) para salvar os dados

## O que aprendi

- Fazer requisições HTTP e tratar o código de status da resposta, entendendo também que nem todo o código 200 é o que eu busco, significa que a requisição deu certo(aprendi isso ao perceber que se respondesse apenas um " " espaço no input de qual pokemón capturar, ele retornava status 200 e permitia seguir para a adição de apelidos).
- Ler e filtrar dados de um JSON aninhado vindo de uma API.
- Salvar e carregar dados em arquivo, inclusive no primeiro uso, quando o arquivo ainda não existe.
- Validar a entrada do usuário com `try/except` e laços de repetição.
- Usar .get substituindo if/else em casos especificos de dicionario e comparação de chaves.
- usar .strip() para tratar respostas com espaço adicionado no começo ou no final de inputs.


## Próximos passos

- [ ] Impedir a captura duplicada do mesmo Pokémon.
- [ ] Tratar falhas de conexão com a API (sem internet, tempo esgotado).
- [ ] Separar o código em módulos (API, armazenamento, menu).
- [ ] Escrever testes automatizados.
- [ ] Front-End.
