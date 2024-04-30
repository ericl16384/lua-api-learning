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
    # "/upload_script": "webpages/upload_script.html",
    # "/watch_replay": "webpages/watch_replay.html",
    # # "/webpages/replayTable.js": "webpages/replayTable.js"
}

def handle_upload_script(request_handler):
    content_length = int(request_handler.headers["Content-Length"])
    post_data = request_handler.rfile.read(content_length)

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

    # print(json.dumps(lines, indent=2))
    # print(json.dumps(sections, indent=2))

    file_content = "\n".join(sections[1])

    # with open("asdf.log", "w") as f:
    #     f.write(json.dumps(post_data.decode("utf-8").split("\r\n"), indent=2))

    # content = "".join(content).split("\n")

    # Print the form data
    # print("Submitted Form Data:")
    # with open("asdf.json", "w") as f:
    #     f.write(json.dumps(sections, indent=2))
    # with open("asdf.lua", "w") as f:
    #     f.write("\n".join(sections[1]))
    # filename = content[0].split(";")[1].split("=")[1][1:-1]

    # input()

    script_type = sections[2][3]

    assert script_type in ("game", "player"), ("script_type", script_type)

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
    savedir = "scripts/" + script_hash + "/"
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    with open(savedir + "info.json", "w") as f:
        f.write(json.dumps({
            "filename": filename,
            "script_type": script_type,
            "save_time": time.time(),
            "script_hash": script_hash,
            "user": 0,
        }))
    with open(savedir + "script.lua", "w") as f:
        f.write(file_content)


    # request_handler.send_response(200)
    request_handler.send_response(307)
    # request_handler.send_header("Content-type", "text/html")
    request_handler.send_header("Location", "/view_script?id=" + script_hash)
    request_handler.end_headers()

    # Send response back to the client
    # request_handler.wfile.write(b"Thank you for submitting the form!")
    # request_handler.wfile.write(bytes(file_content, "utf-8"))


host_name = "localhost"
server_port = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        urlparse_path = urlparse(self.path)
        path = urlparse_path.path
        query = parse_qs(urlparse_path.query)

        assert path[0] == "/"

        if False:
            pass

        elif path == "/fetch_replay_events":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            replay_id = query.get("id")
            if replay_id:
                with open(f"replays/{replay_id[0]}.json", "r") as f:
                    events = json.loads(f.read())
            else:
                events = None

            # print(events)

            self.wfile.write(bytes(json.dumps(events), "utf-8"))

        elif path == "/fetch_replay_table":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            lines = []
            with open("replays/__index__.log", "r") as f:
                lines = f.readlines()

            lines = [json.loads(i) for i in lines]

            count = query.get("count")[0]
            if count.isdigit():
                count = int(count)
            else:
                count = 2*16

            if count >= len(lines):
                out = lines
            else:
                out = lines[-count:]

            out = list(reversed(out))

            # print(json.dumps(out, indent=2))

            self.wfile.write(bytes(json.dumps(out), "utf-8"))

            # self.wfile.(bytes(json.dumps(replays), "utf-8"))

        # elif self.path.startswith("/review_script?"):
        #     print(query)

        # elif self.path.startswith("/watch_replay?")



        # elif path in url_filename_lookup:
        #     with open(url_filename_lookup[path], "rb") as f:
        #         content = f.read()
        #     self.send_response(200)
        #     self.send_header("Content-type", "text/html")
        #     self.end_headers()
        #     self.wfile.write(content)


        elif os.path.isfile("web" + path):
            with open("web" + path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        if path[-1] == "/":
            self.send_response(302)
            self.send_header("Location", path + "index.html")
            self.end_headers()

        else:
            self.send_response(404)

    def do_POST(self):
        urlparse_path = urlparse(self.path)
        path = urlparse_path.path
        query = parse_qs(urlparse_path.query)

        if path == "/upload_script":
            handle_upload_script(self)

        else:
            self.send_response(404)




def main():
    # try:
    #     p = multiprocessing.Process(target=lua_environment.main)
    #     start_time = time.time()
    #     p.start()
    #     p.join(5)
    #     end_time = time.time()
    #     elapsed_time = end_time - start_time
    #     print("elapsed_time", elapsed_time)
    #     if p.is_alive():
    #         p.terminate()
    #         # p.join()

    # except:
    #     print(traceback.format_exc())

    web_server = HTTPServer((host_name, server_port), MyServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")

if __name__ == "__main__": main()
