### SCTec
## SalesInsight_PY_Ademir_Schiestl_QADBEN202629
## SalesInsight PY — análise e visualização de dados de vendas.

**Estudante:** Ademir Schiestl  
**Turma:** QADBEN202629  
**Atividade:** Módulo 01 / Semana 07

## Sobre o meu projeto
Neste projeto, meu objetivo é aplicar os conteúdos estudados no módulo para analisar dados de vendas com Python. Organizei um fluxo que carrega os dados, verifica sua estrutura, trata os registros inválidos e calcula informações sobre vendas, produtos, categorias, regiões e clientes.

Utilizei uma base de vendas fictícias para demonstrar as etapas. A análise é descritiva: procuro entender os dados disponíveis, sem construir um modelo de previsão.

## Como executar
Para executar meu projeto localmente, é necessário ter o Python 3.10 ou superior. Os comandos abaixo devem ser executados no terminal, dentro da pasta do projeto:

```bash
python -m pip install "pandas>=2.0" "numpy>=1.24" "matplotlib>=3.7" "seaborn>=0.13"
python salesinsight.py
```

No Windows, caso o comando `python` não esteja disponível, é possível usar `py` nos dois comandos.

### Execução no Google Colab
Também é possível executar o projeto no Google Colab. Para isso, basta enviar os arquivos `salesinsight.py` e `vendas.csv` para a área de arquivos do notebook e executar:

```python
!python salesinsight.py
```

O Colab normalmente já possui as bibliotecas utilizadas. Os resultados são salvos na pasta `outputs`, ao lado do arquivo Python. Para visualizar os gráficos, basta atualizar a lista de arquivos e abrir a pasta `outputs/graficos`.

## Conceitos que apliquei
Ao organizar o código, procurei utilizar os conceitos trabalhados no módulo:

- Variáveis, tipos de dados, operadores, condicionais, laços, listas e dicionários.
- Funções com parâmetros, retorno e uma breve descrição do que fazem.
- A classe `AnalisadorDeVendas` para organizar as etapas e guardar os resultados.
- Funções lambda para classificar clientes e transformar colunas.
- A função `processar_coluna`, que recebe outra função como argumento.
- Pandas para trabalhar com DataFrames, ler e salvar CSVs, inspecionar os dados, converter tipos e fazer agrupamentos com `groupby` e `agg`.
- NumPy na inicialização da semente do gerador e datetime na criação das datas.
- O acessor `.dt` para obter mês, trimestre e ano, e `.loc` para classificar a receita por faixa de valor.
- Matplotlib e Seaborn para criar gráficos de linha, barras, dispersão e um painel com quatro gráficos.
- `json.dump` e `json.load` para salvar e reler as estatísticas.

Identifiquei no código os requisitos RF01 a RF10 para facilitar a relação entre as funções e os itens solicitados na atividade.

## Dados utilizados e decisões que tomei
Incluí no projeto o arquivo `vendas.csv`, com 200 vendas sintéticas. Caso esse arquivo não esteja na pasta, o programa gera uma base usando a semente 42, o que permite repetir a geração com os mesmos parâmetros.

No tratamento dos dados, removi espaços extras dos textos com `.str.strip()`, converti as datas com `pd.to_datetime(errors="coerce")` e converti quantidade e preço para tipos numéricos antes de fazer os cálculos.

Optei por remover as linhas com datas inválidas porque não seria possível relacionar essas vendas corretamente a um mês ou trimestre. Com `errors="coerce"`, essas datas passam a ser representadas por `NaT`. O programa também remove linhas com quantidade ou preço que não possam ser convertidos e apresenta as contagens no relatório de limpeza.

Para calcular a receita de cada transação, multipliquei a quantidade pelo preço unitário. Já o ticket médio corresponde à média da receita das transações.

Na segmentação dos clientes, considerei o gasto acumulado de cada um:

- **Bronze:** abaixo de R$ 5.000.
- **Prata:** de R$ 5.000 até R$ 15.000, incluindo os dois limites.
- **Ouro:** acima de R$ 15.000.

## Organização dos arquivos
Organizei os arquivos do projeto da seguinte forma:

- `salesinsight.py`: código principal, com as funções, a classe e a função `main()`.
- `vendas.csv`: base de vendas utilizada na análise.
- `outputs/metricas_por_mes.csv`: receita, quantidade e número de vendas por mês.
- `outputs/segmentacao_clientes.csv`: gasto acumulado e classificação de cada cliente.
- `outputs/estatisticas_gerais.json`: resumo das estatísticas, que o programa salva e lê novamente para conferir a gravação.
- `outputs/graficos/receita_por_mes.png`: evolução mensal da receita.
- `outputs/graficos/top_produtos.png`: os cinco produtos com maior receita.
- `outputs/graficos/quantidade_vs_receita.png`: relação entre quantidade e receita por transação, com cores por categoria.
- `outputs/graficos/painel_resumo.png`: painel que reúne quatro visualizações.

## Resultados da análise
Com o CSV incluído no projeto, a execução apresentou 200 registros de entrada. Após a remoção de 6 registros com datas inválidas, ficaram 194 vendas para análise, envolvendo 50 clientes e uma receita total de **R$ 1.260.595,18**.

Com esses resultados, consigo observar a evolução das vendas por mês, comparar produtos e regiões e identificar os clientes com maior gasto acumulado. Os quatro gráficos são exportados em PNG com resolução de 150 dpi. Ao executar o programa novamente, os arquivos de resultados são recriados.

## O que pretendo melhorar
Como próximos passos, pretendo acrescentar uma validação mais detalhada das colunas e dos valores de entrada, permitir filtros por período e adaptar o projeto para trabalhar com dados reais.

Também considero importante ter cuidado na interpretação: o gráfico de dispersão ajuda a visualizar a relação entre quantidade e receita, mas, sozinho, não demonstra uma relação de causa e efeito.

## Versionamento e entrega
Para concluir a entrega individual, preciso conferir a publicação do repositório no GitHub e o atendimento aos requisitos de versionamento: branches `main`, `develop`, `feat/pipeline-dados` e `docs/readme`, além de pelo menos cinco commits com mensagens descritivas.

## Vídeo de demonstração
**Link do vídeo: a inserir em breve.**

Na apresentação, vou mostrar o objetivo do projeto, como executá-lo e os resultados gerados. Também vou explicar a organização das tarefas, as branches utilizadas, a decisão de remover datas inválidas e uma possibilidade de melhoria.

O vídeo terá até cinco minutos, com minha imagem e voz. Depois de publicá-lo com acesso por link, vou atualizar este README e enviar os links do repositório e do vídeo no AVA.
