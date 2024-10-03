import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from flask import Flask
from auth import auth_bp
from analysis import analysis_bp
from config import SECRET_KEY
from flask_cors import CORS

app = Flask(__name__)
# Allow cross-domain requests
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

app.config['SECRET_KEY']=SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(analysis_bp)

if __name__ == '__main__':
    app.run(debug=True)
