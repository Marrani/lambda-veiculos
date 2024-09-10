# lambda-veiculos

Este projeto contém o código-fonte e arquivos de suporte para uma aplicação serverless que você pode implantar usando o SAM CLI. Ele inclui as seguintes pastas e arquivos:

- **lambda/veiculos/** - Código para as funções Lambda relacionadas ao gerenciamento de veículos (criação, edição, listagem e reserva).
- **lambda/pagamentos/** - Código para a função Lambda que processa os pagamentos.
- **lambda/estoque/** - Código para a função Lambda que faz a baixa de estoque.
- **events/** - Eventos de invocação que você pode usar para testar as funções.
- **tests/** - Testes unitários para o código da aplicação.
- **template.yaml** - Um template que define os recursos da AWS necessários para a aplicação.

## Funcionalidades

Este projeto utiliza vários recursos da AWS, como funções Lambda, DynamoDB, SQS e API Gateway, definidos no arquivo `template.yaml`. As principais funções Lambda são:

- **CriarVeiculoFunction**: Cria um novo veículo na tabela DynamoDB.
- **EditarVeiculoFunction**: Edita os detalhes de um veículo existente.
- **ListarVeiculosDisponiveisFunction**: Lista todos os veículos disponíveis para venda.
- **ListarVeiculosVendidosFunction**: Lista os veículos que já foram vendidos.
- **ReservarVeiculoFunction**: Reserva um veículo para um cliente.
- **ProcessarPagamentoFunction**: Processa o pagamento de um veículo reservado.
- **BaixarEstoqueFunction**: Atualiza o estoque de veículos vendidos a partir de mensagens SQS.

## Desenho da Arquitetura

![Arquitetura mducati](https://github.com/user-attachments/assets/f98254a8-7d8f-41fe-b141-3ae03bf49272)

## Fluxo de Compra

O processo de compra de um veículo é composto pelos seguintes passos:

1. **Seleção do Veículo**: O cliente seleciona um veículo disponível.
2. **Reserva do Veículo**: O cliente reserva o veículo, que é marcado como reservado na tabela DynamoDB.
3. **Código de Pagamento**: O cliente recebe um código de pagamento para o veículo reservado.
4. **Processo de Pagamento**: O cliente realiza o pagamento utilizando o código recebido.

   - **Caso de Sucesso**: Se o pagamento é bem-sucedido, a função `ProcessarPagamentoFunction` envia uma mensagem para a fila SQS `atualiza-estoque` para atualizar o estoque.
   - **Caso de Falha**: Se o pagamento falha, a função `ProcessarPagamentoFunction` envia uma mensagem para a mesma fila SQS para tratamento posterior.

5. **Baixa de Estoque**: A função `BaixarEstoqueFunction` é acionada pela fila SQS e realiza o seguinte:

   - **Se o Pagamento foi Bem-Sucedido**: A função baixa o estoque do veículo vendido.
   - **Se o Pagamento Falhou**: A função realiza um rollback, revertendo o veículo para o status de disponível.

### Justificativa dos Serviços Utilizados

- **Serverless**: A utilização de funções Lambda permite escalabilidade automática e gestão simplificada do código sem a necessidade de provisionar ou gerenciar servidores.
- **DynamoDB**: Um banco de dados NoSQL gerenciado, ideal para operações rápidas e escaláveis.
- **SQS**: Facilita a comunicação assíncrona e desacoplada entre funções Lambda, garantindo robustez e resiliência.
- **API Gateway**: Gerencia e protege as APIs, facilitando a integração com clientes e serviços externos.
- **Cognito**: Fornece um sistema seguro e escalável de autenticação e autorização.

### Segurança dos Dados

#### Dados Armazenados

- **Veículos**: Dados como modelo, ano, preço e status (disponível/vendido).
- **Clientes**: Dados pessoais como nome, CPF, e-mail, e informações de pagamento.

#### Dados Sensíveis

- **Informações Pessoais**: CPF, e-mail, e dados de pagamento dos clientes.

#### Políticas de Acesso a Dados

- **IAM Roles**: Políticas que permitem acesso restrito às funções Lambda para interagir com DynamoDB e SQS.
- **Cognito**: Controle de acesso baseado em tokens de autenticação.

#### Políticas de Segurança da Operação

- **Criptografia**: Dados sensíveis são criptografados em trânsito e em repouso.
- **Logs**: Monitoramento e logs são gerados para todas as funções Lambda utilizando o CloudWatch.

#### Riscos e Ações de Mitigação

- **Exposição de Dados Sensíveis**: Implementação de criptografia e políticas de acesso restrito.
- **Falhas na Comunicação SQS**: Garantia de processamento adequado com a verificação de mensagens e rollback em caso de falhas.

## Orquestração SAGA

### Tipo de Orquestração SAGA

**Orquestração baseada em Coreografia**: No padrão de coreografia, cada serviço executa suas tarefas e notifica outros serviços sobre o progresso e resultado da transação. A função Lambda `ProcessarPagamentoFunction` envia uma mensagem para a fila SQS se o pagamento for bem-sucedido. A função `BaixarEstoqueFunction` então consome essas mensagens para atualizar o estoque. Em caso de falha no pagamento, a transação é revertida e o estoque é atualizado conforme necessário.

### Justificativa do Padrão Escolhido

A coreografia é escolhida por sua flexibilidade e escalabilidade, permitindo que cada serviço envolvido na transação execute e notifique seu progresso de forma autônoma. Isso reduz o acoplamento entre os serviços e melhora a resiliência do sistema como um todo.

## Pré-requisitos

Para utilizar o SAM CLI e implantar esta aplicação, você precisará dos seguintes componentes instalados:

- SAM CLI - [Instalar SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3 instalado
- Docker - [Instalar Docker](https://docs.docker.com/get-docker/)

## Implantação da aplicação

Para compilar e implantar sua aplicação pela primeira vez, execute os seguintes comandos no terminal:

```bash
sam build --use-container
sam deploy --guided
