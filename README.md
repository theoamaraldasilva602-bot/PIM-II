# PIM-II - Sistema de Triagem de Edital (Faculdade UNIP: Universidade Paulista)
## Alunos (a):
`Kaique Souza Pereira RA: 2625068`


## Sobre o Projeto

Este projeto implementa um sistema de triagem de edital automatizado que processa documentos PDF e gera relatórios estruturados em JSON. O sistema utiliza processamento de dados para extrair informações relevantes de formulários de triagem e produzir análises padronizadas.

## Como Funciona

O sistema segue o seguinte fluxo:

1. **Entrada**: Recebe um arquivo PDF contendo informações de triagem de Editais
2. **Processamento**: Analisa o documento e extrai os dados relevantes
3. **Saída**: Gera um relatório estruturado em formato JSON com os resultados

## Como Usar

### Pré-requisitos

- Python 3.7 ou superior
- Dependências do projeto instaladas

### Executando o Sistema

Para processar um PDF e gerar o relatório, execute o seguinte comando:

```bash
export PYTHONPATH=$(pwd) && python3 prex_triagem/main.py > resultado.json
```

### Explicação do Comando

- `export PYTHONPATH=$(pwd)`: Define a variável de ambiente PYTHONPATH com o diretório atual, permitindo que os módulos do projeto sejam encontrados
- `python3 prex_triagem/main.py`: Executa o script principal do projeto
- `> resultado.json`: Redireciona a saída para um arquivo JSON contendo o relatório gerado

### Resultado

Após a execução, um arquivo `resultado.json` será criado contendo o relatório estruturado com as informações extraídas do PDF de triagem.

## Estrutura do Projeto

```
PIM-II-main/
├── prex_triagem/
│   ├── main.py          # Script principal
│   └── ...              # Módulos de processamento
├── README.md            # Este arquivo
└── resultado.json       # Arquivo de saída gerado
```

## Exemplos de Uso

```bash
# Copia um arquivo PDF da pasta de Downloads para a pasta de entrada do projeto
# Substitua "nome_do_arquivo.pdf" pelo nome do seu arquivo
cp ~/Downloads/nome_do_arquivo.pdf ./prex_triagem/data/pdfs_entrada/
```

Para processar uma triagem e salvar o resultado:

```bash
export PYTHONPATH=$(pwd) && python3 prex_triagem/main.py > resultado.json
```

```bash
export PYTHONPATH=$(pwd) && python3 prex_triagem/main.py
#Comentário do comando acima:

#Define o diretório atual como `PYTHONPATH` para que o Python encontre os módulos do projeto.
#Executa o arquivo principal `prex_triagem/main.py`.
#Mostra o resultado da execução no terminal.
#Esse comando define o diretório atual como caminho de importação do Python e executa o arquivo principal do projeto `prex_triagem/main.py`.
#O arquivo `resultado.json` conterá a análise completa em formato estruturado.
```
