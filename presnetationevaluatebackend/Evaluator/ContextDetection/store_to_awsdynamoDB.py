import boto3
import config

def store_to_awsdynamoDB(slide_num, scores):
    # Initialize DynamoDB client
    dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-2',
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRET_ACCESS_KEY)
    table = dynamodb.Table('ContentResult')
    # Save the item to the DynamoDB table
    try:
        table.put_item(
            Item={
                'slide_id': slide_num,  # Partition key
                'content_coverage': scores[0],
                'correctness': scores[1],
                'consistency_in_words': scores[2],
                'textual_cohesion': scores[3],
                'language_and_grammar': scores[4]
            }
        )
        print(f"Successfully saved scores for slide {slide_num} to DynamoDB.")
        return 1
    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")
        return 0
