import cv2
import uuid
import os
import imageio
import imutils
import numpy as np
import time
from multiprocessing.dummy import Pool
from multiprocessing.dummy import Event 

"""
Mercury Health - Real Data Collection Script
Author: Ricky Rueda
Updated: 09/011/2019
"""

frame_rate = 10.0 #as float
DIM=(640, 480) #Capture resolution for fisheye camera
# 108 images 9/7 Nael's Room
K=np.array([[240.21086643847192, 0.0, 318.0152843306422], [0.0, 240.66145029587912, 220.42879674202533], [0.0, 0.0, 1.0]])
D=np.array([[-0.03561582686662651], [-0.011557711209240214], [0.004239894818130242], [-0.0011662345578036493]])

def undistort_1(img, balance=0.99, dim2=(1920,1080), dim3=(1920,1080)):
    dim1 = (img.shape[1],img.shape[0])  	#dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1] #Image to undistort needs to have same aspect ratio as the ones used in calibratio
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0] 		# The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  					# Except that K[2][2] is always 1.0
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

def undistort(img):
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

def resize(img): #Transforms Frame to Model Specifications (256x256)
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)] #256x256 center crop (8/9/2019)
    return img

def test_fps(cam_num, delay): #Sets delay to adjust fps
    delay = float(delay)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter('test.avi', fourcc, frame_rate,(256,256))
    cap = cv2.VideoCapture(int(cam_num))
    cap.set(3,640)
    cap.set(4,480)
    cap.set(5,frame_rate)
    sum_fps = []
    i = 0
    n = 0
    try:
        while (cap.isOpened()):
            start = time.time()
            ret, frame = cap.read()
            if ret:
                #frame = undistort(frame)
                frame = resize(frame)
                i+= 1
                writer.write(frame)
                time.sleep(delay)
                if i == 30:
                    n+=1
                    print('n = ',n)
                    i = 0
            else:
                print('Camera failed to initialize\n')
                break
            sum_fps.append(1/(time.time()-start))
    except KeyboardInterrupt:
        avg_fps= sum(sum_fps[1:])/len(sum_fps[1:]) #exclude first frame usually takes long because of light adjustment
        print('avg fps: ',avg_fps)
        writer.release()

def preview(cam_num): #Previews Camera for Set Up
    cap = cv2.VideoCapture(int(cam_num))
    #cap.set(3,640)
    #cap.set(4,480)
    cap.set(5,frame_rate)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            #frame = undistort(frame)
            frame = resize(frame)
            cv2.imshow('Camera '+str(cam_num)+'@'+str(cap.get(5))+' fps',frame)
            k =cv2.waitKey(5)
            if k%256 == 27:
                cap.release()
                break
        else:
            print('Camera failed to initialize\n')
            break
    cv2.destroyAllWindows()

def capture_init(cam_nums): #Initializes Capture Objects
    caps =[]
    for i in range(len(cam_nums)):
        cam = int(cam_nums[i])
        cap = cv2.VideoCapture(cam)
        #cap.set(3,640)
        #cap.set(4,480)
        cap.set(5,frame_rate)
        caps.append(cap)
    for i in range(len(caps)):
        print('checking Camera '+str(i)+'...')
        if caps[i].isOpened():
            print('    Camera '+str(i)+' initialized succesfully')
        else:
            print('    Camera '+str(i)+' failed')
    return caps


def set_writer(action, cam_nums): #Creates Video Objects & File Paths
    action = int(action)
    root_dir = os.getcwd()
    action_names = ['Falling','Sitting_up','Standing', 'Still_On_Bed','Still_On_Ground', 'Rolling_Bed', 'Rolling_Ground']
    action_dir = os.path.join(root_dir, action_names[action-1])
    if not os.path.exists(action_dir):
        os.mkdir(action_dir)

    write_file = os.path.join(action_dir, str(uuid.uuid1()))
    writers = []
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    for i in range(len(cam_nums)):
        writer = cv2.VideoWriter(write_file+'cam'+str(i+1)+'.avi', fourcc, frame_rate, (256,256))
        writers.append(writer)
    return writers

def capture(cap_obj): #Edit for multiprocessing
    i = 0
    n = 0
    print('GO')
    while cap_obj.event.is_set():
        start = time.time()
        ret, frame = cap_obj.cap.read()
        if ret:
            #frame = undistort(frame)
            frame = resize(frame)
            cap_obj.writer.write(frame)
            #time.sleep(0.102)###
            i += 1
            if i == 30:
                n += 1
                print('n'+str(cap_obj.cam_num)+' = ',n)
                i = 0
        if not ret:
            print('Cam '+str(cap_obj.cam_num)+': False')


def multi_thread(cam_nums, func, args):
    event = Event()
    try:
        event.set()
        pool = Pool(len(cam_nums))
        for arg in args: arg.event = event
        results = pool.map(func, args)
    except KeyboardInterrupt:
        event.clear()
    finally:
        pool.close()
        pool.join()
        print('DONE')

class CaptureObj:
    def __init__(self, cap, writer, cam_num, event=None):
        self.cap = cap
        self.writer = writer
        self.cam_num = cam_num
        self.event = event


def main():
	while(True):
		inp = input('\n[d] Collect Data\n[p] Preview Camera\n[f] Test FPS\n[q] Quit\n:')
		if inp == 'q': 
			break
		if inp =='f':
			while(True):
				inp2 = input('\nCamera to Test: ')
				if inp2 == 'q':
					break
				delay = input('Delay: ')
				test_fps(inp2,delay)
		if inp == 'p':
			while(True):
				inp2 = input('\nCamera to Preview: ')
				if inp2 == 'q':
					break
				preview(inp2)
		if inp == 'd':
			inp2 = input('Set Camera Numbers (separate with space): ')
			cam_nums= inp2.split()
			caps = capture_init(cam_nums)
			while True:
				action = input('[1] falling  \n[2] sitting up\n[3] standing \n[4] still on bed \n[5] still on ground \n[6] rolling bed\n[7] rolling ground  \n[q] quit\n:')
				if action == 'q':
					break
				writers = set_writer(action,cam_nums)
				cap_objs = [CaptureObj(c,w,n) for c,w,n in zip(caps,writers,cam_nums)]
				multi_thread(cam_nums, capture, cap_objs)
				for i in range(len(caps)):
					writers[i].release

			for i in range(len(caps)):
				caps[i].release()


if __name__ == '__main__':
    main()
