from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from brain.logic import generate_reply, update_mood, remember_chat

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed.query)
        msg = query.get("msg", [""])[0]

        update_mood(msg)
        reply = generate_reply(msg)
        remember_chat(msg, reply)

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(reply.encode("utf-8"))

def run():
    print("🧠 Siya's brain server running at http://localhost:7860")
    HTTPServer(("localhost", 7860), SimpleHandler).serve_forever()

if __name__ == "__main__":
    run()
