from typing import Iterable, Optional

import cv2

from .common import Frame, FrameGroup


def flat_frames(wrapped_cap) -> Iterable[Frame]:
    for frame_group in wrapped_cap:
        for frame in frame_group.frames:
            yield frame


def cap_wrapper(cap, detector_fps=-1):
    cap_fps = cap.get(cv2.CAP_PROP_FPS)

    target_time_between_frames = 0
    if detector_fps != -1:
        target_time_between_frames = 1 / detector_fps

    prev_frame_time = None

    frame_group = []
    while True:
        ret, image = cap.read()

        if not ret:
            return

        fr_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        fr_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        frame_group.append(Frame(image, fr_idx, fr_time))

        if prev_frame_time is not None and fr_time - prev_frame_time < target_time_between_frames:
            continue

        prev_frame_time = fr_time
        yield FrameGroup(frame_group)
        frame_group = []


def open_video(vid_p: str,
               start_msec: Optional[float] = None,
               end_msec: Optional[float] = None) -> Iterable[Frame]:
    cap = cv2.VideoCapture(vid_p)

    if start_msec:
        cap.set(cv2.CAP_PROP_POS_MSEC, start_msec - 1)

    for frame in flat_frames(cap_wrapper(cap)):
        if end_msec and frame.time * 1000 >= end_msec:
            cap.release()
            return

        yield frame

    cap.release()
