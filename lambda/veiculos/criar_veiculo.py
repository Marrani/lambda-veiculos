import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        item = {
            'id': body['id'],
            'marca': body['marca'],
            'modelo': body['modelo'],
            'ano': body['ano'],
            'cor': body['cor'],
            'preco': body['preco'],
            'disponivel': True,
            'vendido': False,
            'reservado': False
        }
        
        tabela_veiculos.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'body': json.dumps('Veículo criado com sucesso!')
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao criar veículo: {e.response["Error"]["Message"]}')
        }
