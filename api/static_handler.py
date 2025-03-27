import os
import mimetypes
import base64

def static_file_handler(path):
    """
    Function to handle static file requests
    """
    try:
        # Determine the root directory (parent of api folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Construct the full file path
        file_path = os.path.join(root_dir, path.lstrip('/'))
        
        # Check if file exists
        if not os.path.isfile(file_path):
            return {
                'statusCode': 404,
                'body': f'File not found: {path}',
                'headers': {'Content-Type': 'text/plain'}
            }
        
        # Get the MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        # Read the file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Encode binary data for images, fonts, etc.
        is_binary = not mime_type.startswith(('text/', 'application/json'))
        if is_binary:
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            return {
                'statusCode': 200,
                'body': encoded_content,
                'isBase64Encoded': True,
                'headers': {'Content-Type': mime_type}
            }
        else:
            # Text files can be returned as-is
            return {
                'statusCode': 200,
                'body': file_content.decode('utf-8'),
                'headers': {'Content-Type': mime_type}
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error serving static file: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }