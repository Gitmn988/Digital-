from flask import Flask, render_template, jsonify, request
import logging
import traceback
import os
import sys

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Aggiungi la directory principale al path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Percorsi dei file statici e dei template
static_folder = os.path.join(root_dir, 'static')
template_folder = os.path.join(root_dir, 'templates')

try:
    # Crea l'app Flask
    app = Flask(__name__, 
              static_folder=static_folder,
              template_folder=template_folder)

    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

    @app.route('/', methods=['GET'])
    def home():
        """Render the main bibliography generator page"""
        try:
            logger.debug("Rendering homepage")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Errore nel rendering della homepage: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for Vercel"""
        return jsonify({"status": "ok"})

    @app.route('/debug', methods=['GET'])
    def debug_info():
        """Debug endpoint per Vercel"""
        debug_info = {
            "environment": dict(os.environ),
            "paths": {
                "current_path": os.getcwd(),
                "static_path": app.static_folder,
                "template_path": app.template_folder,
                "sys_path": sys.path
            },
            "python_version": sys.version,
            "request": {
                "path": request.path,
                "url": request.url,
                "headers": dict(request.headers)
            }
        }
        return jsonify(debug_info)

    @app.errorhandler(404)
    def page_not_found(e):
        logger.error(f"404 Error: {str(e)}")
        return jsonify({"error": "Page not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"500 Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

except Exception as e:
    logger.critical(f"Errore durante l'inizializzazione dell'app: {str(e)}")
    logger.critical(traceback.format_exc())
    
    # Crea un'app minima per il fallback
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        error_message = f"Errore critico nell'inizializzazione dell'app: {str(e)}"
        logger.critical(error_message)
        return jsonify({"error": error_message, "traceback": traceback.format_exc()}), 500