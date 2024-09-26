# report-backend-zile
network analysis report backend code for TIP of Swinburne

## Prerequisites

- Python 3.x installed
- MySQL server running locally or on a remote server
- `pip3` installed for managing Python packages

## Steps to Set Up and Run the Project

### 1. Install Dependencies

Before starting, install all the required dependencies using `pip`. Run the following command:

```bash
pip3 install -r requirements.txt
```

### 2. Setup your own DB config(using mysql)
Copy database.yml.example to database.yml

Make sure to update the values according to your MySQL setup:

host: the hostname or IP address where MySQL is running (usually localhost for local development)
port: the port MySQL is listening on (usually 3306)
username: your MySQL username
password: your MySQL password
database: the database name you are using

### 3. Run setup script to be ready
```
python3 scripts/setup.py
```

### 4. Start service
```
python3 -m flask run --debug
```