#!/bin/python

import os
import sys
import getopt
import socket
import io
import qrcode
from flask import Flask, send_file, make_response, render_template, request
from dataclasses import dataclass

@dataclass
class Options:
    file:str
    port:int
    ip:str
    directory:str

DEFAULT_PORT = 8000
ARG_LOCATION_KEY = "loc"
APP = Flask(__name__)
program_options = Options("", DEFAULT_PORT, "", None)

def main(argv):
    # parse arguments
    try:
        opts, args = getopt.getopt(argv,"hf:p:d:")
    except getopt.GetoptError:
        help_options()
        sys.exit(1)

    for opt, arg in opts:
        if (opt == "-h"):
            help_options()
            exit()
        elif (opt == "-f"):
            try:
                program_options.file = os.path.realpath(str(arg))
                if (not os.path.exists(program_options.file) or not os.path.isfile(program_options.file)):
                    print("File doesn't exist")
                    exit()
            except ValueError: # error if user didn't pass path after -f flag
                print("-f flag should be followed by file path")
                sys.exit(1)
        elif (opt == "-d"):
            try:
                program_options.directory = os.path.realpath(str(arg))
                if (not os.path.exists(program_options.directory) or not os.path.isdir(program_options.directory)):
                    print("Directory doesn't exist")
                    exit()
            except ValueError: # error if user didn't pass directory after -d flag
                print("-d flag should be followed by directory path")
                sys.exit(1)
        elif (opt == "-p"):
            try:
                program_options.port = int(str(arg))
            except ValueError: # error if user didn't pass port after -p flag
                print("-p flag should be followed by port number (int)")
                sys.exit(1)
    
    program_options.ip = socket.gethostbyname(socket.gethostname()) # get an ip address
    if (program_options.file != "" or program_options.directory != None):
        server_url = f"http://{program_options.ip}:{program_options.port}"
        print(server_url) # print server url
        print(get_qrcode(server_url)) # print the qrcode of url

        # run web server
        APP.run(host=program_options.ip, port=program_options.port, debug=False, use_reloader=False)
    else: # print help menu if user didn't specify a file
        help_options()

def help_options():
    print("-h # print help menu")
    print("-f <file> # file to stream")
    print("-d <directory_with_video_files> # directory to stream from")
    print(f"-p <port> # port to stream on, default port is {DEFAULT_PORT}")
    print("you have to use -f or -d flag")

def get_qrcode(string):
    qr = qrcode.QRCode()
    qr.add_data(string)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()

@APP.route('/')
def root_path_in_web_server():
    if (program_options.directory != None): # if user specified directory instead of the file
        location = request.args.get(ARG_LOCATION_KEY, type = str)
        if (location == None): # if there is no specific directory or file to serve serve default directory
            return serve_directory(program_options.directory)
        else: # serve directory that has been chosen by url argument
            path = program_options.directory + location
            if (not os.path.exists(path)): # if file/directory doesn't exist return error page
                return render_template('file_not_found.html')

            if (os.path.isdir(path)): # if path is directory then return view of that directory
                return serve_directory(path, location)

            return serve_video(path) # if it exists and it's not directory than return it as video

    else: # if user specified one file serve him this one video
        return serve_video()

def serve_directory(path, link_path=""):
    files_dictionary = {}

    if (link_path != ""): # if there is previous location create a link to it so user can return back
        files_dictionary[get_one_directory_back(link_path)] = ".."

    for file in sorted(os.listdir(path)): # add all links and file names to the files dictionary 
        files_dictionary[link_path + "/" + file] = file
    
    return render_template('index.html', files=files_dictionary, arg_location_key = ARG_LOCATION_KEY)

def serve_video(vid_path=None):
    print(f"vid path: {vid_path}")
    if (vid_path == None):
        vid_path = os.path.expanduser(program_options.file) # use default file if none other path is provided
    
    print(f"vid path1: {vid_path}")
    resp = make_response(send_file(vid_path))
    resp.headers['Content-Disposition'] = 'inline'
    return resp

def get_one_directory_back(path:str):
    path = path if path[-1] != '/' else path[0:-2] # strip last slash at the end
    if ('/' not in path):
        return "/"
    
    return path[0:path.rindex('/')] # return everything from start of the path to the position of the last slash

if __name__ == '__main__':
    main(sys.argv[1:])
