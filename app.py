from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Конфігурація бази даних (Render надає DATABASE_URL як змінну середовища)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для таблиці
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return "API працює. Використовуйте /data для POST, PUT, GET, DELETE."

@app.route('/data', methods=['POST'])
def create_data():
    value = request.json.get('value')
    if not value:
        return jsonify({"error": "Missing 'value' parameter"}), 400
    new_data = Data(value=value)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Created", "id": new_data.id}), 201

@app.route('/data', methods=['GET'])
def get_data():
    all_data = Data.query.all()
    result = {item.id: item.value for item in all_data}
    return jsonify(result), 200

@app.route('/data', methods=['PUT'])
def update_data():
    data_id = request.json.get('id')
    value = request.json.get('value')
    data_item = Data.query.get(data_id)
    if not data_item:
        return jsonify({"error": "Not found"}), 404
    data_item.value = value
    db.session.commit()
    return jsonify({"message": "Updated"}), 200

@app.route('/data', methods=['DELETE'])
def delete_data():
    data_id = request.json.get('id')
    data_item = Data.query.get(data_id)
    if not data_item:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(data_item)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=8080, use_reloader=False)
