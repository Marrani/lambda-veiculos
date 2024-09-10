import json
import boto3
import logging
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
veiculos_table = dynamodb.Table('Veiculos')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        codigo_pagamento = message_body.get('codigo_pagamento')
        acao = message_body.get('acao')

        logger.info(f"Mensagem recebida: {message_body}")

        logger.info(f"Código de pagamento: {codigo_pagamento}, Ação: {acao}")

        try:
            veiculo_id = obter_veiculo_id(codigo_pagamento)
            
            if veiculo_id:
                logger.info(f"Chassi do veículo a ser atualizado: {veiculo_id}")

                if acao == 'confirmar-operacao':
                    # Verifica o estado atual do item
                    current_state = veiculos_table.get_item(Key={'chassi': veiculo_id}).get('Item')
                    logger.info(f"Estado atual do item: {current_state}")

                    # Atualiza o veículo como vendido
                    response = veiculos_table.update_item(
                        Key={'chassi': veiculo_id},
                        UpdateExpression="set reservado = :reservado, disponivel = :disponivel, vendido = :vendido",
                        ExpressionAttributeValues={
                            ':reservado': True,
                            ':disponivel': False,
                            ':vendido': True
                        },
                        ReturnValues="ALL_NEW"
                    )
                    logger.info(f"Resposta da atualização: {response}")

                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'Veículo atualizado com sucesso'})
                    }

                elif acao == 'cancelar-operacao':
                    # Limpa o código de pagamento e ID do comprador
                    response = veiculos_table.update_item(
                        Key={'chassi': veiculo_id},
                        UpdateExpression="remove comprador_id, codigo_pagamento set reservado = :reservado, disponivel = :disponivel",
                        ExpressionAttributeValues={
                            ':reservado': False,
                            ':disponivel': True
                        },
                        ReturnValues="ALL_NEW"
                    )
                    logger.info(f"Resposta da atualização: {response}")

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
            logger.error(f"Erro ao atualizar veículo: {str(e)}")
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
            logger.info("Nenhum veículo encontrado com o código de pagamento fornecido.")
            return None 

        veiculo = items[0]
        veiculo_id = veiculo['chassi']
        logger.info(f"Veículo encontrado: {veiculo_id}")
        return veiculo_id

    except Exception as e:
        logger.error(f"Erro ao consultar o veículo: {str(e)}")
        return None
