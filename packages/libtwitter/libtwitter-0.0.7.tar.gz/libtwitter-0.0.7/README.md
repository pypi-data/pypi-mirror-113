LibTwitter
==========

Biblioteca para pesquisa e processamento de tweets.

Para utilizar as funções da biblioteca é necessário ter uma [conta de desenvolvedor](https://developer.twitter.com/en) no Twitter, e obter as keys de acesso:

- API Key
- API Key Secret
- Token key
- Token Secret

## Instalação

`pip install libtwitter`

## Funções

- Pesquisar tweets
- Publicar tweets
- Gerar wordclouds
- Remover emojis
- Remover caracteres

## Criando uma conexão

```python
from libtwitter import libtwitter as lt
my_twitter = lt.Twitter(api_key,api_secret,token_key,token_secret)
```

## Pesquisar tweets

O método *pesquisar_tweets* cria um dataframe  Pandas com as informações: usuário, tweet, data de postagem, idioma e a quantidade de retweets, de acordo com o termo pesquisado, também é possível as informações obtidas em um arquivo .csv.

Parâmetros:

- palavra (str): termo a ser pesquisado
- qnt (int): qnt de tweets a serem solicitados (padrão qnt=500)
- salvar (bool): opção para salvar o dataframe em arquivo .csv (padrão salvar=False)
- namefile (str): nome do arquivo .csv (padrao='result.csv')

```python
from libtwitter import libtwitter as lt
my_twitter = lt.Twitter(api_key,api_secret,token_key,token_secret)
df = my_twitter.pesquisar_tweets('#covid-19')
```

## Publicar tweets

O método *publicar_tweet* publica um tweet de forma automatica.

Parâmetros:

- novo_tweet (str): texto que vai ser publicado

```python
from libtwitter import libtwitter as lt
my_twitter = lt.Twitter(api_key,api_secret,token_key,token_secret)
for i in range(10):
	my_twitter.publicar_tweet(f'test{i}')
```

## Gerar wordclouds

O método *nuvem_de_palavras* gera uma imagem com as palavras que aparecem com mais frequência nos tweets.

Exemplo:

```python
my_twitter.nuvem_de_palavras(df['tweet'])
```


## Remover caracteres ou emojis de um dataframe

Os métodos *remover_emojis* e *remover_caracteres* permitem salvar os resultados em um arquivo .csv.

```python
df = my_twitter.remover_caracteres(dataframe,['@','_','#'])
df2 = my_twitter.remover_emojis(dataframe)
```