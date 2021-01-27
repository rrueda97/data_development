"""Script to label data from AWS with proper de-identification methods"""
import boto3
from decimal import Decimal
import json
import datetime
import base64
import numpy as np
import cv2
import os
from tqdm import tqdm

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
lambda_client = boto3.client('lambda', region_name='us-west-2')


def invoke_lambda(function_name: str, payload: dict, invocation_type: str ='RequestResponse'):
    """invokes a lambda function"""
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload)
        )
        if invocation_type == 'RequestResponse':  # synchronous invocation
            if response['StatusCode'] != 200 or 'FunctionError' in response:
                response_dict = json.loads(response['Payload'].read().decode('utf-8'))
                raise RuntimeError(response_dict['errorMessage'])
            else:
                response_dict = json.loads(response['Payload'].read().decode('utf-8'))
                return response_dict

        elif invocation_type == 'Event':  # asynchronous invocation
            if response['StatusCode'] != 202 or 'FunctionError' in response:
                raise RuntimeError(response['ResponseMetadata'])
            else:
                return

    except Exception as e:
        print(f'{datetime.datetime.now()} Exception in invoke_lambda\n{e}')


def get_unlabeled_data(user_pool_id: str):
    """function to pull unlabeled items from DetectionsByClientUserAndTime using UserPoolID"""
    db_lambda_payload = {'mode': 'query_key_expression',
                         'table_name': 'DetectionsByClientUserAndTime',
                         'key_expression': {'UPID':
                                               {'relationship': 'equals',
                                                'value': user_pool_id}
                                           },
                         'filter_expression': {'TrueOutput':
                                                  {'relationship': 'equals',
                                                   'value': 'not set'}
                                              }
                         }
    print('\npulling data from db...')
    lambda_response = invoke_lambda(function_name='database_lambda',
                                    payload=db_lambda_payload)
    assert lambda_response['statusCode'] == 200
    return lambda_response['result']


def get_blurred_img(file_name: str):
    """function to pull an image from livedevicepersoncapture and blur it for privacy"""
    pull_image_lambda_payload = {'bucket': 'livedevicepersoncapture',
                                 'file_name': file_name}
    lambda_response = invoke_lambda(function_name='pull_image_lambda',
                                    payload=pull_image_lambda_payload)
    assert lambda_response['statusCode'] == 200
    base64_img_bytes = base64.b64decode(lambda_response['img_str_blurred'])
    img_array = np.frombuffer(base64_img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
    return img


def draw_detection(img, detections: list):
    """draws detection bounding box diagonal on image"""
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]  # B, G, R, BLK
    for i, detection in enumerate(detections):
        start = (int(detection[0]), int(detection[1]))
        end = (int(detection[2]), int(detection[3]))
        thickness = 3
        img = cv2.line(img, start, end, colors[i], thickness)
    return img


def set_label(item: dict):
    """function to set a label for a given data item and write it to the database"""
    print(f"\nlabel image: {item['Filename']}")
    labels = {'1': 'sit',
              '2': 'stand',
              '3': 'sitting-standing',
              '4': 'in bed',
              '5': 'empty'}
    while True:
        try:
            for label_num in labels:
                print(f"[{label_num}] {labels[label_num]}")

            new_label = labels[input(':')]
            if input(f'label image as {new_label}? [y/n]') == 'y':
                break

        except KeyError:
            print('\ninvalid label\n')

    table = dynamodb.Table('DetectionsByClientUserAndTime')
    try:
        response = table.update_item(
            Key={'UPID': item['UPID'], 'Timestamp': Decimal(str(item['Timestamp']))},
            UpdateExpression="set TrueOutput = :nl",
            ExpressionAttributeValues={':nl': new_label},
            ReturnValues="UPDATED_NEW")
        assert response['Attributes']['TrueOutput'] == new_label
    except Exception as e:
        print('Exception in set_label')
        print(e)


def main(user_pool_id):
    """main function to label data"""
    unlabeled_data = get_unlabeled_data(user_pool_id=user_pool_id)
    print(f"\nReturned {len(unlabeled_data)} items...\n")
    for item in unlabeled_data:
        s3_img = draw_detection(get_blurred_img(item['Filename']), item['Box'])
        cv2.imshow('Label Image', s3_img)
        cv2.waitKey(1)
        set_label(item)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # upid = 'e1e2a35e-bbfa-4ab9-950a-466c874d4479'  # John's UPID
    upid = '842b9b8d-fead-4d2a-a73d-3fcb62783c65'  # Sandra's UPID
    main(upid)
