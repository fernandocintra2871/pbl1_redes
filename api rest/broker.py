from flask import Flask, jsonify, request

app = Flask(__name__)

data = {
    "1": {"state": True, "temperature": 22},
    "2": {"state": False, "temperature": 21},
    "3": {"state": True, "temperature": 27},
    "4": {"state": False, "temperature": 19}
}

@app.route('/sensors', methods=['GET'])
def get_sensors():
    if request.method == 'GET':
        return jsonify(data)

@app.route('/sensors/<id>', methods=['PATCH'])
def patch_sensor(id):
    if request.method == 'PATCH':
        sensor = data.get(id)
        if sensor:
            partial_data = request.json
            data[id]['state'] = partial_data['state']
            return jsonify(data[id])
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404




app.run(host='0.0.0.0', port=5000)
