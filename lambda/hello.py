import os
import json
import custom_func as cf


def handler(event, context):
    env_test_value = os.environ['env_test_key']
    print(env_test_value)
    cf.cust_fun()
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, AWS CDK! You have hit {}\n'.format(event['path'])
    }
