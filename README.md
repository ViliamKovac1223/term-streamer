# Term_streamer
Do you want to stream your videos from your computer to your phone without leaving your comfy terminal ?
Yes, so this project is just for you. Term_streamer allows you to stream videos from your terminal to your phone or another
computer or just about anything that supports modern web browser such as firefox or chromium.
Term_streamer create flask server which can stream video to multiple devices at the same time.

After you run the program it will show you url to the site with video and
also it will show you qrcode of that url.

# Usage
Basic usage of term_streamer

```bash
./term_streamer.py -f /path/to/the/video.mp4
```

# All command options
-h # print help menu

-f <file> # file to stream, this option is MANDATORY

-p <port> # port to stream on, default port is 8000

# Installation

## Install dependencies
```bash
sudo pip install -r requirements.txt
```

## Install program
Simply add this folder to your $PATH variable.
