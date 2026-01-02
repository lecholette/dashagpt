"""
DashaGPT - AI-Powered Vedic Astrology Application

Main Flask application entry point.
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_compress import Compress
from flask_cors import CORS


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

    # Extensions
    Compress(app)
    CORS(app)

    # Register routes
    register_routes(app)

    # Error handlers
    register_error_handlers(app)

    return app


def register_routes(app):
    """Register all application routes."""

    @app.route('/')
    def index():
        """Landing page."""
        return render_template('landing.html')

    @app.route('/calculator')
    def calculator():
        """Birth chart calculator form."""
        return render_template('calculator.html')

    @app.route('/api/calculate', methods=['POST'])
    def api_calculate():
        """API endpoint for chart calculation."""
        data = request.get_json()
        # TODO: Implement chart calculation
        return jsonify({'status': 'success', 'message': 'Not yet implemented'})

    @app.route('/robots.txt')
    def robots_txt():
        """Robots.txt for SEO."""
        return app.send_static_file('robots.txt')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        """XML sitemap for SEO."""
        return app.send_static_file('sitemap.xml')


def register_error_handlers(app):
    """Register error handlers."""

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('errors/500.html'), 500


# Create the app instance
app = create_app()


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
