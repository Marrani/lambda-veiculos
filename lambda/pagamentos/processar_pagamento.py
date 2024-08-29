import json
import boto3
import os
import random

sqs = boto3.client('sqs')
queue_url = 'arn:aws:sqs:us-east-1:360478535176:atualiza-estoque'

def lambda_handler(event, context):
    # Recebe o código de pagamento do corpo da requisição
    body = json.loads(event['body'])
    codigo_pagamento = body.get('codigo_pagamento')

    if not codigo_pagamento:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'codigo_pagamento é necessário'})
        }

    try:
        # Simulação de verificação de pagamento
        pagamento_sucesso = verificar_pagamento(codigo_pagamento)
        
        if pagamento_sucesso:
            # Envia uma mensagem para a fila SQS indicando sucesso no pagamento
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps({
                    'codigo_pagamento': codigo_pagamento,
                    'acao': 'confirmar-operacao'
                })
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Pagamento processado com sucesso'})
            }
        else:
            raise Exception("Pagamento não efetuado com sucesso")

    except Exception as e:
        # Em caso de erro, envia uma mensagem para a fila SQS para cancelar a operação
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'codigo_pagamento': codigo_pagamento,
                'acao': 'cancelar-operacao'
            })
        )
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao processar pagamento: {str(e)}'})
        }

def verificar_pagamento(codigo_pagamento):
    # Simula um erro aleatório na verificação do pagamento
    if random.choice([True, False]):
        raise Exception("Erro ao verificar o pagamento")

    return True
