from djitellopy import Tello
import cv2
from datetime import datetime
import threading
import time

class TelloDrone(Tello):
  video_args = [cv2.VideoWriter_fourcc(*'H264'), 30.0, (1280, 720)]
  video_output = None
  video_thread = None
  is_recording = False

  def __init__(self):
    Tello.__init__(self)
    self.connect()
    self.streamon()
  
  def get_timestamp(self):
    return datetime.now().strftime("%m-%d-%Y-%H%M%S")

  def take_photo(self):
    timestamp = self.get_timestamp()
    print("saving photo")
    cv2.imwrite(f"{timestamp}.png", self.get_frame_read().frame)

  def _take_video(self):
    while self.is_recording:
      self.video_output.write(self.get_frame_read().frame)
      
      # Fix video to 30 fps
      time.sleep(1/30)

  def start_recording(self):
    timestamp = self.get_timestamp()
    height, width, _ = self.get_frame_read().frame.shape
    self.video_output = cv2.VideoWriter(f'{timestamp}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
    self.is_recording = True
    self.video_thread = threading.Thread(target=self._take_video)

    self.video_thread.start()
  
  def stop_recording(self):
    self.is_recording = False
    if self.video_thread:
      self.video_thread.join()
    self.video_output.release()
    self.streamoff()

  def up(self, dist: int):
    self.move_up(dist)
  
  def down(self, dist: int):
    self.move_down(dist)
  
  def left(self, dist: int):
    self.move_left(dist)
  
  def right(self, dist: int):
    self.move_right(dist)
  
  def forward(self, dist: int):
    self.move_forward(dist)

  def back(self, dist: int):
    self.move_back(dist)
  
  def cw(self, degrees: int):
    self.rotate_clockwise(degrees)
  
  def ccw(self, degrees: int):
    self.rotate_counter_clockwise(degrees)
  
  def get_tof(self) -> int:
    return self.get_distance_tof()

  def __del__(self):
    pass
