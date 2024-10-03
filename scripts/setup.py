import mysql.connector
import yaml
import os

def create_results_directory():
    if not os.path.exists('results'):
        os.makedirs('results')
        print("Created 'results' directory.")
    else:
        print("'results' directory already exists.")

def load_database_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '../database.yml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def create_table():
    print("Start creating user and analysis_results tables without foreign key..........")
    config = load_database_config()
    connection = mysql.connector.connect(**config['development'])  # Change to appropriate environment
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            result_file_url VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL, -- 关联用户的 username，但不设置外键
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    cursor.close()
    connection.close()
    print("Created user and analysis_results tables successfully.")


if __name__ == "__main__":
    create_results_directory()

    create_table()