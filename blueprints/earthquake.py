# Earthquake API blueprint
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import json

from .utils.usgs_service import USGSService

earthquake_bp = Blueprint('earthquake', __name__, url_prefix='/api/earthquake')
usgs_service = USGSService()

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP Requests by method and endpoint',
    ['method', 'endpoint', 'status']
)

@earthquake_bp.before_request
def before_request():
    http_requests_total.labels(request.method, request.path, 'pending').inc()

@earthquake_bp.after_request
def after_request(response):
    if response.status_code == 200:
        http_requests_total.labels(request.method, request.path, 'success').inc()
    else:
        http_requests_total.labels(request.method, request.path, 'failure').inc()
    return response

@earthquake_bp.route('/data', methods=['GET'])
def get_earthquake_data():
    """Endpoint to get earthquake data for a specified time range.
    
    Query Parameters:
        start_time (str): Start date in YYYY-MM-DD format
        end_time (str): End date in YYYY-MM-DD format
    
    Returns:
        JSON: Processed earthquake data
    """
    # Get parameters from the request
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    # Validate required parameters
    if not start_time or not end_time:
        return jsonify({"error": "Both start_time and end_time parameters are required"}), 400

    # Validate that start time is earlier than the end time
    start_time_v = datetime.fromisoformat(start_time)
    end_time_v = datetime.fromisoformat(end_time)

    if start_time_v >= end_time_v:
        return jsonify({'error': 'start_time must be earlier than end_time'}), 400
    
    # Fetch earthquake data with fixed parameters
    raw_data = usgs_service.get_earthquake_data(
        start_time, 
        end_time
    )
    # print(raw_data)
    
    if raw_data is None:
        return jsonify({"error": "Failed to fetch earthquake data"}), 500
    
  
    return jsonify(raw_data)

@earthquake_bp.route('/critical', methods=['GET'])
def get_critical_data():
    """Endpoint to get earthquake data for a specified time range with 10+ reports.
    
    Query Parameters:
        start_time (str): Start date in YYYY-MM-DD format
        end_time (str): End date in YYYY-MM-DD format
    
    Returns:
        JSON: Processed earthquake data
    """

    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    # Validate required parameters
    if not start_time or not end_time:
        return jsonify({"error": "Both start_time and end_time parameters are required"}), 400

    # Validate that start time is earlier than the end time
    start_time_v = datetime.fromisoformat(start_time)
    end_time_v = datetime.fromisoformat(end_time)

    if start_time_v >= end_time_v:
        return jsonify({'error': 'start_time must be earlier than end_time'}), 400
    
    # Fetch earthquake data with fixed parameters
    raw_data = usgs_service.get_critical_earthquake_reported(
        start_time, 
        end_time
    )
    # print(raw_data)
    
    if raw_data is None:
        return jsonify({"error": "Failed to fetch earthquake data"}), 500
    
  
    return jsonify(raw_data)

@earthquake_bp.route("/tsunami", methods=["GET"])
def get_tsunami_data():
    """Endpoint to get earthquake data for the previous day which had tsunami alert.
    
    Query Parameters:
        date (str): Date in YYYY-MM-DD format
    
    Returns:
        JSON: Processed earthquake data
    """

    # Change to input date to the previous date
    date = request.args.get('date')
    date = datetime.strptime(date, "%Y-%m-%d").date()
    previous_date = date - timedelta(days=1)
    previous_date = previous_date.strftime("%Y-%m-%d")
    # print(previous_date)

    # Format the input state name to desired name
    state = request.args.get('state')
    state = state.lower()
    state = state.replace(" ", "")
    # print(state)

    # Validate the parameters
    if not date or not state:
        return jsonify({"error": "Both start_time and state parameters are required"}), 400

    # Fetch earthquake data with fixed parameters
    raw_data = usgs_service.get_previous_date_tsunami_data(
        previous_date,
        state
    )

    if raw_data is None:
        return jsonify({"error": "Failed to fetch earthquake data"}), 500

    return jsonify(raw_data)

@earthquake_bp.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy"}

@earthquake_bp.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
