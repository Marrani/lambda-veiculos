import boto3
import os
import json
import uuid
import logging

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb')
veiculos_table = dynamodb.Table('Veiculos')
clientes_table = dynamodb.Table('Clientes')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def gerar_codigo_pagamento():
    return str(uuid.uuid4())

def lambda_handler(event, context):
    chassi = event['pathParameters']['id']
    body = json.loads(event['body'])
    cpf = body['cpf']

    # Verifica se o veículo está disponível
    try:
        veiculo_response = veiculos_table.get_item(Key={'chassi': chassi})
        veiculo = veiculo_response.get('Item')

        if not veiculo:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Veículo não encontrado'})
            }

        if veiculo.get('reservado', False):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Veículo já está reservado'})
            }

        if veiculo.get('disponivel', False) != True:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Veículo não está disponível para reserva'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao verificar veículo: {str(e)}'})
        }

    # Verifica se o comprador está cadastrado
    try:

        comprador_response = clientes_table.get_item(Key={'cpf': cpf})

        logger.info(f"comprador: {comprador_response}")
    
        cliente = comprador_response.get('Item')

        if not cliente:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Comprador não cadastrado'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao verificar comprador: {str(e)}'})
        }

    # Atualiza o status do veículo para reservado
    try:
        codigo_pagamento = gerar_codigo_pagamento()
        
        veiculos_table.update_item(
            Key={'chassi': chassi},
            UpdateExpression="set reservado = :reservado, disponivel = :disponivel, cpf = :cpf, codigo_pagamento = :codigo_pagamento",
            ExpressionAttributeValues={
                ':reservado': True,
                ':disponivel': False,
                ':cpf': cpf,
                ':codigo_pagamento': codigo_pagamento
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Veículo reservado com sucesso', 'codigo_pagamento': codigo_pagamento})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao reservar veículo: {str(e)}'})
        }
