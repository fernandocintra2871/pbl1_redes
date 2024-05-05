# Problema 1 - MI - Concorrência e Conectividade

## Como utilizar a solução desenvolvida?
A solução desenvolvida está divida em três programas que por sua vez estão disponíveis no formato de imagem Docker no repositório do projeto no [Docker Hub](https://hub.docker.com/repositories/lfrcintra). Então para a utilização dos programas é necessario ter o Docker instalado no dispositivo no qual o programa será executado.

### 1º etapa - Baixando as imagens Docker
Primeiramente é preciso baixar cada uma das três imagens disponíveis no repositório nas respectivas máquinas que serão utilizadas, para isso basta abrir o terminal e executar cada um dos comandos abaixo em uma máquina distinta.

```bash
docker pull lfrcintra/application:latest
```
```bash
docker pull lfrcintra/broker:latest
```
```bash
docker pull lfrcintra/device:latest
```

### 2º etapa - Executando as imagens baixadas
Com as tres imagens baixadas é possível executar cada um dos programas através do Docker.

#### Executando o Broker
O Broker deve ser o primeiro programa a ser executado pois para a execução dos demais é necessário saber o IP da máquina na qual o Broker estará operando. Assim que o Broker for iniciado o IP da máquina será exibido no terminal no qual ele foi executado.
```bash
docker run --network=host --rm -it lfrcintra/broker
```

#### Executando a Aplicação e o Dispositivo
Com o IP do Broker em mãos basta substituir *ip_do_broker* nos comandos abaixo pelo IP obtido no passo anterior e executá-los.
```bash
docker run --network=host --rm -it -e ip_broker=ip_do_broker lfrcintra/application
```
```bash
docker run --network=host --rm -it -e ip_broker=ip_do_broker lfrcintra/device
```
**Obs.** É possível perceber que há três parâmetros, *network*, *it* e *e*, sendo utilizados nos comandos. O parâmetro *network* recebe a *host* da máquina na qual a imagem será executada, ou seja, ele vai compartilhar o mesmo IP e portas da máquina. Já o parâmetro *it* faz com que a execução seja interativa, possibilitando a utilização de entradas manuais com *input*. Por fim temos o parâmetro *e* que possibilita a entrada de um valor para a variável de ambiente *ip_broker*.

### Como interagir com os programas?
Com os programas em execução em cada máquina é possível agora enviar comandos e trocar dados entre eles.


#### Broker
Quando o Broker é executado aparecerá no terminal as mensagens presentes na imagem abaixo:

<p align="center">
  <img src="imgs\broker_ft1.png" alt="broker_ft1">
</p>
<p align="center">Imagem do Broker. Fonte: Autor</p>


#### Aplicação
Quando a Aplicação se conectar ao Broker aparecerá a interface abaixo no terminal. Na qual apertando a tecla ENTER é possível inserir os comandos visíveis na imagem.

<p align="center">
  <img src="imgs\app_ft1.png" alt="app_ft1">
</p>
<p align="center">Imagem da Aplicação. Fonte: Autor</p>

#### Dispositivo
Quando o Dispositivo se conectar ao Broker, será exibida a interface abaixo no terminal. Nela, ao pressionar a tecla ENTER, é possível inserir os comandos visíveis na imagem.

<p align="center">
  <img src="imgs\device_ft1.png" alt="device_ft1">
</p>
<p align="center">Imagem do Dispositivo. Fonte: Autor</p>

Após a conexão do Dispositivo a rede a Aplicação atualiza e ficará no formato abaixo, então já será possível enviar comandos ao Dispositivo conectado.

<p align="center">
  <img src="imgs\app_ft2.png" alt="app_ft2">
</p>
<p align="center">Imagem da Aplicação. Fonte: Autor</p>

**Obs.** A solução foi feita para lidar com a presença de mais de um Dispositivo, ou seja, pode-se repetir o processo de execução do Dispositivo em outras máquinas para adicionar mais Dispositivos a rede.


