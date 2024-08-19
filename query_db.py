# -*- coding: utf-8 -*-
from config import config
import psycopg2
import psycopg2.extras
import json

# Store results from database request
db_results = []

# SQL Command to Query database


def setSqlCmd(trans_id):
    trans_id_query = 'SELECT id, concat(subdir,' + "'/'" + \
        ', name) path,  hashsum, hashtype, size, mimetype, mtime, transaction_id FROM public.files WHERE transaction_id = ' + \
        str(trans_id) + ';'
    return trans_id_query

# Query Local DB and return results
# create a connections.ini file on your local to store local database connection


def getUserList(trans_id):
    postgres_config = config('connections.ini', 'postgresql')
    conn = psycopg2.connect(host=postgres_config['host'],
                            port=postgres_config['port'],
                            database=postgres_config['database'],
                            user=postgres_config['user'],
                            # password = postgres_config['password']
                            )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query_cmd = setSqlCmd(trans_id)
    cur.execute(query_cmd)
    query_results = cur.fetchall()
    return query_results

# Print results to JSON formated array


def printToArray(user_list, trans_id):
    for row in user_list:
        db_results.append({
            'id': '{}'.format(row['id']),
            'path': '{}'.format(row['path']),
            'hashsum': '{}'.format(row['hashsum']),
            'hashtype': '{}'.format(row['hashtype']),
            'size': '{}'.format(row['size']),
            'mimetype': '{}'.format(row['mimetype']),
            'mtime': '{}'.format(row['mtime']),
        })
        # print(db_results)
    results = json.dumps(db_results)
    # print(results)
    print(f'Success! {trans_id} Postgres DB Query Successful')
    return results

# Retrieve the list of users who have contact ID's and their institution association


def main(trans_id):
    user_list = getUserList(trans_id)
    query_results = printToArray(user_list, trans_id)


if __name__ == '__main__':
    main(trans_id)
