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
