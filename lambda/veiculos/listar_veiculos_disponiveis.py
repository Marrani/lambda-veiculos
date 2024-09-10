import json
import boto3
import logging
from botocore.exceptions import ClientError
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

def lambda_handler(event, context):
    try:
        logger.info("Iniciando a consulta ao DynamoDB")
        resposta = tabela_veiculos.scan(
            FilterExpression='disponivel = :disponivel',
            ExpressionAttributeValues={':disponivel': True}
        )
        
        veiculos = resposta.get('Items', [])
        logger.info(f"Itens retornados da consulta: {veiculos}")
        
        for item in veiculos:
            if 'preco' in item and isinstance(item['preco'], Decimal):
                item['preco'] = int(item['preco'])
            if 'ano' in item and isinstance(item['ano'], Decimal):
                item['ano'] = int(item['ano'])
        
        logger.info(f"Itens com preço e ano convertidos: {veiculos}")
    
        veiculos_sorted = sorted(veiculos, key=lambda x: x.get('preco', 0))
    
        logger.info(f"Itens ordenados pelo preço: {veiculos_sorted}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(veiculos_sorted)
        }
    
    except ClientError as e:
        logger.error(f"Erro ao listar veículos disponíveis: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao listar veículos disponíveis: {e.response["Error"]["Message"]}')
        }
