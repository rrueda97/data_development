import numpy as np
import os
import cv2
import imutils

#room_sorter.py
#plays back data from a specified folder and allows you to sort into different rooms
#MAKE SURE to move folder containing all data to 'data_management' repo folder

#Select path for action folder
action_dir = 'real_w_tensors_2500/Falling_all'

#Reduce Delay to Speed up Playback and vis versa
playback_delay = 10 #ms

def resize(img):
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)]
    return img

def restore_file(from_dir, to_dir, file_name):
    joints_file = file_name[:-len('.avi')]+'_joints.tensor'
    try:
        os.rename(os.path.join(from_dir, file_name), os.path.join(to_dir, file_name))
        os.rename(os.path.join(from_dir, joints_file), os.path.join(to_dir, joints_file))
        return True
    except Exception as e:
        #print(e)
        return False

def main(root_dir):
    # Set Up directories
    all_files = os.listdir(root_dir)
    dir_names = ['bad_examples' ,'questionable_examples', 'room_ricky', 'room_ji', 'room_alex','room_alistair','room_other']
    inputs = ['d', 'q', '1', '2', '3', '4', '5']
    dirs = []
    for name in dir_names:
        dirs.append(os.path.join(root_dir,name))

    #Extract video files
    vid_files = []
    for file in all_files:
        if '._' in file: #mac bug
            continue
        if file.endswith('.avi') or file.endswith('.mp4'):
            vid_files.append(file)
    print(len(vid_files),' unsorted videos')

    #
    i=0
    while i < len(vid_files):
        try:
            fname_vid = vid_files[i]
            fname_joints = fname_vid[:-len('.avi')]+'_joints.tensor'

            vid_path = os.path.join(root_dir, fname_vid)
            joints_path = os.path.join(root_dir, fname_joints)

            cap = cv2.VideoCapture(vid_path)

            if not cap.isOpened():
                i += 1
                continue
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            #print(frame count)
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    frame = resize(frame)
                    cv2.imshow(fname_vid,frame)
                else:
                    break
                cv2.waitKey(playback_delay)
            cap.release()
            print(fname_vid+'\n') 
            inp = input('[enter] replay?\n[p] replay previous?\n[d] delete?\n[q] questionable?\n[1] Ricky_s  \n[2] Ji_s\n[3] Alex_s \n[4] Alistair_s \n[5] Other \n[c] exit\n:')
            cv2.destroyAllWindows() # Keep the window open for reference and replay

            if inp in inputs: #Sort
                target_direc = dirs[inputs.index(inp)]
                if not os.path.exists(target_direc):
                    os.mkdir(target_direc)
                os.rename(vid_path, os.path.join(target_direc,fname_vid))
                os.rename(joints_path, os.path.join(target_direc,fname_joints))
            
            elif inp == 'p': #Replay Previous
                for directory in dirs:
                    flag = restore_file(directory, root_dir, vid_files[i-1])
                    if flag:
                        i-=1
                        break
                continue

            elif inp == 'c': #Exit
                break
            else:
                continue    #Replay Current 

        except Exception as e:
            raise
            print(e)

        i += 1

if __name__ == '__main__':
    root_dir = os.getcwd()
    sort_dir = os.path.join(root_dir,action_dir)
    print('Sorting From:',sort_dir,'\n')
    main(sort_dir)