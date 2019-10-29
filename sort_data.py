import cv2
import os
import time

classIDs = ['Falling', 'SittingUp', 'Standing', 'StillGround', 'StillBed', 'RollingGround', 'RollingBed']
roomIDs = ['RRuedaBed','ATamGarage','','room4','room5','room6']
    #room1 = RRuedaBed = Ricky's Room BlackHorse
    #room2 = RRuedaBed = Ricky's Room BlackHorse (Live Test setup)
    #room3 = ATamGarage = Alex's Garage
    #room4 = ATwomblyMaster = Alistair's Master Room
    #room5 = NMousaBed = Nael's Room BlackHorse
    #room6 = RRuedaLiving = BlackHorse Living Room
personIDs = ['RRueda','JLee','ATwombly','ATam','VBaena','MMercurio','BPeck']
    #RRueda = Ricardo Rueda
    #JLee = Ji Lee
    #ATam = Alex Tam
    #ATwombly = Alistair Twombly
    #VBaena = Valeria Baena
    #MMercurio = Matt Mercurio
    #BPeck = Brandon Peck
camIDs= ['CamFront','CamBack','CamLeft','CamRight']
    #wrt person


class data_file:
    fname_ids = ['classID','personID','roomID','camID','splitNum','dateID','extension']
    other_ids = ['variance','% joints generated','etc']
    columns = fname_ids.extend(other_ids) #?

    #later it can initialize from csv info once it's been written to
    def __init__(self,fname):
        self.fname = fname
        #parse fname into: classID,personID,roomID,camID,dateID
        #if fname doesn't contain info then = None
        ids = fname.split('_')
        if len(ids) == len(fname_ids):
            for i in ids:
                self.fname_ids[i] = ids[i]
        else:
            for i in fname_ids:
                self.fname_ids[i] = None

    def has_joints(self,fname):

    def write_to_csv(self):
        #pandas stuff


def main_loop(data_dir):
    #Parameters
    playback_delay = 10 #ms
    date_fmt = '%m-%d-%y-%H-%M-%S' #April 20th 2020 @ 1:05:30 pm = 04-20-20-13-05-30
    bad_vid_dir = os.path.join(data_dir,'bad_videos')
    videos, joints = grab_files(data_dir)
    renamed_vids= []
    renamed_joints = []
    i = 0
    while i < len(videos):
        cv2.destroyAllWindows() #get rid of any previous display window
        fname_vid = videos[i]
        fname_joints = joints[i]
        fpath_vid = os.path.join(data_dir,fname_vid)
        fpath_joints = os.path.join(data_dir,fname_joints)
        bad_video = disp_vid(fpath_vid)
        if bad_video:
            if not os.path.exists(bad_vid_dir):
                os.mkdir(bad_vid_dir)
            os.rename(fpath_vid,bad_vid_dir)
            os.rename(fpath_joints,bad_vid_dir)
            i += 1
            continue
################################################# pseudo code for process flow of User interface ########

        meta_labels = ['Action Class','Person ID','Room ID','Cam Angle','Split Number']
        for i,label in enumerate(meta_labels):
            print('['+str(i)+'] '+label+': '+str(CURRENT_META_DATA_LABEL)) 
            #[n] None
            #[1] Action Class: StillGround
            #[2] Person ID: RRueda
            #[3] Room ID: RRuedaBed
            #[4] Cam Angle: None
            #[5] Split Number: split1
        for i in other_options:
            print(option)
            #[r] replay
            #[p] replay previous
            #[b] bad example
            #[q] questionable example

        edit_labels = input('Enter Labels You Want to Edit / Other Option') #separated by space
        if edit_labels == 'r'
            disp_vid(fpath_vid)
        elif edit_labels == 'p'
            #undo renaming and go back to previous example
            os.rename(os.path.join(data_dir,renamed_vids[-1]),fpath_vid[i-1])
            os.rename(os.path.join(data_dir,renamed_joints[-1]),fpath_joints[i-1])
            renamed_vids.remove(renamed_vids[-1])
            renamed_joints.remove(renamed_joints[-1])
            i-=1
            continue

        elif edit_labels == 'n'
            confirm = input('are you sure? [y/n]:')
            if confirm =='y':
                dateStamp = time.strftime(fmt)
                fname_vid_new = new_name(fname_vid,classID,personID,roomID,dateStamp)
                fname_joints_new= new_name(fname_joints,classID,personID,roomID,dateStamp)
                renamed_vids.append(fname_vid_new)
                renamed_joints.append(fname_joints_new)
                os.rename(fpath_vid,os.path.join(data_dir,fname_vid_new))
                os.rename(fpath_joints,os.path.join(data_dir,fname_joints_new))
                i+=1
                continue
        else:
            edit_labels = edit_labels.split()
            for label in edit_labels:
                new_label = input('label:')
                #update data class label
            continue 
########################################################################################################



def new_name(fname,classID,personID,roomID,dateStamp):
    if '-' in fname:
        if not fname.index('-') > 3:
            splitNum = fname[:fname.index('-')]
        else:
            splitNum ='Split1'
    else:
        splitNum = 'Split1'
    
    if fname.endswith('.tensor'):
        f_ext = '_joints.tensor'
    elif fname.endswith('.avi'):
        f_ext='.avi'
    elif fname.endswith('.mp4'):
        f_ext='.mp4'
    camNum = fname[fname.index('cam'):fname.index('cam')+len('camX')]
    fname_new = classID+'_'+personID+'_'+roomID+'_'+camNum+'_'+splitNum+'_'+dateStamp+'_'+f_ext
    return fname_new

def resize(img,size,offset=0):
    img = imutils.resize(img, height=size)
    y,x = img.shape[0],img.shape[1]
    x_center = int(x/2 + offset)
    y_center = int(y/2)  
    img = img[(y_center-size//2):(y_center+size//2), (x_center-size//2):(x_center+size//2)]
    return img

def disp_vid(fpath,playback_delay):
    bad_video = False
    cap = cv2.VideoCapture(fpath)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #Get frame count to make sure it is a 30 frame example
    if frame_count != 30:
        print('Video is NOT 30 frames')
        bad_video = True
        return bad_video
    if not cap.isOpened():
        print('Could display video')
        bad_video = True
        return bad_video
    while cap.isOpened():
        ret,frame = cap.read()
        if ret:
            frame =resize(frame,256)
            cv2.imshow(fpath,frame)
        else: break
        cv2.waitKey(playback_delay)
    cap.release()

def grab_files(root_dir): #creates matched lists of video and joints files
    no_joints_dir = os.path.join(root_dir,'no_joints')
    if os.path.exists(no_joints_dir):
        os.mkdir(no_joints_dir)
    all_files = os.listdir(root_dir)
    vid_files = []
    joints_files = []
    for file in all_files:
        if '._' in file:
            all_files.remove(file)
            continue
        if file.endswith('.avi') or file.endswith('.mp4'):
            joints_file = file[:-len('.avi')]+'_joints.tensor' 
            joints_path = os.path.join(root_dir,joints_file) #check for associated joints file
            if not os.path.exists(joints_path):
                os.rename(os.path.join(root_dir,file),os.path.join(no_joints_dir,file))
                continue
            vid_files.append(file)
            joints_files.append(joints_file)
    return vid_files, joints_files


if __name__ == '__main__':
    dir_name = input('Directory to sort from:')
    dir_path = os.path.join(os.getcwd(),dir_name)
    main_loop(dir_path)