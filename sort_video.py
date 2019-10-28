import numpy as np
import os
import cv2
import imutils

playback_delay= 10
def resize(img,size,offset=0):
    img = imutils.resize(img, height=size)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2 + offset)
    y_center = int(y/2)  
    img = img[(y_center-size//2):(y_center+size//2), (x_center-size//2):(x_center+size//2)]
    return img


def undistort(img):
    #update K & D with calibration
    K=np.array([[182.07786168118673, 0.0, 320.7685732228652], [0.0, 182.48768379198958, 235.1296956018177], [0.0, 0.0, 1.0]])
    D=np.array([[-0.041045623393449804], [0.005109092320124575], [-0.009949338641026822], [0.0023314540358261196]])
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img
def restore_file(from_dir, to_dir, file_name):
    try:
        os.rename(os.path.join(from_dir, file_name), os.path.join(to_dir, file_name))
        return True
    except:
        return False


def main(root_dir):

    all_files = os.listdir(root_dir)
    dir_names = ['bad_examples','questionable_examples','Falling','Sitting_Up','Standing','Still_On_Bed','Still_On_Ground','Rolling_Bed','Rolling_Ground'] 
    inputs = ['b','q','1','2','3','4','5','6','7']
    dirs = []
    for name in dir_names:
        dirs.append(os.path.join(root_dir,name))
    vid_files = []
    for file in all_files:
        if '._' in file:
            continue
        if file.endswith('.avi') or file.endswith('.mp4'):
            vid_files.append(file)
    print(len(vid_files),' unsorted videos')

    i=0
    while i < len(vid_files):
        try:
            fname = vid_files[i]
            fpath = os.path.join(root_dir,fname)
            cap = cv2.VideoCapture(fpath)
            if not cap.isOpened():
                i += 1
                continue
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    #frame = undistort(frame)
                    frame = resize(frame,256)
                    cv2.imshow('frame count: '+str(frame_count),frame)
                else:
                    break
                cv2.waitKey(playback_delay)
            cap.release()
            print(fname+'\n')
            inp = input('[p] replay previous?\n[r] replay?\n[d] delete?\n[q] questionable?\n[1] falling  \n[2] sitting up\n[3] standing \n[4] still on bed \n[5] still on ground \n[6] rolling bed\n[7] rolling ground  \n[c] exit\n:')
            cv2.destroyAllWindows() # Keep the window open for reference and replay
            if inp in inputs:
                target_dir = dirs[inputs.index(inp)]
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
                os.rename(fpath, os.path.join(target_dir,fname))
            elif inp =='p':
                for directory in dirs:
                    flag = restore_file(directory,root_dir,vid_files[i-1])
                    if flag:
                        i-=1
                        break
                continue
            elif inp == 'c':
                break
            else:
                continue
        except Exception as e:
            raise
            print(e)
        i+=1

if __name__ == '__main__':
    dir_name = input('Directory to sort from:')
    dir_path = os.path.join(os.getcwd(),dir_name)
    main(dir_path)