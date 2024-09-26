from flask import Flask, request, jsonify
import json
import os
import yaml
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def load_database_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, './database.yml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def insert_result_into_db(file_url):
    db_config = load_database_config()
    
    try:
        conn = mysql.connector.connect(**db_config['development'])
        cursor = conn.cursor()

        created_at = updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO analysis_results (result_file_url)
            VALUES (%s)
        ''', (file_url,))

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

@app.route('/analysis', methods=['POST'])
def analysis():
    if 'file' not in request.files:
        return jsonify({"status": "error", "error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": "error", "error": "No selected file"}), 400

    try:
        file_content = file.read().decode('utf-8')
        json_data = json.loads(file_content)

        # TODO need to add model code and use json_data variable (code below is not real, just for placeholder)
        prediction = {
                "status": "success",
                "analysis_time": "2024-08-26T12:10:00Z",
                "summary": {
                    "total_attacks_detected": 5,
                    "critical_warnings": 2,
                    "system_health_status": "warning"
                },
                "details": {
                    "network_traffic_analysis": [
                        {
                            "attack_type": "DDoS",
                            "source_ip": "192.168.1.4",
                            "target_ip": "192.168.1.5",
                            "timestamp": "2024-08-26T12:00:05Z",
                            "severity": "high",
                            "description": "Detected Distributed Denial of Service attack targeting port 80."
                        },
                        {
                            "attack_type": "Port Scan",
                            "source_ip": "192.168.1.6",
                            "target_ip": "192.168.1.7",
                            "timestamp": "2024-08-26T12:02:00Z",
                            "severity": "medium",
                            "description": "Multiple ports scanned from a single IP address, indicating possible reconnaissance."
                        },
                        {
                            "attack_type": "DDoS",
                            "source_ip": "192.168.1.4",
                            "target_ip": "192.168.1.5",
                            "timestamp": "2024-08-26T12:40:05Z",
                            "severity": "high",
                            "description": "Detected Distributed Denial of Service attack targeting port 443."
                        }
                    ],
                    "system_logs_analysis": [
                        {
                            "event_type": "Failed Login",
                            "hostname": "server1",
                            "service": "sshd",
                            "timestamp": "2024-08-26T12:00:00Z",
                            "user": "user1",
                            "source_ip": "192.168.1.100",
                            "severity": "low",
                            "description": "Repeated failed login attempts detected, may indicate brute force attack."
                        },
                        {
                            "event_type": "Service Error",
                            "hostname": "server1",
                            "service": "nginx",
                            "timestamp": "2024-08-26T12:07:00Z",
                            "severity": "medium",
                            "description": "Nginx service failed to start due to missing configuration file."
                        },
                                                {
                            "event_type": "Service Error",
                            "hostname": "server1",
                            "service": "nginx",
                            "timestamp": "2024-08-26T12:20:00Z",
                            "severity": "medium",
                            "description": "Nginx service failed to start due to missing configuration file."
                        }
                    ],
                    "system_health_analysis": [
                        {
                            "timestamp": "2024-08-26T12:00:00Z",
                            "cpu_usage": {
                                "current": 85.2,
                                "threshold": 80.0,
                                "status": "warning",
                                "description": "CPU usage exceeded threshold, indicating possible system overload."
                            },
                            "memory_usage": {
                                "current": 65.3,
                                "threshold": 90.0,
                                "status": "normal",
                                "description": "Memory usage within normal range."
                            },
                            "disk_usage": {
                                "current": 88.7,
                                "threshold": 85.0,
                                "status": "warning",
                                "description": "Disk usage exceeded threshold, potential risk of disk space exhaustion."
                            },
                            "network_bandwidth_usage": {
                                "current_in": 750,
                                "current_out": 500,
                                "threshold": 1000,
                                "status": "normal",
                                "description": "Network bandwidth usage within acceptable limits."
                            }
                        },
                        {
                            "timestamp": "2024-08-26T12:05:00Z",
                            "cpu_usage": {
                                "current": 90.1,
                                "threshold": 80.0,
                                "status": "critical",
                                "description": "CPU usage critically high, indicating possible attack or resource overuse."
                            },
                            "memory_usage": {
                                "current": 75.5,
                                "threshold": 90.0,
                                "status": "normal",
                                "description": "Memory usage within normal range."
                            },
                            "disk_usage": {
                                "current": 92.1,
                                "threshold": 85.0,
                                "status": "critical",
                                "description": "Disk usage critically exceeded threshold, immediate action required."
                            },
                            "network_bandwidth_usage": {
                                "current_in": 850,
                                "current_out": 600,
                                "threshold": 1000,
                                "status": "warning",
                                "description": "Network bandwidth usage approaching limit."
                            }
                        },
                        {
                            "timestamp": "2024-08-26T12:10:00Z",
                            "cpu_usage": {
                                "current": 87.1,
                                "threshold": 80.0,
                                "status": "critical",
                                "description": "CPU usage critically high, indicating possible attack or resource overuse."
                            },
                            "memory_usage": {
                                "current": 70.5,
                                "threshold": 90.0,
                                "status": "normal",
                                "description": "Memory usage within normal range."
                            },
                            "disk_usage": {
                                "current": 95.1,
                                "threshold": 85.0,
                                "status": "critical",
                                "description": "Disk usage critically exceeded threshold, immediate action required."
                            },
                            "network_bandwidth_usage": {
                                "current_in": 800,
                                "current_out": 650,
                                "threshold": 1000,
                                "status": "warning",
                                "description": "Network bandwidth usage approaching limit."
                            }
                        }
                    ]
                },
                "recommendations": [
                    "Investigate the source of the DDoS attack and consider blocking the IP address 192.168.1.4.",
                    "test",
                    "Increase disk space or clean up unnecessary files to avoid disk exhaustion."
                ]
            }

        filename = f'results/{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(prediction, f)

        insert_result_into_db(filename)

        # TODO need to change to the real model prediction result, just return a static json temporarily
        response = {
            "status": "ok",
            "prediction": prediction
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
