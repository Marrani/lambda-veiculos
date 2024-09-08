import json
import boto3
import logging
from botocore.exceptions import ClientError
from decimal import Decimal

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        logger.info("Iniciando o scan para listar veículos vendidos.")
        resposta = tabela_veiculos.scan(
            FilterExpression='vendido = :vendido',
            ExpressionAttributeValues={':vendido': True}
        )
        
        veiculos = resposta.get('Items', [])
        logger.info(f"Veículos encontrados (antes da ordenação e conversão): {veiculos}")

        # Ordena os veículos pelo preço
        veiculos = sorted(veiculos, key=lambda x: x.get('preco', 0))
        logger.info(f"Veículos ordenados pelo preço: {veiculos}")

        # Converte Decimal para float e int
        for item in veiculos:
            if 'preco' in item and isinstance(item['preco'], Decimal):
                item['preco'] = float(item['preco'])
                logger.info(f"Preço convertido para float: {item['preco']}")
            if 'ano' in item and isinstance(item['ano'], Decimal):
                item['ano'] = int(item['ano'])
                logger.info(f"Ano convertido para int: {item['ano']}")

        return {
            'statusCode': 200,
            'body': json.dumps(veiculos)
        }
    
    except ClientError as e:
        logger.error(f"Erro ao listar veículos vendidos: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao listar veículos vendidos: {e.response["Error"]["Message"]}')
        }
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro inesperado: {str(e)}')
        }
