#!/usr/bin/env python3
import http.server
import socketserver
import os
from functools import partial

# Custom request handler to serve files from the project directory
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/workspace/etax-mobile-pwa/source", **kwargs)

# Also serve debugging tools from the workspace root
class DebugHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Check if the request is for debugging tools
        if path.startswith('/debug_') or path in ['/', '/inject_debug.js', '/debug_config.json']:
            # Serve debugging tools from workspace root
            return '/workspace' + path
        else:
            # Serve main site files from etax-mobile-pwa/source
            return '/workspace/etax-mobile-pwa/source' + path
    
    def end_headers(self):
        # Add CORS headers to allow debugging tools to access all resources
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

# Create a custom handler that can serve both directories
class MultiDirHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.base_dir = "/workspace/etax-mobile-pwa/source"
        self.debug_dir = "/workspace"
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        # If the path is for debugging tools, serve from debug_dir
        if any(keyword in path for keyword in ['debug_', 'inject_debug', 'debug_config', 'comprehensive_debug']):
            return self.debug_dir + path
        else:
            # Otherwise serve from base_dir
            return self.base_dir + path
    
    def end_headers(self):
        # Add CORS headers to allow debugging tools to access all resources
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

# Start the server on port 8082 to avoid conflicts
PORT = 8082

Handler = MultiDirHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    print("Serving eTax Mobile PWA files from /workspace/etax-mobile-pwa/source")
    print("Serving debugging tools from /workspace/")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")