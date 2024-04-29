from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

# import main

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("index.html", "rb") as f:
                self.wfile.write(f.read())

            # self.wfile.write(bytes("<html><head><title>lua-api-learning</title></head>", "utf-8"))
            # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            # self.wfile.write(bytes("<body>", "utf-8"))
            # self.wfile.write(bytes("<h1>This is an example web server for a Lua API game.</h1>", "utf-8"))


            # self.wfile.write(bytes("<canvas id=\"drawCanvas\" width=\"1024\" height=\"576\" style=\"border:1px solid #000000;\">Sorry, you browser does not support canvas.</canvas>", "utf-8"))

            # self.wfile.write(bytes("<script>", "utf-8"))
            # with open("canvas_script.js", "rb") as f:
            #     self.wfile.write(f.read())
            #     # self.wfile.write(bytes("asdfghjkl", "utf-8"))
            # self.wfile.write(bytes("</script>", "utf-8"))

            # # display_interface = main.GameInstance.DisplayInterface()
            # # display_interface.draw_rect(100, 200, 300, 400, "green")
            # # self.wfile.write(bytes(display_interface.get_HTML_canvas(), "utf-8"))

            # # display game.lua
            # # self.wfile.write(bytes("<pre>", "utf-8"))
            # # with open("scripts/game.lua", "rb") as f:
            # #     self.wfile.write(f.read())
            # # self.wfile.write(bytes("</pre>", "utf-8"))

            # self.wfile.write(bytes("</body></html>", "utf-8"))

        elif self.path.startswith("/fetchdata?"):
            query = parse_qs(urlparse(self.path).query)

            # print(self.path)
            # print(query)
            # print()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(json.dumps([
                "testing", "todo"
            ]), "utf-8"))

        else:
            self.send_response(404)
            # self.send_header("Content-type", "text/html")
            self.end_headers()



if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
