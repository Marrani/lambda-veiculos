import json
import boto3
import logging
from botocore.exceptions import ClientError
from decimal import Decimal

# Configurar o logger
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
        
        # Converter Decimal para float e ordenar
        veiculos_sorted = sorted(
            veiculos, 
            key=lambda x: float(x.get('preco', 0)) if isinstance(x.get('preco'), Decimal) else float(x.get('preco', 0))
        )
        
        # Converter Decimal para float em todos os itens
        for item in veiculos_sorted:
            if 'preco' in item and isinstance(item['preco'], Decimal):
                item['preco'] = float(item['preco'])
        
        logger.info(f"Itens com preço convertido: {veiculos_sorted}")
        
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
