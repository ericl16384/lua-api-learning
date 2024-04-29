from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

import json
import multiprocessing
import time
import traceback

import lua_environment



url_filename_lookup = {
    "/": "webpages/index.html",
    "/upload_script": "webpages/upload_script.html",
}


host_name = "localhost"
server_port = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # if self.path == "/":
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html")
        #     self.end_headers()

        #     with open("index.html", "rb") as f:
        #         self.wfile.write(f.read())

        #     # self.wfile.write(bytes("<html><head><title>lua-api-learning</title></head>", "utf-8"))
        #     # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        #     # self.wfile.write(bytes("<body>", "utf-8"))
        #     # self.wfile.write(bytes("<h1>This is an example web server for a Lua API game.</h1>", "utf-8"))


        #     # self.wfile.write(bytes("<canvas id=\"drawCanvas\" width=\"1024\" height=\"576\" style=\"border:1px solid #000000;\">Sorry, you browser does not support canvas.</canvas>", "utf-8"))

        #     # self.wfile.write(bytes("<script>", "utf-8"))
        #     # with open("canvas_script.js", "rb") as f:
        #     #     self.wfile.write(f.read())
        #     #     # self.wfile.write(bytes("asdfghjkl", "utf-8"))
        #     # self.wfile.write(bytes("</script>", "utf-8"))

        #     # # display_interface = main.GameInstance.DisplayInterface()
        #     # # display_interface.draw_rect(100, 200, 300, 400, "green")
        #     # # self.wfile.write(bytes(display_interface.get_HTML_canvas(), "utf-8"))

        #     # # display game.lua
        #     # # self.wfile.write(bytes("<pre>", "utf-8"))
        #     # # with open("scripts/game.lua", "rb") as f:
        #     # #     self.wfile.write(f.read())
        #     # # self.wfile.write(bytes("</pre>", "utf-8"))

        #     # self.wfile.write(bytes("</body></html>", "utf-8"))

        if self.path.startswith("/fetchgameevents?"):
            query = parse_qs(urlparse(self.path).query)

            # print(self.path)
            # print(query)
            # print()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # display = lua_environment.GameInstance.DisplayInterface()
            # display.draw_rect(10, 20, 30, 40, "black")
            # display.draw_rect(20, 40, 60, 80, "yellow")
            # display.sleep(2)
            # display.draw_rect(30, 60, 90, 120, "red")

            # lua_environment.main()
            with open("scripts/history.json", "r") as f:
                events = json.loads(f.read())

            self.wfile.write(bytes(json.dumps(events), "utf-8"))


        elif self.path in url_filename_lookup:
            with open(url_filename_lookup[self.path], "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_response(404)


def main():
    try:
        p = multiprocessing.Process(target=lua_environment.main)
        start_time = time.time()
        p.start()
        p.join(5)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("elapsed_time", elapsed_time)
        if p.is_alive():
            p.terminate()
            # p.join()

    except:
        print(traceback.format_exc())

    web_server = HTTPServer((host_name, server_port), MyServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")

if __name__ == "__main__": main()
