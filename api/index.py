import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the Flask app
from app import app

# Vercel serverless function handler
def handler(environ, start_response):
    return app(environ, start_response)

# Lambda compatibility
def lambda_handler(event, context):
    # Convert API Gateway event to WSGI environ
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    query_string = event.get('queryStringParameters', {}) or {}
    
    # Build query string
    query_string_str = '&'.join([f"{k}={v}" for k, v in query_string.items()])
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string_str,
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': headers.get('content-length', '0'),
        'SERVER_NAME': 'vercel.app',
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.input': sys.stdin,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
    }
    
    # Add headers
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            environ[f'HTTP_{key}'] = value
    
    # Handle request body
    if method in ['POST', 'PUT', 'PATCH']:
        body = event.get('body', '')
        if isinstance(body, str):
            environ['wsgi.input'] = sys.stdin
        environ['CONTENT_LENGTH'] = str(len(body))
    
    # Capture response
    response_data = {}
    
    def start_response(status, response_headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = response_headers
    
    # Get response from Flask app
    response = app(environ, start_response)
    response_body = b''.join(response)
    
    # Convert to API Gateway response format
    return {
        'statusCode': int(response_data['status'].split()[0]),
        'headers': dict(response_data['headers']),
        'body': response_body.decode('utf-8')
    }

# For local testing
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
