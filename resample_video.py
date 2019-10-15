import cv2 
import math
import numpy as np
import os
import imageio
import imutils

def resize(img):
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)]
    return img

def main(root_dir):
    fps = 30                #Target FPS
    frames_per_video = 30   #Target Frames
    files = os.listdir(root_dir)
    fps30_dir = os.path.join(root_dir, 'resampled')
    if not os.path.exists(fps30_dir):
        os.mkdir(fps30_dir)
        
    i = 0
    while i < len(files):
        
        f = files[i]
        if '._' in f:
            i += 1
            continue
        if '.avi' or '.mp4' in f:
            cap = cv2.VideoCapture(f)
            if not cap.isOpened(): 
                i += 1
                continue

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps_old = int(cap.get(cv2.CAP_PROP_FPS))
            total_videos = math.ceil(total_frames/frames_per_video)

            print('Converting ', f,"\n from ",fps_old," fps to ",fps," fps." )
            print('Splitting into %s videos...'%str(total_videos))

            video = 0
            currentFrame = 0
            videowriter = imageio.get_writer(os.path.join(fps30_dir,str(video+1)+'-'+f), fps=fps)

            while(video < total_videos):
                ret, frame = cap.read()
                if ret:
                    frame = resize(frame)
                    videowriter.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    currentFrame += 1
                if ret and (currentFrame >= frames_per_video):
                    video += 1
                    videowriter.close()
                    videowriter = imageio.get_writer(os.path.join(fps30_dir,str(video+1)+'-'+f), fps=fps)
                    currentFrame = 0
                if not ret:
                    #print(currentFrame)
                    video += 1
                    videowriter.close()
            videowriter.close()
            cap.release()
        i += 1
            


if __name__ == '__main__':
    root_dir = os.getcwd()
    main(root_dir)           