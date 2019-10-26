import cv2
import numpy as np
import imutils
import os
import imageio

threshold = 7 #How many extra frames should result in a new video?
manual = False #flag to count manually
preview = False#flag to preview manually generated video

# 108 images 9/7 Nael's Room
DIM=(640, 480)
K=np.array([[240.21086643847192, 0.0, 318.0152843306422], [0.0, 240.66145029587912, 220.42879674202533], [0.0, 0.0, 1.0]])
D=np.array([[-0.03561582686662651], [-0.011557711209240214], [0.004239894818130242], [-0.0011662345578036493]])

def undistort(img):
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

def resize(img): #Transforms Frame to Model Specifications (256x256)
    #img = undistort_1(img) #Takes too long
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)] #256x256 center crop (8/9/2019)
    return img

def count_frames(cap): #manual frame count
    frameCount_cap = int(cap.get(7))
    frameCount = 0
    otherCount = 0
    prev_frames = []
    print('counting frames manually..')
    for i in range(frameCount_cap):
        ret, frame = cap.read()
        if ret:
            if otherCount > 3:
                prev_frames.append(frame)
                frameCount += 1
            otherCount += 1
        else:
            otherCount += 1
    print(otherCount,' iterations')
    print('manual frame count: ',frameCount)
    if preview:
        counting = 0
        for frame in prev_frames:
            cv2.imshow(str(counting),frame)
            cv2.waitKey(1000)
            counting += 1
        cv2.destroyAllWindows()
    return frameCount
        
    
def split_video(rootdir):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") #video codec (use MJPG for Linux), 'MP4V' for mp4 files?
    frame_rate = 10
    frames_per_video = 30
    files = os.listdir(rootdir)
    split_dir = os.path.join(rootdir,os.path.basename(rootdir)+'_split')
    if not os.path.exists(split_dir):
        os.mkdir(split_dir)

    fileCount = 0
    while fileCount < len(files):
        f = files[fileCount]
        if f.startswith('._'):
            fileCount += 1
            continue
        if f.endswith('.avi') or f.endswith('.mp4'):
            cap = cv2.VideoCapture(os.path.join(rootdir,f))
            if not cap.isOpened(): #check if file is valid video file
                fileCount += 1
                print("Couldn't read {}".format(f))
                continue
            frame_size = (int(cap.get(3)),int(cap.get(4)))  #get frame size as tuple
            total_frames = int(cap.get(7))  #get frame count from video object
            if manual:                      #get frame count manually
                total_frames = count_frames(cap)
            
            if total_frames<frames_per_video:
                fileCount+=1
                continue #disregard if video is too short

            r = total_frames%frames_per_video
            initial_frames = list(range(0,total_frames+1,30))
            initial_frames = initial_frames[:-1]
            if r >= threshold:
                initial_frames.append(total_frames-30)
            videos = len(initial_frames)
            print('current file:', f)
            print('total frames: ',total_frames,'\nframe rate:',int(cap.get(5)))
            print('splitting {} into {} videos ...'.format(f,videos))
            
            video = 0
            for j in initial_frames:
                videowriter = cv2.VideoWriter(os.path.join(split_dir,str(video+1)+'-'+f),fourcc,frame_rate,frame_size)
                for k in range(frames_per_video):
                    cap.set(1,j+k)
                    ret, frame = cap.read()
                    if ret:
                        #frame = undistort(frame)
                        #frame = resize(frame)
                        videowriter.write(frame)
                videowriter.release()
                video += 1
        fileCount += 1


if __name__ == '__main__':
    dir_name = input('Directory to split from:')
    dir_path = os.path.join(os.getcwd(),dir_name) 
    split_video(dir_path)
