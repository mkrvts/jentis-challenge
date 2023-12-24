from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def get_static_data():
    data = {
        'message': 'disco pickle',
        'status': 'success'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)