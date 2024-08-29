import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
veiculos_table = dynamodb.Table(os.environ['DB_TABLE_NAME'])

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        codigo_pagamento = message_body.get('codigo_pagamento')
        acao = message_body.get('acao')

        try:
            veiculo_id = obter_veiculo_id(codigo_pagamento)
            
            if veiculo_id:
                if acao == 'confirmar-operacao':
                    # Atualiza o veículo como vendido
                    veiculos_table.update_item(
                        Key={'id': veiculo_id},
                        UpdateExpression="set reservado = :reservado, disponivel = :disponivel, vendido = :vendido",
                        ExpressionAttributeValues={
                            ':reservado': True,
                            ':disponivel': False,
                            ':vendido': True
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'Veículo atualizado com sucesso'})
                    }

                elif acao == 'cancelar-operacao':
                    # Limpa o código de pagamento e ID do comprador
                    veiculos_table.update_item(
                        Key={'id': veiculo_id},
                        UpdateExpression="remove comprador_id, codigo_pagamento set reservado = :reservado, disponivel = :disponivel",
                        ExpressionAttributeValues={
                            ':reservado': False,
                            ':disponivel': True
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'Operação cancelada e veículo atualizado com sucesso'})
                    }
                else:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': f'Ação desconhecida: {acao}'})
                    }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Veículo não encontrado'})
                }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Erro ao atualizar veículo: {str(e)}'})
            }

def obter_veiculo_id(codigo_pagamento):
    try:
        response = veiculos_table.scan(
            FilterExpression=Attr('codigo_pagamento').eq(codigo_pagamento)
        )
        items = response.get('Items')

        if not items:
            return None 

        veiculo = items[0]
        veiculo_id = veiculo['id']
        return veiculo_id

    except Exception as e:
        print(f"Erro ao consultar o veículo: {str(e)}")
        return None
