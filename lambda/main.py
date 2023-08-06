import json
import psycopg2
from datetime import datetime
from google.cloud.sql.connector import Connector
import sqlalchemy
import logging

def write_to_db(event):
    epochms = event['requestContext']['timeEpoch']
    data = json.loads(event['body'].replace("'", "\""))
    data['updated_at'] = datetime.fromtimestamp(epochms/1000).strftime('%Y-%m-%d')
    table_name = 'swimmer'
    data_columns = [k for k in data.keys()]
    data_values = [v for v in data.values()]
    n_elements = len(data_columns)
    n_wildcards = ['%s' for x in range(n_elements+2)]
    sql = f'''
        INSERT INTO {table_name} (swimmer_id, {','.join(data_columns)}, ds) 
        VALUES ({','.join(n_wildcards)});
    '''
    data_values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logging.info(f'inserting {data_values}')
    conn = create_pooled_connection()
    with conn.connect() as db_conn:
        try:
            db_conn.execute(sql, values)
        except (Exception, psycopg2.DatabaseError) as error:
            logging.info(error)
            response = error
        finally:
            if conn is not None:
                conn.close()
    return response


def get_secret():
    # todo
    return

# function to return the database connection
def getconn():
    connector = Connector()
    conn = connector.connect(
        "project:region:instance-name", #todo
        "pg8000",
        user="my-user",
        password="my-password",
        db="my-database"
    )
    return conn

def create_pooled_connection():
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn
    )
    return pool
