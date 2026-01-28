"""
DevOps Info Service - Flask implementation for Lab 1 Task 1
"""
import os
import socket
import platform
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Application start time (UTC)
START_TIME = datetime.now(timezone.utc)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info('DevOps Info Service starting')


def get_uptime():
    delta = datetime.now(timezone.utc) - START_TIME
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {
        'seconds': seconds,
        'human': f"{hours} hours, {minutes} minutes"
    }


def get_system_info():
    return {
        'hostname': socket.gethostname(),
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'cpu_count': os.cpu_count() or 1,
        'python_version': platform.python_version(),
    }


@app.route('/')
def index():
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

    uptime = get_uptime()
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    info = {
        'service': {
            'name': 'devops-info-service',
            'version': '1.0.0',
            'description': 'DevOps course info service',
            'framework': 'Flask'
        },
        'system': get_system_info(),
        'runtime': {
            'uptime_seconds': uptime['seconds'],
            'uptime_human': uptime['human'],
            'current_time': now,
            'timezone': 'UTC'
        },
        'request': {
            'client_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'method': request.method,
            'path': request.path
        },
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Service information'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'}
        ]
    }

    return jsonify(info)


@app.route('/health')
def health():
    uptime = get_uptime()
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    return jsonify({
        'status': 'healthy',
        'timestamp': now,
        'uptime_seconds': uptime['seconds']
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'Endpoint does not exist'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
