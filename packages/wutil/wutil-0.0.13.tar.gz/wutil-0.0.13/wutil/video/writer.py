import av
import cv2
import numpy as np
from wutil import Size


class AvVideoWriter:
    '''
    PyAV videowriter based on sample https://pyav.org/docs/develop/cookbook/numpy.html#generating-video

    Encodes video with h264 codec, follows interface similar to OpenCV VideoWriter.
    '''

    def __init__(
        self,
        out_p: str,
        size: Size,
        fps: float
    ):
        self.container = av.open(out_p, mode='w')

        self.stream = self.container.add_stream('h264', rate=fps)
        self.stream.width = size.w
        self.stream.height = size.h
        self.stream.pix_fmt = 'yuv420p'
        self.stream.options = {'preset': 'fast'}
        self.container.streams.video[0].thread_type = 'AUTO'

    def write(self, img: np.ndarray):
        frame = av.VideoFrame.from_ndarray(img, format='bgr24')
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def release(self):
        # Flush stream
        for packet in self.stream.encode():
            self.container.mux(packet)

        # Close the file
        self.container.close()


def video_writer(out_p: str, fps: float, vid_width: int, vid_height: int) -> AvVideoWriter:
    return AvVideoWriter(out_p, Size(vid_width, vid_height), fps)


def video_writer_from_cap(cap: cv2.VideoCapture, out_p: str, round_fps=True) -> AvVideoWriter:
    fps = cap.get(cv2.CAP_PROP_FPS)
    if round_fps:
        fps = round(fps)

    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return video_writer(out_p, fps, vid_width, vid_height)
