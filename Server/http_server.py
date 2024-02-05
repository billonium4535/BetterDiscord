import http.server
import socketserver


PORT = 8459
ZIP_FILES_LOCATION = "./Latest_Version/BetterDiscord.zip"


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return ZIP_FILES_LOCATION


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    httpd.serve_forever()
