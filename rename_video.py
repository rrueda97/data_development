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
def new_name(fname,classID,personID,roomID,dateStamp):
    if '-' in fname:
        if not fname.index('-') > 3:
            splitNum = fname[:fname.index('-')]
        else:
            splitNum ='split1'
    else:
        splitNum = 'split1'
    
    if fname.endswith('.tensor'):
        f_ext = '_joints.tensor'
    elif fname.endswith('.avi'):
        f_ext='.avi'
    elif fname.endswith('.mp4'):
        f_ext='.mp4'
    camNum = fname[fname.index('cam'):fname.index('cam')+len('camX')]
    fname_new = classID+'_'+personID+'_'+roomID+'_'+camNum+'_'+splitNum+'_'+dateStamp+'_'+f_ext
    return fname_new

def main():
    target_dir = input('Folder path to rename:')
    classID = input('classID:')
    personID = input('personID:')
    roomID = input('roomID:')
    fmt = '%m-%d-%y-%H-%M-%S' #April 20th 2020 @ 1:05:30 pm = 04-20-20-13-05-30
    target_path= os.path.join(os.getcwd(),target_dir)
    renamed_path = os.path.join(target_path,os.path.basename(target_path)+'_renamed')
    if not os.path.exists(renamed_path):
        os.mkdir(renamed_path)
    all_files = os.listdir(target_path)
    vid_files = []
    for file in all_files:
        if '._' in file:
            all_files.remove(file)
            continue
        if file.endswith('.avi') or file.endswith('.mp4'):
            vid_files.append(file)
    i=0
    for fname_vid in vid_files:
        time.sleep(2)
        dateStamp = time.strftime(fmt)
        fname_joints = fname_vid[:-len('.avi')]+'_joints.tensor'
        vid_renamed = new_name(fname_vid,classID,personID,roomID,dateStamp)
        joints_renamed = new_name(fname_joints,classID,personID,roomID,dateStamp)
        os.rename(os.path.join(target_path,fname_vid),os.path.join(renamed_path,vid_renamed))
        os.rename(os.path.join(target_path,fname_joints),os.path.join(renamed_path,joints_renamed))
        i+=1
        print(i,'/',len(vid_files),' videos renamed')
if __name__ == '__main__':
    main()
    while True:
        
        inp = input('continue? [y/n]:')
        if inp == 'n': 
            break
        elif inp == 'y':
            main()
        else:
            print('invalid entry')
