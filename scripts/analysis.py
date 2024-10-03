import json
from datetime import datetime
import os
from database import insert_result_into_db,load_database_config
from auth import token_required
from flask import Blueprint, request, jsonify
import mysql.connector
import pandas as pd
import joblib
import numpy as np

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/user-reports', methods=['GET'])
@token_required
def get_user_reports(current_user):
    try:
        db_config = load_database_config()
        conn = mysql.connector.connect(**db_config['development'])
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM analysis_results WHERE username = %s', (current_user['username'],))
        reports = cursor.fetchall()

        detailed_reports= []
        for report in reports:
            file_path = report["result_file_url"]
            if(os.path.exists(file_path)):
                with open(file_path,"r") as f:
                    report_data=json.load(f)
                detailed_reports.append(report_data)
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "reports": detailed_reports})
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "error": str(err)}), 500

@analysis_bp.route('/analysis', methods=['POST'])
@token_required
def analysis(current_user):
    if 'file' not in request.files:
        return jsonify({"status": "error", "error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "error": "No selected file"}), 400

    try:
        file_content = file.read().decode('utf-8')
        json_data = json.loads(file_content)

        model_path = os.path.dirname(__file__)
        voting_reg = joblib.load(os.path.join(model_path, '../model/voting_regressor_model.pkl'))
        scaler = joblib.load(os.path.join(model_path, '../model/scaler.pkl'))
        encoder = joblib.load(os.path.join(model_path, '../model/encoder.pkl'))
        
        categorical_columns = ['protocol', 'traffic_direction', 'is_encrypted', 'destination_device']
        numeric_columns = ['packet_rate', 'data_rate', 'cpu_usage', 'memory_usage', 'disk_usage',
                'network_traffic_in', 'network_traffic_out']

        for data in json_data:
            data_without_timestamp = {key: value for key, value in data.items() if key != 'timestamp'}
            
            new_packet_data = pd.DataFrame(data_without_timestamp)
            
            new_packet_categorical_encoded = encoder.transform(new_packet_data[categorical_columns])
            new_packet_numeric_scaled = scaler.transform(new_packet_data[numeric_columns])
            new_packet_combined = np.concatenate([new_packet_numeric_scaled, new_packet_categorical_encoded], axis=1)
            
            predicted_risk_score = voting_reg.predict(new_packet_combined)
            data['risk_score'] = round(predicted_risk_score[0], 2)

        filename = f'results/{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(json_data, f)

        insert_result_into_db(filename,current_user['username'])

        return jsonify({"status": "ok", "prediction": json_data})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
