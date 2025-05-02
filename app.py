from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return "API працює. Використовуйте /data для POST, PUT, GET, DELETE."

@app.route('/data', methods=['GET'])
def get_data():
    all_data = Data.query.all()
    return jsonify([{ "id": d.id, "value": d.value } for d in all_data]), 200

@app.route('/data', methods=['POST'])
def create_data():
    value = request.json.get('value')
    if not value:
        return jsonify({"error": "Missing 'value' parameter"}), 400
    new_entry = Data(value=value)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Created"}), 201

@app.route('/data', methods=['PUT'])
def update_data():
    data_id = request.json.get('id')
    value = request.json.get('value')
    entry = Data.query.get(data_id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    entry.value = value
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

@app.route('/data', methods=['DELETE'])
def delete_data():
    data_id = request.json.get('id')
    entry = Data.query.get(data_id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

@app.route('/healthz')
def healthz():
    try:
        db.session.execute('SELECT 1')
        return 'Database is connected!', 200
    except Exception as e:
        return f"Database connection error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
