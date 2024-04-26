from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>lua-api-learning</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>This is an example web server for a Lua API game.</h1>", "utf-8"))

        if self.path == "/":
            pass

        self.wfile.write(bytes("<canvas id=\"drawCanvas\" width=\"1024\" height=\"576\" style=\"border:1px solid #000000;\">Sorry, you browser dones not support canvas.</canvas>", "utf-8"))

        # display game.lua
        # self.wfile.write(bytes("<pre>", "utf-8"))
        # with open("scripts/game.lua", "rb") as f:
        #     self.wfile.write(f.read())
        # self.wfile.write(bytes("</pre>", "utf-8"))

        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")