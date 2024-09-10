
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

## Pré-requisitos

Para utilizar o SAM CLI e implantar esta aplicação, você precisará dos seguintes componentes instalados:

- SAM CLI - [Instalar SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3 instalado
- Docker - [Instalar Docker](https://docs.docker.com/get-docker/)

## Implantação da aplicação

Para compilar e implantar sua aplicação pela primeira vez, execute os seguintes comandos no terminal:

\`\`\`bash
sam build --use-container
sam deploy --guided
\`\`\`

O primeiro comando compilará o código-fonte da aplicação. O segundo comando empacota e implanta sua aplicação na AWS, com uma série de perguntas:

- **Stack Name**: Nome da stack a ser criada no CloudFormation.
- **AWS Region**: Região AWS onde a aplicação será implantada.
- **Confirm changes before deploy**: Selecione "yes" para revisar as mudanças antes de implantar.
- **Allow SAM CLI IAM role creation**: Permita que o SAM CLI crie as funções IAM necessárias.
- **Save arguments to samconfig.toml**: Escolha "yes" para salvar as configurações para futuras implantações.

O URL do endpoint do API Gateway será exibido nos valores de saída após a implantação.

## Testando localmente

Você pode construir sua aplicação localmente com o comando:

\`\`\`bash
sam build --use-container
\`\`\`

Teste uma única função Lambda invocando-a diretamente com um evento de teste JSON. Os eventos de exemplo estão disponíveis na pasta \`events\`.

\`\`\`bash
sam local invoke CriarVeiculoFunction --event events/event.json
\`\`\`

Para simular o API Gateway, utilize:

\`\`\`bash
sam local start-api
\`\`\`

E então acesse o endpoint local:

\`\`\`bash
curl http://localhost:3000/veiculos
\`\`\`

## Logs das funções Lambda

Use o comando \`sam logs\` para visualizar os logs das funções Lambda já implantadas.

\`\`\`bash
sam logs -n CriarVeiculoFunction --stack-name "lambda-veiculos" --tail
\`\`\`

## Testes

Os testes estão definidos na pasta \`tests\`. Use o PIP para instalar as dependências de teste e execute os testes:

\`\`\`bash
pip install -r tests/requirements.txt --user
# Testes unitários
python -m pytest tests/unit -v
# Testes de integração (necessita de deploy)
AWS_SAM_STACK_NAME="lambda-veiculos" python -m pytest tests/integration -v
\`\`\`

## Limpeza

Para deletar a aplicação implantada:

\`\`\`bash
sam delete --stack-name "lambda-veiculos"
\`\`\`

## Recursos adicionais

- [Documentação do AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications)

