import http.server
import socketserver


PORT = 8459
ZIP_FILES_LOCATION = "./Latest_Version/BetterDiscord.zip"


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return ZIP_FILES_LOCATION


def start_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")
            httpd.server_close()
        except Exception as e:
            print(f"Unexpected error: {e}")
