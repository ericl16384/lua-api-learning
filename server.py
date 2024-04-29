from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

import json
import multiprocessing
import os
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
        query = parse_qs(urlparse(self.path).query)

        if self.path.startswith("/fetch_game_events?"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("scripts/history.json", "r") as f:
                events = json.loads(f.read())

            self.wfile.write(bytes(json.dumps(events), "utf-8"))

        # elif self.path.startswith("/review_script?"):
        #     print(query)


        elif self.path in url_filename_lookup:
            with open(url_filename_lookup[self.path], "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_response(404)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # Parse the form data
        # params = parse_qs(post_data.decode("utf-8"))

        lines = post_data.decode("utf-8").split("\r\n")

        sections = []
        i = 0
        while i < len(lines):
            if lines[i].startswith("------WebKitFormBoundary"):
                sections.append(lines[i:i+4])
                sections.append([])
                i += 4
                continue
            else:
                sections[-1].append(lines[i])
                i += 1

        file_content = "\n".join(sections[1])
        # print(json.dumps(sections, indent=2))

        # with open("asdf.log", "w") as f:
        #     f.write(json.dumps(post_data.decode("utf-8").split("\r\n"), indent=2))

        # content = "".join(content).split("\n")

        # Print the form data
        # print("Submitted Form Data:")
        with open("asdf.json", "w") as f:
            f.write(json.dumps(sections, indent=2))
        # with open("asdf.lua", "w") as f:
        #     f.write("\n".join(sections[1]))
        # filename = content[0].split(";")[1].split("=")[1][1:-1]

        # input()

        script_type = sections[2][3]

        form_content = sections[0][1].split("; ")[1:]
        form_data = {}
        for data in form_content:
            if i == 0:
                continue

            k, v = data.split("=")
            v = v[1:-1]
            form_data[k] = v
        # print(form_data)
        filename = form_data["filename"]

        script_hash = lua_environment.basic_hash(file_content)
        savename = "scripts/" + script_hash
        with open(savename + ".json", "w") as f:
            f.write(json.dumps({
                "filename": filename,
                "script_type": script_type,
                "time": time.time(),
                "script_hash": script_hash,
                "user": 0,
            }))
        with open(savename + ".lua", "w") as f:
            f.write(file_content)



        # print("filename", filename)


        # for key, value in params.items():
        #     # print(key)
        #     # print()
        #     # print(value)
        #     # print()
        #     # print()
        #     # print()
        #     # # input()
        #     print(json.dumps((key, value), indent=2))
        # print()

        # Send response back to the client
        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Thank you for submitting the form!")


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
