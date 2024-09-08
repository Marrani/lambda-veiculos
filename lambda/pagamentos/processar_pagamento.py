import json
import boto3
import os
import random

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/360478535176/atualiza-estoque'

def lambda_handler(event, context):
    body = json.loads(event['body'])
    codigo_pagamento = body['codigo_pagamento']

    if not codigo_pagamento:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'codigo_pagamento é necessário'})
        }

    try:
        pagamento_sucesso = verificar_pagamento(codigo_pagamento)
        
        if pagamento_sucesso:
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
    if random.choice([True, False]):
        raise Exception("Erro ao verificar o pagamento")

    return True
