# Earthquake API blueprint
from flask import Blueprint, jsonify, request
from .utils.usgs_service import USGSService

earthquake_bp = Blueprint('earthquake', __name__, url_prefix='/api/earthquake')
usgs_service = USGSService()

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
    
    # Fetch earthquake data with fixed parameters
    raw_data = usgs_service.get_earthquake_data(
        start_time, 
        end_time
    )
    # print(raw_data)
    
    if raw_data is None:
        return jsonify({"error": "Failed to fetch earthquake data"}), 500
    
  
    return jsonify(raw_data)