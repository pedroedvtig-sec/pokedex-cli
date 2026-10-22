# Pokédex CLI

Pokédex de terminal em Python que consome a [PokéAPI](https://pokeapi.co/). É possível buscar um Pokémon pelo nome, capturá-lo com um apelido e listar, editar ou remover os capturados. Os dados ficam salvos em um arquivo JSON entre uma execução e outra, e a Pokédex pode ser lida em voz alta.

Este projeto é parte dos meus estudos de Python. Com ele pratiquei consumo de API REST, persistência em JSON, as quatro operações de um CRUD, organização do código em módulos e testes automatizados com pytest.

## Funcionalidades

- **Capturar (Create):** busca o Pokémon na PokéAPI e salva nome, peso, tipos, até 3 habilidades e até 5 movimentos, além de um apelido opcional. Digitar `n` cancela a captura.
- **Listar (Read):** mostra os Pokémon capturados com apelido, tipos e peso em kg.
- **Editar (Update):** troca o apelido de um Pokémon capturado.
- **Remover (Delete):** apaga um Pokémon da Pokédex.
- **Falar a Pokédex:** lê em voz alta nome, apelido, tipos e peso de cada Pokémon capturado, com uma voz neural em português gerada localmente pelo [Piper](https://github.com/OHF-Voice/piper1-gpl), sem internet.
- **Persistência:** tudo fica gravado em `pokemon.json`, que é carregado automaticamente ao iniciar.
- **Peso em kg:** a PokéAPI devolve o peso em hectogramas. O programa converte para kg e mostra `6 kg` em vez de `6.0 kg` quando a divisão é exata.
- **Tratamento de entrada e de erros:** o menu aceita só números; buscas vazias são recusadas; maiúsculas e espaços extras são normalizados; nomes inexistentes na API pedem uma nova tentativa; sem internet, o programa avisa e volta ao menu em vez de quebrar. Pokémon sem apelido aparecem como “sem apelido”.

## Como rodar

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/pedroedvtig-sec/pokedex-cli.git
cd pokedex-cli
pip install -r requirements.txt
python -m piper.download_voices pt_BR-jeff-medium
python pokedex.py
```

O comando `piper.download_voices` baixa a voz usada na opção de falar (cerca de 60 MB) para a pasta do projeto. Ele só precisa ser rodado uma vez. O arquivo da voz (`.onnx`) não fica no repositório por causa do tamanho.

Para tocar o áudio, o programa usa o `paplay`, que já vem na maioria das distribuições Linux. Se ele não estiver instalado:

```bash
sudo apt install pulseaudio-utils
```

## Testes

O projeto tem testes automatizados com [pytest](https://docs.pytest.org/), que ficam na pasta `tests/`. Para rodar todos, na pasta principal do projeto:

```bash
pytest
```

```
25 passed
```

Os testes não usam a internet nem o `pokemon.json` de verdade:

- **`test_nomes_lista.py`** e **`test_hectogramas_para_kg.py`:** testes unitários das funções que recebem um valor e devolvem outro (lista de nomes e conversão de peso), incluindo os casos “não bonitos”, como Pokédex vazia e peso que não termina em zero.
- **`test_armazenamento.py`:** salva e carrega a Pokédex dentro de uma pasta temporária (`tmp_path`), incluindo o primeiro uso, quando o arquivo ainda não existe.
- **`test_api.py`:** usa o `monkeypatch` do pytest para trocar o `input()` por respostas prontas e o `requests.get()` por uma resposta falsa. Assim dá para testar cancelar com `n`, campo vazio, nome errado, falta de internet e o dicionário montado na captura, sem chamar a PokéAPI.
- **`test_pokedex.py`:** testa o remover. Uma lista de teste no mesmo formato da Pokédex real e uma fila de respostas no lugar do `input()`: o usuário erra o nome, o programa pede de novo e remove o certo; e, com a Pokédex vazia, o programa avisa sem perguntar nada.
- **`test_voz.py`:** confere o aviso quando a Pokédex está vazia, sem carregar a voz nem tocar áudio.

O arquivo `pytest.ini` diz ao pytest que os testes estão em `tests/` e que o código fica na pasta principal, para os `import` dos testes encontrarem os módulos.

## Estrutura do projeto

```
pokedex-cli/
├── pokedex.py              # menu e funções de listar, remover e editar
├── api.py
├── armazenamento.py
├── voz.py
├── lista_nomes.py
├── hectogramas_para_kg.py
├── tests/                  # testes automatizados (pytest)
├── pytest.ini
├── requirements.txt
└── README.md
```

| Arquivo | O que faz |
|---|---|
| `pokedex.py` | Menu principal e as funções de listar, remover e editar |
| `api.py` | Busca na PokéAPI e monta o Pokémon capturado |
| `armazenamento.py` | Salva e carrega a Pokédex no `pokemon.json` |
| `voz.py` | Lê a Pokédex em voz alta com o Piper |
| `listas_pokemons.py` | Monta a lista com os nomes dos Pokémon capturados |
| `hectogramas_para_kg.py` | Converte o peso de hectogramas para kg |
| `tests/` | Testes automatizados (pytest) |
| `pytest.ini` | Configuração do pytest: onde estão os testes e o código |

## Exemplo de uso

```
=== Pokedex ===
1 - Listar Pokemóns capturados
2 - Capturar Pokemón
3 - Remover Pokemón
4 - Editar Pokemón
5 - Falar a pokedéx
6 - Sair
Selecione uma opção:
2
Digite o nome do pokemon que você busca ou digite 'n' para não capturar nada:
pikachu
```

## Tecnologias

- Python
- [requests](https://pypi.org/project/requests/) para as chamadas HTTP
- `json` (biblioteca padrão) para salvar os dados
- [Piper](https://github.com/OHF-Voice/piper1-gpl) (`piper-tts`) para gerar a voz, com `wave` e `subprocess` (biblioteca padrão) para gravar e tocar o áudio
- [pytest](https://docs.pytest.org/) para os testes automatizados

## O que aprendi

- Fazer requisições HTTP e tratar o código de status da resposta, entendendo também que nem todo o código 200 é o que eu busco, significa que a requisição deu certo(aprendi isso ao perceber que se respondesse apenas um " " espaço no input de qual pokemón capturar, ele retornava status 200 e permitia seguir para a adição de apelidos).
- Ler e filtrar dados de um JSON aninhado vindo de uma API.
- Salvar e carregar dados em arquivo, inclusive no primeiro uso, quando o arquivo ainda não existe.
- Validar a entrada do usuário com `try/except` e laços de repetição.
- Usar .get substituindo if/else em casos especificos de dicionario e comparação de chaves.
- usar .strip() para tratar respostas com espaço adicionado no começo ou no final de inputs.
- Tratar a falta de internet com `try/except` e `requests.exceptions.ConnectionError`, e usar `None` (com `is None`) para avisar que a captura foi cancelada.
- Separar o código em módulos e importar cada função de onde ela mora (`from arquivo import funcao`).
- Criar funções que recebem um valor e devolvem outro com `return`, para não repetir código (ex.: `nomes_pokemon()`).
- Entender que um `return` dentro do `for` encerra a função na primeira volta do laço, e que uma função que termina sem `return` devolve `None`.
- Escrever testes com pytest seguindo o padrão preparar, executar e conferir (Arrange, Act, Assert), e entender por que testar com 3 casos: com um Pokémon só, o bug do `return` dentro do `for` passava despercebido; só os casos com vários Pokémon e com a Pokédex vazia mostraram o erro.
- Que importar um arquivo roda o arquivo inteiro (por isso o menu começou a rodar dentro do pytest).
- Ler a saída do pytest (`Expected` × `Actual`) e decidir quem está errado: o código ou o teste.
- Proteger o menu com `if __name__ == "__main__":`, para ele só rodar quando executo o `pokedex.py` e não quando ele é importado pelos testes.
- Fazer as funções receberem a Pokédex por parâmetro em vez de usar uma variável de fora escondida, o que também permitiu testá-las com uma lista de teste.
- Testar uma função sem `return` (como o remover) conferindo a lista depois, já que ela é a mesma lista que foi entregue, e não uma cópia.
- Fazer  o `assert` errar de propósito para provar que um teste que passou de primeira também sabe falhar.
- Separar os testes numa pasta própria e configurar o `pythonpath` do pytest, depois de ver o `ModuleNotFoundError` que a mudança causou.

## Próximos passos

- [x] Separar o código em módulos (API, armazenamento, menu).
- [x] Tratar falta de internet ao buscar na API.
- [ ] Definir tempo máximo de espera (`timeout`) nas chamadas à API.
- [x] Escrever testes automatizados para as funções de API, armazenamento, conversão de peso e lista de nomes.
- [x] Fazer o menu parar de rodar quando o `pokedex.py` é importado.
- [x] Organizar os testes na pasta `tests/`.
- [ ] Terminar os testes do remover (ex.: usuário digita só espaço).
- [ ] Testar o editar.
- [ ] Rodar os testes automaticamente a cada push (GitHub Actions).
- [ ] Impedir a captura duplicada do mesmo Pokémon.
- [ ] Remover um Pokémon pelo apelido.
- [ ] Trocar o JSON por um banco de dados SQLite.
- [ ] Front-End.
