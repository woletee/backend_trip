from flask import Flask, jsonify, request
import logging
import os
from dotenv import load_dotenv
import json
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load hotel data from JSON file
def load_hotel_data():
    try:
        with open('Hotels_Final.json', 'r') as file:
            data = json.load(file)
            logging.debug(f"Hotel data loaded: {data}")
            return data
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        logging.error(f"Error loading hotel data: {e}")
        return []

# Function to get all hotels
def get_all_hotels():
    try:
        hotels = load_hotel_data()
        return hotels
    except KeyError as e:
        logging.error(f"Key error: {e}")
        return {'error': f"Key error: {e}"}
    except Exception as e:
        logging.error(f"General Error: {e}")
        return {'error': str(e)}

@app.route('/', methods=['GET'])
def home():
    logging.debug("Default route '/' was called")
    return jsonify({'message': 'Welcome to the Hotels API. Use /api/all-hotels to get all the hotels.'})

@app.route('/api/all-hotels', methods=['GET'])
def api_all_hotels():
    logging.debug("API endpoint '/api/all-hotels' was called")
    all_hotels = get_all_hotels()
    if 'error' in all_hotels:
        return jsonify(all_hotels), 500
    return jsonify(all_hotels)

@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"404 Error: {request.url} was not found on the server.")
    return jsonify({'error': 'Not Found', 'message': f"The requested URL {request.url} was not found on the server."}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 Error: Internal server error at {request.url}. Error: {error}")
    return jsonify({'error': 'Internal Server Error', 'message': 'An internal server error occurred.'}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    logging.error(f"Unhandled Exception: {error}")
    return jsonify({'error': 'Server Error', 'message': str(error)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
