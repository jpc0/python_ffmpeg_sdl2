FFMPEG subprocess python test
=============================

This is simply to test whether I can pass ram frame from ffmpeg in a subprocess
into python and then display it using pysdl2 in an efficient manner. The test
was a success.

To run this yourself you can simply put a video file named test.webm (in webm
format, sorry) in the folder and `python main.py`. You could also change the 
filename in the ffmpeg subprocess command if you so wish, this is a test, I
won't be getting it from an arg, sorry.

Executing
---------

Unixlike

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Windows

```pwsh
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
