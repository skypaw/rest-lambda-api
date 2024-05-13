import json
import os

import boto3

from responses import success_response, bad_request_response, not_found_response

DYNAMODB_CLIENT = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
FAVOURITE_FOR_USER = {"type": {"S": "user"}, "id": "uuidv4"}


def decode_body(event):
    return json.loads(event["body"])


def get_item(key):
    return DYNAMODB_CLIENT.get_item(TableName=TABLE_NAME, Key=key)


def put_item(item):
    return DYNAMODB_CLIENT.put_item(TableName=TABLE_NAME, Item=item)


def list_characters():
    characters_db = DYNAMODB_CLIENT.query(
        TableName=TABLE_NAME,
        ExpressionAttributeNames={'#t': 'type'},
        ExpressionAttributeValues={':a': {'S': 'character'}},
        KeyConditionExpression='#t = :a'
    )
    characters = []
    for character in characters_db['Items']:
        characters.append(character['id']['S'])
    return success_response(characters)


def unpack_favourite(item):
    return item["Item"]["favourites"]["SS"]


def favourites(event):
    method = event.get('httpMethod')
    if method == 'GET':
        item = get_item(FAVOURITE_FOR_USER)
        return success_response(item)
    if method == 'POST':
        try:
            body = decode_body(event)["add"]
        except (json.JSONDecodeError, KeyError, TypeError):
            return bad_request_response('body syntax: {"add": "character_name"}')
        character = get_item({'type': {'S': 'character'}, 'id': {'S': body}})

        if character.get("Item"):
            favourites_db = get_item(FAVOURITE_FOR_USER)
            favourite_characters = {i for i in unpack_favourite(favourites_db)}
            favourite_characters.add(body)

            put_item({'favourites': {'SS': list(favourite_characters)}, **FAVOURITE_FOR_USER})
            return success_response('Favourite character added')
        return not_found_response('Character not found')


def handler(event, context):
    pass
