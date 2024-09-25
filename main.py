import subprocess
import sdl2
import sdl2.ext
import ctypes
import queue
import threading
import numpy as np


def decode_video(queue: queue.Queue, event: threading.Event):
    p1 = subprocess.Popen(
        [
            "ffmpeg",
            "-hwaccel",
            "auto",
            "-i",
            "test.webm",
            "-filter:v",
            "scale=1280x720,fps=fps=60",
            "-pix_fmt",
            "rgb24",
            "-f",
            "rawvideo",
            "-",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    frame_size = 1280 * 720 * 3
    while not event.is_set():
        if p1.stdout is None:
            break
        frame = p1.stdout.read(frame_size)
        if len(frame) < frame_size:
            break
        arr = np.frombuffer(frame, dtype=np.uint8)
        queue.put(arr)
    p1.terminate()


def main():
    sdl2.ext.common.init()
    sdl2.ext.set_texture_scale_quality("best")
    sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)
    display_flags = sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_ALLOW_HIGHDPI
    renderer_flags = sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC

    window = sdl2.ext.Window("Test", (1280, 720), flags=display_flags)
    renderer = sdl2.ext.Renderer(window, flags=renderer_flags)
    sdl2.ext.renderer.set_texture_scale_quality("best")

    texture = sdl2.SDL_CreateTexture(
        renderer.sdlrenderer,
        sdl2.SDL_PIXELFORMAT_RGB24,
        sdl2.SDL_TEXTUREACCESS_STREAMING,
        1280,
        720,
    )

    q: queue.Queue[np.ndarray] = queue.Queue(32)
    e = threading.Event()
    t1 = threading.Thread(target=decode_video, args=[q, e])
    t1.start()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
        renderer.clear()
        try:
            uint8_array = q.get_nowait()
            sdl2.SDL_UpdateTexture(
                texture,
                None,
                ctypes.cast(uint8_array.ctypes.data, ctypes.POINTER(ctypes.c_uint8)),
                1280 * 3,
            )
            sdl2.SDL_RenderCopy(renderer.renderer, texture, None, None)
        except queue.Empty:
            pass
        renderer.present()

    e.set()
    while not q.empty():
        q.get()


if __name__ == "__main__":
    main()
