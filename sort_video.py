import numpy as np
import os
import cv2
import imutils

# 108 images 9/7 Nael's Room
DIM=(640, 480)
K=np.array([[240.21086643847192, 0.0, 318.0152843306422], [0.0, 240.66145029587912, 220.42879674202533], [0.0, 0.0, 1.0]])
D=np.array([[-0.03561582686662651], [-0.011557711209240214], [0.004239894818130242], [-0.0011662345578036493]])

def resize(img):
    img = imutils.resize(img, height=256)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2)
    y_center = int(y/2)  
    img = img[(y_center-128):(y_center+128), (x_center-128):(x_center+128)]
    return img
def undistort2(img, balance=0.1, dim2=None, dim3=None):
    #img = cv2.imread(img)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1] #"Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0] # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0            # Except that K[2][2] is always 1.0
                                    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

def undistort1(img):
    #update K & D with calibration
    #K=np.array([[182.07786168118673, 0.0, 320.7685732228652], [0.0, 182.48768379198958, 235.1296956018177], [0.0, 0.0, 1.0]])
    #D=np.array([[-0.041045623393449804], [0.005109092320124575], [-0.009949338641026822], [0.0023314540358261196]])
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
    files = os.listdir(root_dir)
    del_dir = os.path.join(root_dir, 'bad_examples')
    unsure_dir = os.path.join(root_dir,'questionable_examples')
    fall_dir = os.path.join(root_dir, 'Falling')
    still_gnd_dir = os.path.join(root_dir, 'Still_On_Ground')
    situp_dir = os.path.join(root_dir, 'Sitting_Up')
    still_bed_dir = os.path.join(root_dir,'Still_On_Bed')
    stand_dir = os.path.join(root_dir,'Standing')
    roll_gnd_dir = os.path.join(root_dir, 'Rolling_Ground')
    roll_bed_dir = os.path.join(root_dir, 'Rolling_Bed')
    if not os.path.exists(del_dir):
        os.mkdir(del_dir)
    if not os.path.exists(unsure_dir):
        os.mkdir(unsure_dir)

    i=0
    while i < len(files):
        try:
            f = files[i]
            if '._' in f: #hidden files bug
                i += 1
                continue
            if '.avi'or '.mp4' in f: #only try to read avi files
                file_path = os.path.join(root_dir, f)
                cap = cv2.VideoCapture(file_path)
                if not cap.isOpened():
                    i += 1
                    continue
                print(f)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    if ret:
                        #frame = undistort1(frame)
                        frame = resize(frame)
                        cv2.imshow('frame count: '+str(frame_count),frame)
                    else:
                        break
                    cv2.waitKey(10)


                cap.release()
                
                inp = input('[p] replay previous?\n[r] replay?\n[d] delete?\n[q] questionable?\n[1] falling  \n[2] sitting up\n[3] standing \n[4] still on bed \n[5] still on ground \n[6] rolling bed\n[7] rolling ground  \n[c] exit\n:')
                cv2.destroyAllWindows() # Keep the window open for reference and replay
                if inp == 'd':
                    os.rename(file_path, os.path.join(del_dir, f))
                elif inp == 'q':
                    os.rename(file_path, os.path.join(unsure_dir, f))         
                elif inp == '1':
                    if not os.path.exists(fall_dir):
                        os.mkdir(fall_dir)
                    os.rename(file_path, os.path.join(fall_dir, f))
                elif inp == '2':
                    if not os.path.exists(situp_dir):
                        os.mkdir(situp_dir)
                    os.rename(file_path, os.path.join(situp_dir, f))
                elif inp == '3':
                    if not os.path.exists(stand_dir):
                        os.mkdir(stand_dir)
                    os.rename(file_path, os.path.join(stand_dir, f))
                elif inp == '4':
                    if not os.path.exists(still_bed_dir):
                        os.mkdir(still_bed_dir)
                    os.rename(file_path, os.path.join(still_bed_dir, f))
                elif inp == '5':
                    if not os.path.exists(still_gnd_dir):
                        os.mkdir(still_gnd_dir)
                    os.rename(file_path, os.path.join(still_gnd_dir, f))
                elif inp == '6':
                    if not os.path.exists(roll_bed_dir):
                        os.mkdir(roll_bed_dir)
                    os.rename(file_path, os.path.join(roll_bed_dir, f))
                elif inp == '7':
                    if not os.path.exists(roll_gnd_dir):
                        os.mkdir(roll_gnd_dir)
                    os.rename(file_path, os.path.join(roll_gnd_dir, f))
                
                elif inp== 'p': #Replay Previous
                    in_del = restore_file(del_dir, root_dir, files[i-1])
                    in_fall = restore_file(fall_dir, root_dir, files[i-1])
                    in_situp = restore_file(situp_dir, root_dir, files[i-1])
                    in_stand = restore_file(stand_dir, root_dir, files[i-1])
                    in_still_bed = restore_file(still_bed_dir, root_dir, files[i-1])
                    in_still_gnd = restore_file(still_gnd_dir, root_dir, files[i-1])
                    in_roll_bed = restore_file(roll_bed_dir, root_dir, files[i-1])
                    in_roll_gnd = restore_file(roll_gnd_dir, root_dir, files[i-1])
                    flag  = in_del or in_fall or in_situp or in_stand or in_still_bed or in_still_gnd or in_roll_bed or in_roll_gnd
                    if flag:
                        i-=1
                        continue
                    continue
                elif inp == 'r': #Replay Current
                    continue
                elif inp == 'c': #Exit
                    break
                else:
                    continue

        except Exception as e:
            raise
            print(e)

        i += 1

if __name__ == '__main__':
    dir_name = input('Directory to sort from:')
    dir_path = os.path.join(os.getcwd(),dir_name)
    main(dir_path)