import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

def lambda_handler(event, context):
    try:
        resposta = tabela_veiculos.scan(
            FilterExpression='disponivel = :disponivel',
            ExpressionAttributeValues={':disponivel': True}
        )
        
        veiculos = sorted(resposta.get('Items', []), key=lambda x: x['preco'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(veiculos)
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao listar veículos disponíveis: {e.response["Error"]["Message"]}')
        }
