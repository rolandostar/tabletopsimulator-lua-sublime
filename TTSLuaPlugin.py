import sublime
import sublime_plugin

import socket, sys, struct, time, json, os, re, io, glob
from os import walk

suffix = "\Lua"

class getscriptsCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        directory = sublime.packages_path()+suffix
        settings = sublime.load_settings('TTSLuaPlugin.sublime-settings')
        if not os.path.exists(directory):
            os.makedirs(directory)
        if settings.get('open_all_files') == 0:
            self.view.window().run_command("open_folder_as_project", {"folder": directory})
        def recv_timeout(the_socket,timeout=2):
            the_socket.setblocking(0)
            total_data=[];data='';
            begin=time.time()
            while 1:
                if total_data and time.time()-begin > timeout:
                    break
                elif time.time()-begin > timeout*2:
                    break
                try:
                    data = the_socket.recv(8192)
                    if data:
                        total_data.append(data)
                        begin = time.time()
                    else:
                        time.sleep(0.1)
                except:
                    pass
            return b''.join(total_data)
        if sublime.ok_cancel_dialog("Get Lua Scripts from game?", "Yes"):
            # Create socket and connect to TTS server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 39999))
            try:
                sock.sendall('{"messageID": 0}'.encode('utf-8'))
                # Look for the response
                raw_response = recv_timeout(sock)
                json_string  = (raw_response.decode('utf-8')).replace("\r","")
                status  = json.loads(json_string)
                # TODO: Check message status

                # remove cache files
                for f in glob.glob(directory+"\*"):
                    os.remove(f)

                # for each list member create a file
                for tts_object in status['scriptStates']:
                    filename = "\\"+tts_object["name"]+"."+tts_object["guid"]+".lua"
                    with io.FileIO(directory+filename, "w") as file:
                        file.write(bytes(tts_object["script"],'utf-8'))
                    if settings.get('open_all_files') == 1:
                        self.view.window().open_file(directory+filename)
            finally:
                sock.close()

class pushscriptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        directory = sublime.packages_path()+suffix
        f = []
        for (dirpath, dirnames, filenames) in walk(directory):
            f.extend(filenames)
            break
        status = {"messageID":1,"scriptStates":[]}
        for value in f:
            pattern = re.compile(r'(.*)\.(.*)\.lua', re.IGNORECASE)
            match = pattern.findall(value)
            file = open(directory+"\\"+value, 'rb')
            status['scriptStates'].append({"name":match[0][0],"guid":match[0][1],"script":file.read().decode('utf-8')})
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 39999))
        raw_message = json.dumps(status)
        try:
            sock.send(raw_message.encode('utf-8'))
            sublime.status_message("TTS Scripts Sent")
        finally:
            sock.close()
