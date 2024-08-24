import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
tabela_veiculos = dynamodb.Table('Veiculos')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        veiculo_id = body['id']
        
        update_expression = "SET marca = :marca, modelo = :modelo, ano = :ano, cor = :cor, preco = :preco"
        expression_attribute_values = {
            ':marca': body.get('marca'),
            ':modelo': body.get('modelo'),
            ':ano': body.get('ano'),
            ':cor': body.get('cor'),
            ':preco': body.get('preco')
        }
        
        resposta = tabela_veiculos.update_item(
            Key={'id': veiculo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Veículo atualizado com sucesso!')
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro ao atualizar veículo: {e.response["Error"]["Message"]}')
        }
