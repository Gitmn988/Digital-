from flask import Flask, render_template, send_from_directory, jsonify
import os
import sys
import traceback
import logging
import mimetypes

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import il handler statico
from api.static_handler import static_file_handler

def handler(event, context):
    """
    Handler for AWS Lambda via Vercel
    """
    try:
        path = event.get('path', '')
        
        # Se il percorso inizia con /static, utilizziamo l'handler dedicato
        if path.startswith('/static/'):
            return static_file_handler(path)
            
        # Altrimenti, passiamo alla nostra app Flask
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Percorsi dei file statici e dei template
        static_folder = os.path.join(root_dir, 'static')
        template_folder = os.path.join(root_dir, 'templates')
        
        # Crea l'app Flask
        app = Flask(__name__,
                   static_folder=static_folder,
                   template_folder=template_folder)
        
        # Variabili per la risposta
        status_code = 200
        headers = {'Content-Type': 'text/html'}
        body = ''
        
        # Route principale
        if path == '/' or path == '':
            try:
                # Renderizza il template index.html
                with open(os.path.join(template_folder, 'index.html'), 'r') as f:
                    body = f.read()
            except Exception as e:
                logger.error(f"Errore nel rendering dell'indice: {str(e)}")
                status_code = 500
                headers = {'Content-Type': 'application/json'}
                body = jsonify({"error": str(e)}).get_data(as_text=True)
        
        # Health check API
        elif path == '/api/health':
            headers = {'Content-Type': 'application/json'}
            body = '{"status": "ok"}'
        
        # Debug API
        elif path == '/debug':
            debug_info = {
                "environment": dict(os.environ),
                "paths": {
                    "current_path": os.getcwd(),
                    "static_path": static_folder,
                    "template_path": template_folder,
                },
                "event": event
            }
            headers = {'Content-Type': 'application/json'}
            import json
            body = json.dumps(debug_info)
            
        # 404 per tutti gli altri percorsi
        else:
            status_code = 404
            headers = {'Content-Type': 'application/json'}
            body = '{"error": "Page not found"}'
            
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': body
        }
        
    except Exception as e:
        logger.error(f"Errore serverless: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Internal Server Error", "details": "{str(e)}"}}'
        }