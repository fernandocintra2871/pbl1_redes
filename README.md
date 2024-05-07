# Problema 1 - Internet das Coisas (MI de Concorrência e Conectividade)

## Sumario
  * [Introdução](#introdução)
  * [Como utilizar a solução desenvolvida?](#como-utilizar-a-solução-desenvolvida)
    + [1º etapa - Baixando as imagens Docker](#1º-etapa---baixando-as-imagens-docker)
    + [2º etapa - Executando as imagens baixadas](#2º-etapa---executando-as-imagens-baixadas)
      - [Executando o Broker](#executando-o-broker)
      - [Executando a Aplicação e o Dispositivo](#executando-a-aplicação-e-o-dispositivo)
    + [Como interagir com os programas?](#como-interagir-com-os-programas)
      - [Broker](#broker)
      - [Aplicação](#aplicação)
      - [Dispositivo](#dispositivo)
  * [Solução Desenvolvida](#solução-desenvolvida)
    + [Dispositivo Virtual](#dispositivo-virtual)
    + [Broker](#broker-1)
    + [Aplicação](#aplicação-1)
  * [Aspectos do Projeto](#aspectos-do-projeto)
    + [Arquitetura da Solução](#arquitetura-da-solução)
    + [Protocolo de Comunicação Entre Dispositivo e Broker - Camada de Aplicação](#protocolo-de-comunicação-entre-dispositivo-e-broker---camada-de-aplicação)
    + [Protocolo de Comunicação Entre Dispositivo e Broker - Camada de Transporte](#protocolo-de-comunicação-entre-dispositivo-e-broker---camada-de-transporte)
    + [Interface da Aplicação (REST)](#interface-da-aplicação-rest)
    + [Formatação, Envio e Tratamento de Dados](#formatação-envio-e-tratamento-de-dados)
    + [Tratamento de Conexões Simultâneas](#tratamento-de-conexões-simultâneas)
    + [Gerenciamento do Dispositivo](#gerenciamento-do-dispositivo)
    + [Desempenho](#desempenho)
    + [Confiabilidade da Solução](#confiabilidade-da-solução)

## Introdução
O presente projeto foi solicitado como trabalho avaliativo para a disciplina MI - Concorrência e Conectividade (TEC502) do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS). No trabalho em questão foi requerido o desenvolvimento de um  middleware distribuído, ou seja, um sistema que possibilitasse a comunicação entre dispositivos IoT e suas respectivas aplicações. 

O produto a ser desenvolvido deveria permitir o envio de comandos da aplicação para os seus dispositivos e também o envio de dados dos dispositivos para a aplicação. Além disso, a solução deveria possuir um *broker*, um intermediário que facilitasse essa troca de mensagens. O *broker* teria de usar como base um subsistema de rede TCP/IP e não poderia ser feito o uso de nenhum framework de troca de mensagens.

Além do mais, também foi demandado a criação de um dispositivo virtual que seria utilizado para a geração de dados fictícios. O dispositivo citado, deveria possuir uma interface de entrada não grafica para comandos de gerenciamento para a geração dos dados. Para mais, o dispositivo deveria utilizar abordagem não confiável para o envio de dados e uma abordagem confiável para recepção de comandos,  fazendo uso da interface de socket nativa do TCP/IP.

Por fim, foi pedido a criação de uma aplicação simples com interface para emissão de comandos de gerenciamento para os dispositivos simulados. A aplicação deveria se comunicar com o serviço *broker* através de uma API RESTful.


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

## Solução Desenvolvida
Para atender aos requisitos solicitados, foram desenvolvidos três programas distintos para cumprir os papeis de dispositivo virtual, *broker* e aplicação, utilizando Python, que quando em execução se comunicam de acordo com o diagrama abaixo. 

<p align="center">
  <img src="imgs\diagrama.png" alt="diagrama">
</p>
<p align="center">Diagrama das Conexões. Fonte: Autor</p>



### Dispositivo Virtual
O dispositivo virtual criado simula um sensor de temperatura, no qual tem-se os dados de temperatura e estado (ligado ou desligado) que podem ser alterados tanto no próprio terminal de execução do programa, através dos comandos *ligar, desligar e temp [valor]*, quanto na interface da aplicação, neste último caso apenas o estado pode ser alterado.

O dispositivo envia dados através do *User Datagram Protocol* (UDP) para o serviço *broker*, ou seja, já que o UDP é um protocolo não orientado à conexão, ele não oferece garantias de entrega confiável. Além disso o dispositivo virtual recebem do serviço *broker* comandos através do *Transmission Control Protocol* (TCP), que diferente do UDP é orientado à conexão então garante um serviço de entrega confiável. A comunicação UDP e TCP foi feita utilizando a biblioteca Socket do Python que permite o uso desses protocolos para criar conexões de rede bidirecionais entre um cliente e um servidor. Também foi feito o uso da biblioteca Threading do Python para permitir que o dispositivo simulado possa enviar dados enquanto aguarda comandos usando diferentes *threads*.

### Broker
O serviço *broker* desenvolvido atua como um servidor, visto que tanto a aplicação como o dispositivo iniciam a comunicação com ele, e ele por sua vez está sempre aguardando novas conexões.

Assim, ele também faz uso da biblioteca Socket  para receber dados via UDP dos dispositivos virtuais conectados e enviar comandos provenientes da aplicação via TCP para os respectivos dispositivos. O *broker* Também possui uma API, que foi construída utilizando o framework Flask, cuja qual se comunica com a aplicação via HTTP.

O *broker* também faz uso de *threads* através da biblioteca Threading do Python, para ficar atento a conexões com novos dispositivos, enviar dados via TCP, receber dados via UDP e ficar atento à desconexão de dispositivos.

### Aplicação
A interface da aplicação foi feita de forma não grafica, usando o terminal para exibir os dados provenientes dos dispositivos e para entrada de comandos por parte do usuário.  Ela se comunica com o *broker* via HTTP e faz uso da API do mesmo, através da biblioteca Request do Python, para requisitar os dados dos dispositivos e para enviar os comandos. A aplicação também utiliza *threads*, através da biblioteca Threading do Python, para exibir os dados dos dispositivos no terminal enquanto fica atento a entrada de comandos pelo usuário.

## Aspectos do Projeto

### Arquitetura da Solução
O sistema possui três componentes, o dispositivo, o broker e a aplicação.  Durante o uso dos componentes, alguns cenários de troca de mensagens ocorrem, são eles:

**Inicialização:** O broker é o primeiro a ser iniciado e a partir do momento que ele é iniciado ele fica observando as portas TCP e UDP para detectar novas conexões, além de deixar a API operante. Quando um dispositivo é iniciado ele envia duas mensagens para o broker, uma via UDP contendo os dados do dispositivo e outra via TCP contendo a string “init”. Assim que o broker recebe essas duas mensagens ele atribui um id ao dispositivo e salva o endereço, os dados recebidos e a conexão TCP estabelecida em dicionários distintos usando o mesmo id como chave. Quando a aplicação é iniciada ela começa a pedir continuamente através da API os dados de todos os dispositivos conectados ao broker.

**Envio de comando da aplicação para um dispositivo:** Quando um comando é dado na aplicação, ela envia o comando através da API para o broker. Quando o broker recebe a requisição adiciona o comando recebido a uma fila, da qual ele continuamente remove comandos e os enviam via TCP para seus respectivos dispositivos para serem executados, fazendo uso das conexões TCP salvas no processo de inicialização. O comando então é recebido pelo dispositivo e executado.

**Atualização da aplicação quando um comando é dado diretamente no dispositivo:** Quando um comando é dado diretamente no dispositivo, uma mensagem é enviada via UDP para o broker contendo os dados do dispositivo. O broker recebe então os dados e atualiza o dicionário de dados, substituindo o valor contido na chave referente ao ID do dispositivo pelos novos dados. Como a aplicação está continuamente pedindo os dados dos dispositivos para o broker, em algum momento ela irá solicitar os dados atualizados.

**Verificação de conectividade entre o broker e os dispositivos:** Para garantir que  os dispositivos visíveis na aplicação ainda estão conectados e recebendo comandos, o broker fica continuamente verificando a conexão TCP com eles. Para isso o broker envia uma mensagem TCP contendo a string “test” e aguarda uma resposta com tempo limite de dois segundos. Quando o dispositivo recebe a string “test” ele envia via TCP a mesma string para o broker. Caso o tempo limite de recebimento for ultrapassado, o broker remove os dados do dispositivo do dicionário de dados. Desse modo, quando a aplicação for solicitar os dados dos dispositivos, o dispositivo descontado já não estará mais presente. A partir do momento que um dispositivo for desconectado, o broker passa a tentar se reconectar ao dispositivo. Quando a reconexão acontece, o broker envia a string “reconnect” via TCP para o dispositivo, quando o dispositivo recebe ele envia os dados novamente para o broker via UDP, assim fazendo com que os dados do dispositivo apareçam novamente na aplicação.

### Protocolo de Comunicação Entre Dispositivo e Broker - Camada de Aplicação
Para a construção da solução foram desenvolvidos alguns protocolos de comunicação entre o dispositivo e o broker, são eles:

**Inicialização:** Quando o dispositivo é iniciado ele envia uma mensagem via TCP contendo a string “init’ e outra via UDP contendo um json com um dicionário com os dados do dispositivo (temperatura e estado) para o broker. Quando o broker recebe essas duas mensagens ele adiciona o dispositivo ao dicionário de dispositivos, os dados recebidos ao dicionário de dados e a conexão estabelecida ao dicionário de conexões, todos utilizando a mesma chave, o ID atribuído ao dispositivo pelo broker.

**Atualização de dados:** Quando um dado é alterado diretamente no dispositivo, ele envia via UDP um json com um dicionário, contendo a temperatura e o estado, para o broker. Quando o broker recebe esse dicionário ele descobre o ID do dispositivo com base no endereço dele salvo no dicionário de dispositivos e substitui os dados salvos no mesmo ID no dicionário de dados pelos recém recebidos.
<a id="ver_con"></a>
**Verificação de conectividade:** A partir do momento que o broker é iniciado ele verifica constantemente a conexão com os dispositivos, para isso ele envia a string “test” via TCP para um dispositivo e espera  que o dispositivo envie a mesma string via TCP em até dois segundos.
<a id="rec"></a>
**Reconexão:** Quando um dispositivo que havia se desconectado é conectado novamente o broker envia a string “reconnect” via TCP. Quando a string é recebida pelo dispositivo ele envia via UDP os dados contendo a temperatura e o estado do dispositivo para o broker.

### Protocolo de Comunicação Entre Dispositivo e Broker - Camada de Transporte
No projeto foram utilizados os protocolos TCP e UDP. O protocolo TCP foi utilizado para o envio de comandos do broker para os dispositivos, pois por possuir uma abordagem confiável para o envio de dados, garante que os comandos cheguem até os dispositivos caso haja conexão. Já o protocolo UDP foi utilizado para o envio de dados do dispositivo para o broker, pois foi requerido pelo problema.

### Interface da Aplicação (REST)
Para comunicação entre a aplicação e o broker foi utilizado uma API RESTful. Nela foi utilizado o método *POST* na rota */commands* para adicionar comandos dados na aplicação a lista de comandos a serem enviados para os dispositivos no broker. Além disso, também foi utilizado o método *GET* na rota */sensors” para a aplicação conseguir obter os dados de todos os dispositivos conectados ao broker.

### Formatação, Envio e Tratamento de Dados
Os dados enviados do dispositivo para o broker via UDP estão na forma de uma dicionario com o seguinte formato: {“state”:True, “temp”: 19.1}, o dicionário é convertido para json e enviado. Já os dados dos dispositivos contidos no broker que são consumidos pela aplicação via API estão em um dicionário contendo os dados dos dispositivos organizados por ID da seguinte forma: { 1:{“state”:False, “temp”: 12.7}, 4:  {“state”:True, “temp”: 28.3}}, e também são convertidos para json antes de serem enviados.

### Tratamento de Conexões Simultâneas
No dispositivo foi criado uma *thread* receber comandos via TCP e realizar suas respectivas execuções. O uso da *thread* se fez necessário pois era preciso durante a execução do programa também permitir a entrada de comandos diretamente no dispositivo pelo usuário o que tornaria inviável o recebimento de comandos vindos do broker. Como o broker só envia um comando por vez para cada dispositivo, não foram identificados problemas de concorrência nesse cenário.

No broker foram criadas três *threads*, sendo a primeira usada para detectar novas conexões TCP feitas por novos dispositivos através do protocolo de inicialização desenvolvido. Nesse caso não foi identificado problema de concorrência pois como se utiliza o protocolo TCP, se outro dispositivo tentar se conectar, enquanto um já está fazendo isso, ele só vai ter que esperar o processo do anterior terminar. Já a segunda foi usada para ficar enviando os comandos recebidos da aplicação para os respectivos dispositivos, como os comandos são inseridos em uma fila e enviados um por um, os problemas de concorrência foram evitados. Por fim, a terceira foi utilizada para checar a conexão com todos os dispositivos conectados ao broker, como essa checagem é feita em ordem percorrendo o dicionário de conexões, também não foi identificado problemas de concorrência.

Na aplicação foi utilizada uma *thread* para solicitar para o broker os dados dos sensores e exibi-los no terminal da aplicação ao mesmo tempo que é possível a entrada de comandos pelo usuário.

### Gerenciamento do Dispositivo
Com o produto desenvolvido é possível controlar cada um dos dispositivos conectados através da aplicação com os comandos `ligar [id]` e `desligar [id]` que são enviados para o broker e posteriormente para o respectivo dispositivo. Já no próprio dispositivo é possível utilizar os seguintes comandos: `ligar`, `desligar` e `temp [value]`. Quando um dispositivo está desligado, se sua temperatura for alterada no próprio dispositivo, ela não é enviada, isso e o fato de não poder alterar a temperatura do dispositivo a partir da aplicação foram decisões de projeto tomadas para tornarem o dispositivo virtual mais realista.

### Desempenho
Para otimizar o desempenho da solução em geral o broker possui uma cache na forma de dicionário que está organizado por ID e armazena as temperaturas e estados de todos os sensores conectados, quando a aplicação solicita os dados dos sensores via API é dessa cache que esses dados são retirados. Essa cache é atualizada toda vez que alguma alteração ocorre no sensor. Isso evita que a aplicação tenha que esperar o broker enviar uma requisição para o dispositivo para depois ser retornada a ela.

O mesmo acontece com os comandos enviados da aplicação para os dispositivos, os comandos são armazenados em uma fila no broker, cuja qual em uma *thread* específica, são enviados para seus respectivos sensores.

### Confiabilidade da Solução
O broker possui uma *thread* chamada `check_device_conn()` que verifica constantemente se os dispositivos conectados estão recebendo mensagens através do protocolo de [Verificação de conectividade](#ver_con). Quando não é possível enviar mensagens para o dispositivo ele é removido do dicionário de dados para que assim não apareça na aplicação, desse modo o usuário não poderá na aplicação enviar comandos para o dispositivo desconectado. Já quando o dispositivo se conecta novamente se inicia o protocolo de [Reconexão](#rec), fazendo com o que dispositivo seja novamente adicionado ao dicionário de dados, o que por sua vez o fará aparecer novamente na aplicação, o tornando receptivo a comandos.

Quando o broker é desconectado a aplicação passa a tentar reconexão com o broker pois a solicitações de API geraram *ConnectionError* que é tratado e induz a aplicação a esse estado de “tentando reconexão”. Já o dispositivo, quando o broker é desconectado, continua operando normalmente, porém os dados enviados via UDP durante essa situação serão perdidos, mas quando o broker se reconectar ele solicitará os últimos dados através do protocolo de reconexão.

