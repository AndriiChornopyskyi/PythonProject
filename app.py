from flask import Flask, request, jsonify

app = Flask(__name__)

# Створимо словник для зберігання даних (CRUD)
data = {}
id_counter = 1
@app.route('/')
def home():
    return "API працює. Використовуйте /data для POST, PUT, GET, DELETE."
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data), 200

@app.route('/data', methods=['POST'])
def create_data():
    global id_counter
    value = request.json.get('value')
    if not value:
        return jsonify({"error": "Missing 'value' parameter"}), 400
    data[id_counter] = value
    id_counter += 1
    return jsonify({"message": "Created"}), 201

@app.route('/data', methods=['PUT'])
def update_data():
    data_id = request.json.get('id')
    value = request.json.get('value')
    if data_id not in data:
        return jsonify({"error": "Not found"}), 404
    data[data_id] = value
    return jsonify({"message": "Updated"}), 200

@app.route('/data', methods=['DELETE'])
def delete_data():
    data_id = request.json.get('id')
    if data_id not in data:
        return jsonify({"error": "Not found"}), 404
    del data[data_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
