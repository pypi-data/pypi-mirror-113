ImagemBinaria
=============

#### Esse é um pacote que faz operações com imagens binarias!
#### Imagem normal:

![Imagem de entrada.](imgs/flor.jpg)

## Instalação:

    pip install ImagemBinaria

## Usos:
### Tranformando em binaria:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_binaria.jpg)

### Rotacionando a Imagem em 90 graus:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.rotacao(90, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_rotacao.jpg)

### Deslocando a Imagem 100 pixels para baixo e 100 pixels para a direita:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.translacao(100, 100, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_translacao.jpg)

### Dilatando a imagem com kernel de 9x9:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.dilatacao(9, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_dilatacao.jpg)

### Causando erosão na imagem com kernel de 6x6:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.erosao(6, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_erosao.jpg)

### Causando abertura na imagem com kernel de 6x6:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.abertura(6, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_abertura.jpg)

### Causando fechamento na imagem com kernel de 6x6:
```
from ImagemBinaria import ImagemBinaria

teste = ImagemBinaria('../imgs/flor.jpg')

teste.fechamento(6, True)

teste.mostrar()
```
![Imagem de entrada.](imgs/flor_fechamento.jpg)