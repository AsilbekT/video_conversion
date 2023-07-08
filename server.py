import http.server
import socketserver
import os


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin',
                         '*')  # Allow all origins
        super().end_headers()


def serve_hls_files(directory, port=8000):
    # Change to the specified directory
    os.chdir(directory)

    # Create an HTTP server with custom request handler
    with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
        print(f"Serving HLS files at port {port}")
        httpd.serve_forever()


# Example usage
hls_directory = '/Users/asilbekturgunboev/Desktop/video_conversion/converted_videos/'
server_port = 8000

serve_hls_files(hls_directory, server_port)
