import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('452-predictions')

def lambda_handler(event, context):
    #get table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('452-predictions')

    now = datetime.today().strftime('%Y-%m-%d')
    week_later = (datetime.today() + timedelta(7)).strftime('%Y-%m-%d')

    response = table.query(
        KeyConditionExpression = Key('location').eq(event["location"]) & Key('date').between(now, week_later)
    )

    if len(response['Items']) < 1:
        #TODO: call sagemaker and get prediction
        prediction = 3.50

        table.put_item(
            TableName='452-predictions',
            Item={
                'location': event["location"],
                'prediction': str(prediction),
                'date': now,
            }
        )
    else:
        prediction = response['Items']
        print(prediction)

    return {
        'statusCode': 200,
        'body': prediction
    }
