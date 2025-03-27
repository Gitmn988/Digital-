from index import app, handler

# Vercel handler
def serverless_handler(environ, start_response):
    return handler(environ, start_response)