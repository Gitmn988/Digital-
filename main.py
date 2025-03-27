from flask import Flask, render_template, send_from_directory, jsonify
import os
import logging
import traceback

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Percorsi dei file statici e dei template
current_dir = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(current_dir, 'static')
template_folder = os.path.join(current_dir, 'templates')

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

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files explicitly"""
    try:
        logger.debug(f"Servendo file static: {filename}")
        logger.debug(f"Path completo: {os.path.join(static_folder, filename)}")
        if os.path.exists(os.path.join(static_folder, filename)):
            logger.debug(f"Il file {filename} esiste!")
        else:
            logger.error(f"Il file {filename} NON esiste!")
            
        return send_from_directory(static_folder, filename)
    except Exception as e:
        logger.error(f"Errore nel servire file statico: {filename}, {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon file"""
    try:
        logger.debug("Servendo favicon.ico")
        return send_from_directory(static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        logger.error(f"Errore nel servire favicon: {str(e)}")
        # Se non esiste, restituiamo un'immagine vuota per evitare errori 404
        return '', 204

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Vercel"""
    return jsonify({"status": "ok"})

@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"404 Error: {str(e)}")
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 Error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
