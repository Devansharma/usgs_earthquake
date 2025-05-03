# Main application entry point
from flask import Flask, jsonify
from blueprints.earthquake import earthquake_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(earthquake_bp)
    
    # Default route
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "service": "USGS Earthquake API",
            "endpoint": "/api/earthquake/data?start_time=YYYY-MM-DD&end_time=YYYY-MM-DD"
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)