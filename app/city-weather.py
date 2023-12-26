# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route('/')
# def get_static_data():
#     data = {
#         'message': 'disco pickle',
#         'status': 'success'
#     }
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



import requests
from flask import Flask, jsonify

def get_weather(api_key, city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'q': city,
        'key': api_key,
        'aqi': 'no'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        temperature = data['current']['temp_c']
        return f"Current temperature in {city}: {temperature}C."

    except requests.RequestException as e:
        return f"Error: {str(e)}"

app = Flask(__name__)

@app.route('/')
def get_weather_data():
    result = get_weather(api_key, city)
    data = {
        'message': result,
        'status': 'success' if 'Error' not in result else 'failure'
    }
    return jsonify(data)

if __name__ == "__main__":
    api_key = "944c815cb09a43ca89f100329232112"
    city = "Vienna"

    app.run(host='0.0.0.0', port=5000)
