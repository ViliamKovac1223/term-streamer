#!/bin/python

import os
import sys
import getopt
import socket
import io
import qrcode
from flask import Flask, send_file, make_response
from dataclasses import dataclass

@dataclass
class Options:
    file:str
    port:int
    ip:str

DEFAULT_PORT=8000
APP = Flask(__name__)
program_options = Options("", DEFAULT_PORT, "")

def main(argv):
    # parse arguments
    try:
        opts, args = getopt.getopt(argv,"hf:p:")
    except getopt.GetoptError:
        help_options()
        sys.exit(1)

    for opt, arg in opts:
        if (opt == "-h"):
            help_options()
            exit()
        elif (opt == "-f"):
            try:
                program_options.file = str(arg)
            except ValueError: # error if user didn't pass path after -f flag
                print("-f flag should be followed by file path")
                sys.exit(1)
        elif (opt == "-p"):
            try:
                program_options.port = int(str(arg))
            except ValueError: # error if user didn't pass port after -p flag
                print("-p flag should be followed by port number (int)")
                sys.exit(1)
    
    program_options.ip = socket.gethostbyname(socket.gethostname()) # get an ip address
    if (program_options.file != ""):
        server_url = f"http://{program_options.ip}:{program_options.port}"
        print(server_url) # print server url
        print(get_qrcode(server_url)) # print the qrcode of url

        # run web server
        APP.run(host=program_options.ip, port=program_options.port, debug=False, use_reloader=False)
    else: # print help menu if user didn't specify a file
        help_options()

def help_options():
    print("-h # print help menu")
    print("-f <file> # file to stream, this option is MANDATORY")
    print(f"-p <port> # port to stream on, default port is {DEFAULT_PORT}")

def get_qrcode(string):
    qr = qrcode.QRCode()
    qr.add_data(string)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()

@APP.route('/')
def serve_video():
    vid_path = os.path.expanduser(program_options.file)
    resp = make_response(send_file(vid_path))
    resp.headers['Content-Disposition'] = 'inline'
    return resp

if __name__ == '__main__':
    main(sys.argv[1:])
