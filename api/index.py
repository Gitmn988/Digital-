import sys
import os

# Aggiungi la directory principale al path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Importa l'app Flask da main.py
from main import app

# Handler per Vercel serverless
def handler(environ, start_response):
    return app(environ, start_response)