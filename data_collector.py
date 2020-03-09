import cv2
import os
#import imutils
#import numpy as np
import time


class Timer:
	def __init__(self, set_time_min: float):
		self.set_time = set_time_min*60
		self.stop_time = time.time() + self.set_time

	def done(self):
		return time.time() > self.stop_time

	def reset(self):
		self.stop_time = time.time() + self.set_time


class Camera:
	def __init__(self, src=0, fps=10.0, frame_width=640, frame_height=480):
		self.cam_object = cv2.VideoCapture(src)
		self.cam_object.set(3, frame_width)
		self.cam_object.set(4, frame_height)
		self.cam_object.set(5, fps)
		self.frames = []
		self.frame_size = (int(self.cam_object.get(3)), int(self.cam_object.get(4)))
		self.fps = self.cam_object.get(5)

	def stream(self, timer: Timer, display=False):
		print(f'\n\nCamera streaming {self.frame_size} frames @ {self.fps} fps for {timer.set_time} seconds')
		while timer.done() is False:
			ret, frame = self.cam_object.read()
			if ret:
				if display is True:
					cv2.imshow('camera display', frame)
					k = cv2.waitKey(1)
					if k == 27:  # Press ESC to exit
						break
				self.frames.append((frame, int(time.time())))
		self.cam_object.release()
		cv2.destroyAllWindows()


class Video:
	def __init__(self, path, camera: Camera=None):
		if camera is None and os.path.exists(path):
			self.load(path)
		else:
			str1 = time.strftime('%d-%b-%Y_%H-%M-%S_', time.localtime(camera.frames[0][1]))
			str2 = time.strftime('to_%H-%M-%S.avi', time.localtime(camera.frames[-1][1]))
			video_path = os.path.join(path, str1+str2)
			frames = [frame[0] for frame in camera.frames]
			self.write(video_path, frames, camera.fps, camera.frame_size)

	def label(self, video_path, frame_start, frame_end):
		label = None
		action = input('\n\n[1] sitting_up\n[2] standing\n[3] falling\n[4] still_on_bed\n[5] still_on_ground\n'
					   '[6] rolling_on_bed\n[7] rolling_on_ground\nlabel action:')
		if action == '1':
			label = 'sitting_up'
		elif action == '2':
			label = 'standing'
		elif action == '3':
			label = 'falling'
		elif action == '4':
			label = 'still_on_bed'
		elif action == '5':
			label = 'still_on_ground'
		elif action == '6':
			label = 'rolling_on_bed'
		elif action == '7':
			label = 'rolling_on_ground'
		labeled_video_path = video_path[:-len('.avi')]+f'_{frame_start}_to_{frame_end}_{label}.avi'
		cap_object = cv2.VideoCapture(video_path)
		frames = []
		for i in range(frame_start, frame_end+1):
			cap_object.set(1,i)
			ret, frame = cap_object.read()
			if ret:
				frames.append(frame)
		self.write(labeled_video_path, frames, cap_object.get(5), (int(cap_object.get(3)), int(cap_object.get(4))))

	def write(self, video_path, frames, fps, frame_size):
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(video_path, fourcc, fps, frame_size)
		for frame in frames:
			writer.write(frame)
		writer.release()
		print(f'\n\nVideo saved as {video_path}')

	def load(self, path):
		video_paths = None
		if os.path.isdir(path):
			video_paths = [os.path.join(path,f) for f in os.listdir(path) if (f.endswith('.avi') and not f.startswith('._'))]
		elif os.path.isfile(path):
			video_paths = [path]
		else:
			raise FileNotFoundError(f'{path} is neither a file nor a directory')
		video_i = 0
		frame_i = 0
		action_start, action_end = (None, None)
		print('\n[s] next video\n[w] previous video\n[d] >\n[a] <\n[c] >>\n[z] <<\n[0] action start\n[1] action end')
		while video_i < len(video_paths):
			cap_object = cv2.VideoCapture(video_paths[video_i])
			frame_count = int(cap_object.get(7))
			cap_object.set(1, frame_i)
			ret, frame = cap_object.read()
			if ret:
				cv2.imshow('window_title', frame)
			k = cv2.waitKey()  # wait for key press, no delay
			if k == ord('d'):  # next frame
				if frame_i+1 < frame_count:
					frame_i += 1
				else:
					print('end of video')
			elif k == ord('a'):  # prev frame
				if frame_i-1 >= 0:
					frame_i -= 1
				else:
					print('start of video')
			elif k == ord('w'):  # prev video
				if video_i-1 >= 0:
					video_i -= 1
				else:
					print('first video')
			elif k == ord('s'):  # next video
				if video_i+1 < len(video_paths):
					video_i += 1
				else:
					print('last video')
			elif k == ord('c'):  # fast forward
				if frame_i+10 < frame_count:
					frame_i += 10
				elif frame_i+5 < frame_count:
					frame_i += 5
			elif k == ord('z'):  # fast backward
				if frame_i-10 >= 0:
					frame_i -= 10
				elif frame_i-5 >= 0:
					frame_i -= 5
			elif k == ord('0'):  # start frame
				action_start = frame_i
				print(f'action started at frame {frame_i+1}/{frame_count}')
			elif k == ord('1'):
				if action_end == None:
					action_end = frame_i
					print(f'action ended at frame {frame_i + 1}/{frame_count}')
			elif k == 27:  # ESC to exit
				cv2.destroyAllWindows()
				break
			if (action_start is not None) and (action_end is not None):  # Labeled
				self.label(video_paths[video_i], action_start, action_end)
				print('\n[s] next video\n[w] previous video\n[d] >\n[a] <\n[c] >>\n[z] <<\n[0] action start\n'
					  '[1] action end')
				action_start, action_end = (None, None)


def view_data():
	path = os.path.join(os.getcwd(), 'data_collector_videos')
	video_writer = Video(path)

def collect_data(collections, collection_time, delay):
	path = os.path.join(os.getcwd(), 'data_collector_videos')
	if not os.path.exists(path):
		os.mkdir(path)
	timer = Timer(set_time_min=collection_time)
	for i in range(collections):
		cam = Camera(src=0, fps=10.0, frame_width=640, frame_height=480)
		cam.stream(timer, display=True)
		video_writer = Video(path, cam)
		t_start = time.time()
		print(f'next collection in {delay*60} seconds...\n')
		while(time.time() < t_start+(delay*60)):
			pass
		timer.reset()


if __name__ == '__main__':
	collect_data(collections=7, collection_time=0.25, delay=0.5)
	view_data()

