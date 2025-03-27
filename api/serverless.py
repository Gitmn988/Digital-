from flask import Flask
import os
import sys
import logging
import traceback

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Aggiungi la directory principale al path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logger.debug(f"Path aggiunto: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    logger.debug(f"sys.path ora contiene: {sys.path}")
    
    # Importa la tua app Flask
    from api.app import app as flask_app
    logger.debug("L'app Flask è stata importata correttamente")
    
    def handler(request, **kwargs):
        logger.debug(f"Handler invocato con richiesta: {request.url}")
        try:
            return flask_app
        except Exception as e:
            logger.error(f"Errore nel gestore: {str(e)}")
            logger.error(traceback.format_exc())
            # Fallback minimale per rispondere
            app = Flask(__name__)
            response = app.make_response(f"Errore del server: {str(e)}")
            response.status_code = 500
            return response

except Exception as e:
    logger.critical(f"Errore durante l'inizializzazione: {str(e)}")
    logger.critical(traceback.format_exc())
    
    # Crea un'app minima in caso di errore
    app = Flask(__name__)
    
    def handler(request, **kwargs):
        error_message = f"Errore critico nell'inizializzazione: {str(e)}"
        logger.critical(error_message)
        response = app.make_response(error_message)
        response.status_code = 500
        return response