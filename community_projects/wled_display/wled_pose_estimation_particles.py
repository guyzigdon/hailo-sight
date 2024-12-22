import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import sys
import numpy as np
import cv2
import hailo
sys.path.append('../../basic_pipelines')

from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    app_callback_class,
)
from hailo_apps_infra.pose_estimation_pipeline import GStreamerPoseEstimationApp

from wled_display import WLEDDisplay
from particle_simulation import ParticleSimulation


class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.wled = WLEDDisplay(panels=2, udp_enabled=True)
        self.frame_skip = 2
        self.particle_simulation = ParticleSimulation()

    def __del__(self):
        self.particle_simulation = None


def app_callback(pad, info, user_data):
    user_data.increment()
    if user_data.get_count() % user_data.frame_skip != 0:
        return Gst.PadProbeReturn.OK

    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    width = 40
    height = 20

    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    hand_positions = {}
    for detection in detections:
        if detection.get_label() != "person":
            continue
        track_id = detection.get_objects_typed(hailo.HAILO_UNIQUE_ID)[0].get_id()
        landmarks = detection.get_objects_typed(hailo.HAILO_LANDMARKS)[0].get_points()
        for i, wrist in enumerate(['left_wrist', 'right_wrist']):
            keypoint_index = {'left_wrist': 9, 'right_wrist': 10}[wrist]
            point = landmarks[keypoint_index]
            x = int(point.x() * width)
            y = int(point.y() * height)
            hand_positions[(track_id << 1) + i] = (x, y)

    user_data.particle_simulation.update_hand_positions(hand_positions)
    user_data.particle_simulation.update()

    frame = user_data.particle_simulation.get_frame(
        user_data.wled.panel_width * user_data.wled.panels, user_data.wled.panel_height
    )
    user_data.wled.frame_queue.put(frame)

    return Gst.PadProbeReturn.OK


if __name__ == "__main__":
    user_data = user_app_callback_class()
    app = GStreamerPoseEstimationApp(app_callback, user_data)
    app.run()