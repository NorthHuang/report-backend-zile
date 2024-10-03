import mysql.connector
import yaml
import os

def load_database_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '../database.yml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def insert_result_into_db(file_url,username):
    db_config = load_database_config()
    try:
        conn = mysql.connector.connect(**db_config['development'])
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO analysis_results (result_file_url, username)
            VALUES (%s, %s)
        ''', (file_url,username))

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
