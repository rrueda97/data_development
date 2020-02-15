import cv2
import numpy as np
import imutils
import os


threshold = 7    # How many extra frames should result in a new video?
manual = False   #flag to count manually
preview = False  # flag to preview manually generated video
########################################################################################################################
# 108 images 9/7 MousaLiving
DIM=(640, 480)
K=np.array([[240.21086643847192, 0.0, 318.0152843306422],
            [0.0, 240.66145029587912, 220.42879674202533],
            [0.0, 0.0, 1.0]])
D=np.array([[-0.03561582686662651],
            [-0.011557711209240214],
            [0.004239894818130242],
            [-0.0011662345578036493]])
########################################################################################################################

def undistort(img, K, D):
    h,w, channel = img.shape
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


def resize(img):  # Transforms Frame to Model Specifications (256x256)
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)] #256x256 center crop (8/9/2019)
    return img


def count_frames(cap):  # manual frame count
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
        

def main(split_dir):
    vids = [f for f in os.listdir(split_dir) if not f.startswith('._') and (f.endswith(('mp4','avi')))]
    codec = cv2.VideoWriter_fourcc(*"XVID")
    for i, vid in enumerate(vids):
        print('spliting '+vid+' '+str(i)+'/'+str(len(vids)))
        split_video(vid, split_dir, codec, imgs=True)


def split_video(video_file, split_dir, fourcc, frame_split=None, write_size= None, write_fps=None, imgs=False, vids=False,
                label_imgs=False):
    # video codec (use MJPG for Linux),  'MP4V' for mp4 files?
    # Figure out codecs for all machines
    split_path = split_dir+'_split'
    if not os.path.isdir(split_path):
        os.mkdir(split_path)
    video_path = os.path.join(split_dir, video_file)
    new_video_path = os.path.join(split_path, video_file)
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        frame_size = (int(cap.get(3)),int(cap.get(4)))
        if manual:
            total_frames = count_frames(cap)
        else:
            total_frames = int(cap.get(7))
        # split into videos
        if vids:
            if not write_fps:
                write_fps = cap.get(5)
            r = total_frames%frame_split
            initial_frames = list(range(0,total_frames+1,30))
            initial_frames = initial_frames[:-1]
            if r >= threshold:
                initial_frames.append(total_frames-30)
            videos = len(initial_frames)
            print('current file:', video_path)
            print('total frames: ',total_frames,'\nframe rate:',int(cap.get(5)))
            print('splitting into: {} videos ...'.format(videos))
            video = 0
            for j in initial_frames:
                writer = cv2.VideoWriter(new_video_path ,fourcc, write_fps, frame_size)
                for k in range(frame_split):
                    cap.set(1,j+k)
                    ret, frame = cap.read()
                    if ret:
                        # frame = undistort(frame)
                        # frame = resize(frame)
                        writer.write(frame)
                writer.release()
                video += 1

        elif imgs:
            for i in range(total_frames):
                cap.set(1, i)
                ret, img = cap.read()
                if ret:
                    # frame = undistort(img)
                    # frame = resize(img)
                    if label_imgs:
                        cv2.imshow('frame '+str(i), img)
                        labels = ['Falling', 'SittingUp', 'Standing', 'StillGround', 'StillBed', 'RollingGround',
                                  'RollingBed']
                        label_i = input('[1] Falling\n[2] Sitting\n[3] Standing\n[4] StillGround\n''[5] StillBed\n[6]'+
                                        'RollingGround\n[7] RollingBed\n: ')
                        cv2.imwrite(new_video_path+'/frame_'+str(i)+'_'+labels[int(label_i)]+'.png', img)
                    else:
                        try:
                            cv2.imwrite(new_video_path[:-len('.avi')]+'_frame_'+str(i)+'.png', img) # file format?
                        except Exception as e:
                            print(e)



if __name__ == '__main__':
    dir_name = input('Directory to split from:')
    dir_path = os.path.join(os.getcwd(),dir_name) 
    main(dir_path)