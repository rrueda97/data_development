import cv2
import os
import time

classIDs = ['falling', 'sittingUp', 'standing', 'stillGround', 'stillBed', 'rollingGround', 'rollingBed']
roomIDs = ['room1','room2','room3','room4','room5','room6']
    #room1 = Ricky's Room BlackHorse
    #room2 = Ricky's Room BlackHorse (Live Test setup)
    #room3 = Alex's Garage
    #room4 = Alistair's Master Room
    #room5 = Nael's Room BlackHorse
    #room6 = BlackHorse Living Room
personIDs = ['RR1','JL1','AT1','AT2','VB1','MM1','BP1']
    #RR1 = Ricardo Rueda
    #JL1 = Ji Lee
    #AT1 = Alex Tam
    #AT2 = Alistair Twombly
    #VB1 = Valeria Baena
    #MM1 = Matt Mercurio
    #BP1 = Brandon Peck
def new_name(fname,classID,personID,roomID,dateStamp):
    if '-' in fname:
        if not fname.index('-') > 3:
            splitNum = fname[:fname.index('-')]
        else:
            splitNum ='1'
    else:
        splitNum = '1'
    
    if fname.endswith('.tensor'):
        f_ext = '_joints.tensor'
    elif fname.endswith('.avi'):
        f_ext='.avi'
    elif fname.endswith('.mp4'):
        f_ext='.mp4'
    camNum = fname[fname.index('cam'):fname.index('cam')+len('camX')]
    fname_new = classID+'_'+personID+'_'+roomID+'_'+dateStamp+'_'+camNum+'_'+splitNum+f_ext
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
