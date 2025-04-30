from .server import app

# This is the handler that Vercel will use
def handler(request, context):
    """Handle a request to the serverless function."""
    return app 