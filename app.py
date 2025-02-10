from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from model import search_instruction_ai, generate_image_from_prompt

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Sample route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

# API for searching generic instructions
@app.route('/api/v1/search/instructions', methods=['GET'])
def search_instruction():
    try:
        product = request.args.get('product')
        if not product:
            return jsonify({'error': 'Missing product parameter'}), 400
        
        action = request.args.get('action')
        if not action:
            return jsonify({'error': 'Missing action parameter'}), 400

        role = request.args.get('role')
        if not role:
            return jsonify({'error': 'Missing role parameter'}), 400
        
        # Your logic here
        result = search_instruction_ai(role, product, action)
        print("search result: ", result)
        result = {
            'message': 'Success',
            'step_count': len(result),
            'steps': result
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API for generating instructions manuals (LEGO-style)
@app.route('/api/v1/generate/instructions/lego', methods=['POST'])
def generate_graphics():
    try:
        body: Dict[str, Any] = request.get_json()

        if not body or 'steps' not in body or 'product' not in body:
            return jsonify({'error': 'Missing fields in request body'}), 400
            
        # Your logic here
        product  = body.get('product')
        steps = body.get('step') ## TODO: parse and process steps into list
        generate_image_from_prompt(product = product, steps = steps)
        result = {'message': 'Success'}
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 