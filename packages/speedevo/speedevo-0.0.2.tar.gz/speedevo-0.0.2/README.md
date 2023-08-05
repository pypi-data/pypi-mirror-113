speedevo
==============

#### Esse é um pacote que faz teste de velocidade na sua internet e gera um arquivo em .xlsx com as informação do teste.

## Instação:

```
pip install speedevo
```

## Como usar:

```
import speedevo
s = speedevo.Speedevo()
s.speed_test('nomeDoArquivo')
s.histogram('nomeDoArquivo', 'nomeDaColuna')
```
