from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

import ctypes
import json
import multiprocessing
import os
import time
import threading
import traceback
import queue

import lupa

import lua_environment



# url_filename_lookup = {
#     "/": "webpages/index.html",
#     # "/upload_script": "webpages/upload_script.html",
#     # "/watch_replay": "webpages/watch_replay.html",
#     # # "/webpages/replayTable.js": "webpages/replayTable.js"
# }



# run_script_queue = queue.Queue()




class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        urlparse_path = urlparse(self.path)
        path = urlparse_path.path
        query = parse_qs(urlparse_path.query)

        assert path[0] == "/"

        if False:
            pass

        elif path == "/fetch_replay_events":
            replay_id = query.get("id")
            filename = f"replays/{replay_id[0]}.json"
            if replay_id and os.path.isfile(filename):
                with open(filename, "r") as f:
                    events = json.loads(f.read())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(json.dumps(events), "utf-8"))
            else:
                self.send_response(404)

        elif path == "/fetch_replay_table":
            lines = []
            try:
                with open("replays/__index__.log", "r") as f:
                    lines = f.readlines()
            except:
                pass

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

            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(out), "utf-8"))

            # self.wfile.(bytes(json.dumps(replays), "utf-8"))
        
        elif path == "/fetch_script":
            out = self.get_script(query.get("id")[0])

            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(out), "utf-8"))

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
            assert ".." not in path

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

        elif path == "/run_script": # will be POST
            game = query.get("game")[0]
            players = query.get("player")
            assert len(players) == 1

            # print("sleeping")
            # time.sleep(10)
            # print("finished sleeping", urlparse_path.query)
            self.handle_run_script(game, players)

        else:
            self.send_response(404)

    def do_POST(self):
        urlparse_path = urlparse(self.path)
        path = urlparse_path.path
        query = parse_qs(urlparse_path.query)

        if path == "/post_script":
            self.handle_upload_script()

        else:
            self.send_response(404)
    
    def get_script(self, id):
        directory = "scripts/" + id + "/"
        if not os.path.isdir(directory):
            return None
        
        with open(directory + "info.json", "r") as f:
            info = json.loads(f.read())
        with open(directory + "script.lua", "r") as f:
            script = f.read()

        return {
            "info": info,
            "script": script
        }
        # else:
        #     return False

    def handle_upload_script(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

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

        script_hash = self.save_script(file_content, filename, script_type)


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            f"<meta http-equiv=\"refresh\" content=\"0; URL=view_script.html?id={script_hash}\" />",
        "utf-8"))

        # Send response back to the client
        # self.wfile.write(b"Thank you for submitting the form!")
        # self.wfile.write(bytes(file_content, "utf-8"))
    
    def handle_run_script(self, game, players):
        # I'll need to figure out an async way to do this :)
        # run_script_queue.put((game, players))

        # try:
        success, result = self.generate_game_replay(game, players)
        # except:
        #     # print(traceback.format_exc())
        #     self.send_response(400)
        #     self.wfile.write(bytes(traceback.format_exc(), "utf-8"))
        #     return
        
        if success:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(
                f"<meta http-equiv=\"refresh\" content=\"0; URL=watch_replay.html?id={result}\" />",
            "utf-8"))
        else:
            self.send_response(400)
            # self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(str(result), "utf-8"))
    
    def save_script(self, file_content, filename, script_type):
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
        
        return script_hash
    
    def generate_game_replay(self, game_id, player_ids):
        """returns (success, result)"""

        assert len(player_ids) == 1

        game_script = self.get_script(game_id)["script"]
        player_script = self.get_script(player_ids[0])["script"]

        timeout_length = 3

        # out = multiprocessing.Manager().Value(ctypes.c, "")
        # print(out.value)
        connection_receiver, connection_sender = multiprocessing.Pipe()
        p = multiprocessing.Process(target=lua_environment.run_new_game_process, args=(
            connection_sender,
            game_script, player_script
        ))
        # start_time = time.time()
        p.start()
        p.join(timeout_length)
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print("elapsed_time", elapsed_time)
        if p.is_alive():
            p.terminate()
            return False, TimeoutError(timeout_length)
        success, result = connection_receiver.recv()
        return success, result
            # p.join()
        # print(out.value)
        # return out.value





def run_server(host_name, server_port):
    web_server = HTTPServer((host_name, server_port), RequestHandler)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")


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

    # server_process = multiprocessing.Process(target=run_server)
    # server_process.start()
    server_thread = threading.Thread(target=run_server, args=("localhost", 80))
    server_thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__": main()
