import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

def lambda_handler(event, context):
    try:
        resposta = tabela_veiculos.scan(
            FilterExpression='vendido = :vendido',
            ExpressionAttributeValues={':vendido': True}
        )
        
        veiculos = sorted(resposta.get('Items', []), key=lambda x: x['preco'])

        for item in veiculos:
            if 'preco' in item and isinstance(item['preco'], Decimal):
                item['preco'] = float(item['preco'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(veiculos)
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao listar veículos vendidos: {e.response["Error"]["Message"]}')
        }
