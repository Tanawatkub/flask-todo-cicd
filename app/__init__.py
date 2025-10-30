import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db
from app.routes import api
from app.config import config


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # ---------------- Enable CORS ----------------
    # ✅ รองรับ Localhost, Network IP, GitHub Pages และ Render
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",             # สำหรับ dev local
                "http://127.0.0.1:3000",
                "http://192.168.1.103:3000",         # ✅ Network IP
                "https://tanawatputta.github.io",    # ✅ GitHub Pages
                "https://flask-todo-app-3r5b.onrender.com"  # ✅ Render backend
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": False
        }
    })

    # ---------------- Initialize Extensions ----------------
    db.init_app(app)

    # ---------------- Register Routes ----------------
    app.register_blueprint(api, url_prefix="/api")

    # ---------------- Root Endpoint ----------------
    @app.route("/")
    def index():
        return jsonify({
            "message": "Flask Todo API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/health",
                "todos": "/api/todos"
            }
        })

    # ---------------- Error Handlers ----------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions safely"""
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

    # ---------------- Create Database Tables ----------------
    with app.app_context():
        db.create_all()

    return app
