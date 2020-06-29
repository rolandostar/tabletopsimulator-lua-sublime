import sublime
import sublime_plugin

import socket, sys, struct, time, json, os, re, io, glob
from os import walk

suffix = "\Lua"

class getscriptsCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        if(self.view.window().folders()):
            directory = self.view.window().folders()[0]+suffix
        else:
            directory = sublime.packages_path()+suffix
        settings = sublime.load_settings('TTSLuaPlugin.sublime-settings')
        if not os.path.exists(directory):
            os.makedirs(directory)
        if settings.get('open_as_project') == 1:
            self.view.window().run_command("open_folder_as_project", {"folder": directory})
        if sublime.ok_cancel_dialog("Get Lua Scripts from game?", "Yes"):
            # Create socket and connect to TTS server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', 39999))
                sock.sendall(b'{messageID: 0}')
            data = b''
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("localhost", 39998))
                sock.listen(0)
                conn, addr = sock.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        d = conn.recv(8192)
                        if d:
                            data += d
                        else:
                            break
            json_string  = (data.decode('utf-8')).replace("\r","")
            status  = json.loads(json_string)
            # TODO: Check message status
            for f in glob.glob(directory+"\*"):
                os.remove(f)
            for tts_object in status['scriptStates']:
                subs_tts_object_name = re.sub(r'[\/\\:*?"<>|]', "-", tts_object["name"])
                filename = "\\"+subs_tts_object_name+"."+tts_object["guid"]+".lua"
                with io.FileIO(directory+filename, "w") as file:
                    file.write(bytes(tts_object["script"],'utf-8'))
                if settings.get('open_as_project') == 0:
                    self.view.window().open_file(directory+filename)

                if "ui" in tts_object.keys():
                    filename = "\\"+subs_tts_object_name+"."+tts_object["guid"]+".xml"
                    with io.FileIO(directory+filename, "w") as file:
                        file.write(bytes(tts_object["ui"],'utf-8'))
                    if settings.get('open_as_project') == 0:
                        self.view.window().open_file(directory+filename)


class pushscriptsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().run_command('save_all')
        if(self.view.window().folders()):
            directory = self.view.window().folders()[0]+suffix
        else:
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
