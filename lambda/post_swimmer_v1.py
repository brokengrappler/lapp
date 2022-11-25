import json
import uuid
import boto3
from botocore.exceptions import ClientError
import psycopg2
from datetime import datetime


def lambda_handler(event, context):
    # userEventBody = json.loads(event['queryStringParameters'])
    # userEventBody = event['queryStringParameters']

    response = write_to_db(event)
    responseObject = {}
    responseObject['status_code'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(event)
    return


def write_to_db(event):
    epochms = event['requestContext']['timeEpoch']
    updated_at = datetime.fromtimestamp(epochms/1000).strftime('%Y-%m-%d')
    data = json.loads(event['body'].replace("'", "\""))
    data['updated_at'] = updated_at
    table_name = 'swimmers'
    data_columns = [k for k in data.keys()]
    data_values = [v for v in data.values()]
    n_elements = len(data_columns)
    n_wildcards = ['%s' for x in range(n_elements+2)]
    sql = f'''
        INSERT INTO {table_name} (swimmer_id, {','.join(data_columns)}, ds) 
        VALUES ({','.join(n_wildcards)});
    '''
    values=[str(uuid.uuid1())]
    values = values + data_values
    values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(values)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        response=200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        response=error
    finally:
        if conn is not None:
            conn.close()
    return response


def get_secret():
    secret_name = "dev/lapp/postgresdb"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    json_secret = secret.replace("'", "\"")
    dict_secret = json.loads(json_secret)
    return dict_secret


def get_connection():
    lapp_db_secrets = get_secret()
    lappdb_username = lapp_db_secrets['username']
    lappdb_pw = lapp_db_secrets['password']
    lappdb_host = lapp_db_secrets['host']
    lappdb_port = int(lapp_db_secrets['port'])
    lappdb_engine = lapp_db_secrets['engine']
    connection = psycopg2.connect(user=lappdb_username,
                                  password=lappdb_pw,
                                  host=lappdb_host,
                                  port=lappdb_port,
                                  database=lappdb_engine)
    return connection