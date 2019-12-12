import cv2
import imutils
import os
import time
import csv
import sys

# All Labels: Subject to Change
classID_labels = ['Falling', 'SittingUp', 'Standing', 'StillGround', 'StillBed', 'RollingGround', 'RollingBed']
roomID_labels = ['RRuedaBed', 'ATamGarage', 'ATwomblyMaster', 'NMousaBed', 'RRuedaLiving', 'JLeeBed']
personID_labels = ['RRueda', 'JLee', 'ATwombly', 'ATam', 'VBaena', 'MMercurio', 'DBerry', 'JAlvarenga', 'RBhardwaj']
camID_labels = ['CamFront', 'CamBack', 'CamLeft', 'CamRight']
splitNum_labels = ['split0', 'split1', 'split2']
descrip_labels = ['low', 'medium', 'high']
position_labels = ['center', 'right', 'left', 'top', 'bottom']
clothing_labels = ['tshirt + pants', 'tshirt + shorts', 'longsleeve + pants', 'longsleeve + shorts', 'tank + pants',
                   'tank + shorts']
gender_labels = ['male', 'female']
displace_labels = ['front', 'back', 'left', 'right']
labels_dict = {'classID': classID_labels, 'personID': personID_labels, 'roomID': roomID_labels, 'camID': camID_labels,
               'splitNum': splitNum_labels, 'position': position_labels, 'clothing': clothing_labels, 'gender':
                   gender_labels, 'displacement': displace_labels}
labels_dict.update(dict.fromkeys(['skinTone', 'lighting', 'roomInfo', 'zoom', 'vidSpeed', 'variance'], descrip_labels))


class DataFile:
    def __init__(self, file_name, root_dir, constants=None):
        self.fname = file_name
        joints_path = os.path.join(root_dir, self.fname[:-len('.avi')]+'_joints.tensor')
        if not os.path.exists(joints_path):
            self.has_joints = False
        else:
            self.has_joints = True
        if constants:
            self.classID = constants['classID']
            self.personID = constants['personID']
            self.roomID = constants['roomID']
            self.camID = constants['camID']
            self.splitNum = constants['splitNum']
            self.position = constants['position']
            self.clothing = constants['clothing']
            self.gender = constants['gender']
            self.skinTone = constants['skinTone']
            self.lighting = constants['lighting']
            self.roomInfo = constants['roomInfo']
            self.zoom = constants['zoom']
            self.vidSpeed = constants['vidSpeed']
            self.variance = constants['variance']
            self.displacement = constants['displacement']
            self.bad = False
            self.questionable = False
        else:
            self.classID = None
            self.personID = None
            self.roomID = None
            self.camID = None
            self.splitNum = None
            self.position = None
            self.clothing = None
            self.gender = None
            self.skinTone = None
            self.lighting = None
            self.roomInfo = None
            self.zoom = None
            self.vidSpeed = None
            self.variance = None
            self.displacement = None
            self.bad = False
            self.questionable = False

    def check(self):
        if not self.bad:
            self.bad_info = None
        if not self.questionable:
            self.quest_info = None

    def is_bad(self, bad_info):
        self.bad = True
        self.bad_info = bad_info 

    def is_quest(self, quest_info):
        self.questionable = True
        self.quest_info = quest_info

    def is_good(self):
        self.questionable = False
        self.quest_info = None
        self.bad = False

    def set_new_labels(self, new_labels):
        for key in labels_dict:
            if key not in new_labels:
                new_labels[key] = None
        self.classID = new_labels['classID']
        self.personID = new_labels['personID']
        self.roomID = new_labels['roomID']
        self.camID = new_labels['camID']
        self.splitNum = new_labels['splitNum']
        self.position = new_labels['position']
        self.clothing = new_labels['clothing']
        self.gender = new_labels['gender']
        self.skinTone = new_labels['skinTone']
        self.lighting = new_labels['lighting']
        self.roomInfo = new_labels['roomInfo']
        self.zoom = new_labels['zoom']
        self.vidSpeed = new_labels['vidSpeed']
        self.variance = new_labels['variance']
        self.displacement = new_labels['displacement']

    def new_name(self):
        date_fmt = '%m-%d-%y-%H-%M-%S'  # April 20th 2020 @ 1:05:30 pm = 04-20-20-13-05-30
        dateStamp = time.strftime(date_fmt)
        if self.fname.endswith('.avi'):
            f_ext = '.avi'
        elif self.fname.endswith('.mp4'):
            f_ext = '.mp4'
        fname_new = str(self.classID)+'_'+str(self.personID)+'_'+str(self.roomID)+'_'+str(self.camID)+'_'+str(self.splitNum)+'_'+dateStamp+f_ext
        fname_joints_new = str(self.classID)+'_'+str(self.personID)+'_'+str(self.roomID)+'_'+str(self.camID)+'_'+str(self.splitNum)+'_'+dateStamp+'_'+'joints.tensor'
        return fname_new, fname_joints_new

    def re_name(self, root_dir, labeled_dir):
        if not os.path.exists(labeled_dir):
            os.mkdir(labeled_dir)
        # update filename attributes, store previous filename, rename files
        self.prev_fname = self.fname 
        self.prev_fname_joints = self.fname[:-len('.avi')]+'_joints.tensor'
        self.fname, self.fname_joints = self.new_name()
        os.rename(os.path.join(root_dir, self.prev_fname), os.path.join(labeled_dir, self.fname))
        if self.has_joints:
            os.rename(os.path.join(root_dir, self.prev_fname_joints), os.path.join(labeled_dir, self.fname_joints))


def csv_write(csv_file_path, data_obj):
    file_exists = os.path.isfile(csv_file_path)
    data_dict = vars(data_obj)
    col_names = list(data_dict.keys())
    with open(csv_file_path, mode='a+', newline='') as csv_file:
        data_writer = csv.DictWriter(csv_file, fieldnames=col_names)
        if not file_exists:
            data_writer.writeheader()
        data_writer.writerow(vars(data_obj))
    print('saved to', csv_file_path)


def csv_overwrite(csv_file_path):  # removes last row
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            rows_list = list(reader)
        rows_list.pop()
        with open(csv_file_path, mode='w', newline='') as csv_file_overwrite:
            writer = csv.writer(csv_file_overwrite)
            writer.writerows(rows_list)


def sort_attrs(data_obj):   # creates dictionary where empty attributes of type None are first (have keys 0-n)
    ignored = ['fname', 'has_joints', 'fname_joints', 'bad', 'questionable']
    sorted_dict = {}
    sorted_ls = []
    attrs_dict = vars(data_obj)
    for attr in attrs_dict:  # creates a list where empty attributes ( = None) are on top
        if attr in ignored:
            continue
        if not attrs_dict[attr]:
            sorted_ls.insert(0, attr)
        else:
            sorted_ls.append(attr)
    for item in sorted_ls:  # dictionary with list indices as keys
        sorted_dict[str(sorted_ls.index(item))] = item
    return sorted_dict


def set_constants(constants=None):  # input previous set constants
    if not constants:
        constants_dict = {}
    else:
        constants_dict = constants
    while True:
        constants_ls = []
        print('\nSelect Constant Attribute Labels')
        for i, attr in enumerate(labels_dict):
            if attr in constants_dict:
                constants_ls.append(attr)
                print('['+str(i)+']', attr, ':', constants_dict[attr])  # show constants that have been set
            else:
                constants_ls.append(attr)
                print('['+str(i)+']', attr)
        print('[q] Done')
        user_inp = input('\nSelect an Attribute: ')
        if user_inp == 'q':
            break
        elif user_inp.isnumeric():
            if len(constants_ls) <= int(user_inp):
                print('input out of range')
                continue
            else:
                attr_sel = constants_ls[int(user_inp)]
        else:
            print('invalid input')
            continue
        print('\n', attr_sel, ':')
        for j, label in enumerate(labels_dict[attr_sel]):
            print('['+str(j)+']', label)
        print('[n] None')
        new_label_i = input('\nSelect a Label: ')

        if new_label_i == 'n':
            new_label = None
        elif new_label_i.isnumeric():
            if len(labels_dict[attr_sel]) <= int(new_label_i):
                print('invalid input')
                continue
            else:
                new_label = labels_dict[attr_sel][int(new_label_i)]
        else:
            print('invalid input')
            continue 
        constants_dict[attr_sel] = new_label
    for key in labels_dict:  # set everything else to None
        if key not in constants_dict:
            constants_dict[key] = None
    return constants_dict


def edit_label(attr):
    while True:
        print('\nLabels for', attr)
        for i, label in enumerate(labels_dict[attr]):
            print('['+str(i)+']', label)
        new_label_i = input('Select New Label: ')
        if new_label_i.isnumeric():
            if int(new_label_i) >= len(labels_dict[attr]):  # if out of range
                print('invalid input')
                continue
            else:
                new_label = labels_dict[attr][int(new_label_i)]
                break
        else:
            continue
    return new_label


def restore(prev_data_obj, from_dir, to_dir):
    from_path = os.path.join(from_dir, prev_data_obj.fname)
    from_path_joints = os.path.join(from_dir, prev_data_obj.fname_joints)
    to_path = os.path.join(to_dir, prev_data_obj.prev_fname)
    to_path_joints = os.path.join(to_dir, prev_data_obj.prev_fname_joints)
    os.rename(from_path, to_path)
    prev_data_obj.fname = prev_data_obj.prev_fname
    if prev_data_obj.has_joints:
        os.rename(from_path_joints, to_path_joints)
        prev_data_obj.fname_joints = prev_data_obj.prev_fname_joints


def preview(data_dir, playback_delay=10):
    videos, joints = grab_files(data_dir)
    i = 0
    while i < len(videos):
        cv2.destroyAllWindows()
        fpath_vid = os.path.join(data_dir, videos[i])
        disp_vid(fpath_vid, playback_delay)
        while True:
            print('Previewing Data\n[enter] replay\n[a] previous video\n[d] next video\n[q] exit preview')
            usr_inp = input(':')
            if not usr_inp:
                break
            elif usr_inp == 'a':
                i -= 1
                break
            elif usr_inp == 'd':
                i += 1
                break
            elif usr_inp == 'q':
                return
            else:
                print('invalid input')
                continue


def main_loop(labeled_dir, data_dir, csv_path):
    restored = None     # initialize restored flag
    constants = None    # initialize with no constants
    playback_delay = 50  # ms
    bad_vid_dir = os.path.join(data_dir, 'bad_videos')
    videos, joints = grab_files(data_dir)
    data_objs = [] 
    i = 0
    print('total videos:', len(videos), 'joints:', len(joints))
    while i < len(videos):
        cv2.destroyAllWindows()
        fname_vid = videos[i]
        fname_joints = joints[i]
        fpath_vid = os.path.join(data_dir, fname_vid)
        fpath_joints = os.path.join(data_dir, fname_joints)
        if not os.path.exists(fpath_vid):
            print("can't replay what has already been sorted")
            i += 1
            continue
        bad_video = disp_vid(fpath_vid, playback_delay)
        if bad_video:
            if not os.path.exists(bad_vid_dir):
                os.mkdir(bad_vid_dir)
            os.rename(fpath_vid, bad_vid_dir)
            os.rename(fpath_joints, bad_vid_dir)
            i += 1
            continue
        if not restored:
            data_obj = DataFile(fname_vid, data_dir, constants)
        else:
            data_obj = data_objs.pop()
            restored = False
        opts_dict = {'[exit]': 'exit', '[enter]': 'replay', '[p]': 'preview videos', '[c]': 'set constant labels', '[z]': 'undo ', '[f]': 'confirm labels', '[b]': 'bad', '[q]': 'questionable'}
        new_labels = {}
        while True:
            attrs = sort_attrs(data_obj)
            attr_vals = vars(data_obj)  # Dictionary with current attributes and labels
            print('videos sorted:', len([f for f in os.listdir(labeled_dir) if f.endswith('.avi') and f[:2] != '._']))
            print('\nfile name:', data_obj.fname)
            print('has joints:', data_obj.has_joints, '\n')
            for opt in opts_dict:
                print(opt, opts_dict[opt])
            print('')
            for attr in attrs:
                print('['+attr+']', attrs[attr]+':', attr_vals[attrs[attr]])  # [1] classID: Standing
            x = input('\nAttribute to Edit: ')

            if not x:
                disp_vid(fpath_vid, playback_delay)
            elif x == 'p':
                preview(data_dir)
                break
            elif x == 'b':
                bad_info = input('\nNote on why its bad: ')
                data_obj.is_bad(bad_info)
            elif x == 'q':
                quest_info = input('\nNote on why its questionable: ')
                data_obj.is_quest(quest_info)
            elif x == 'c':
                constants = set_constants(constants)  # initializes/updates constants
                break
            elif x == 'f':
                confirm = input('Are you sure?[y/n]: ')
                if confirm == 'y':
                    data_obj.re_name(data_dir, labeled_dir)  # rename files & put them into labeled_data
                    data_obj.check()
                    data_objs.append(data_obj)  # append object for accessing later
                    csv_write(csv_path, data_obj)
                    i += 1
                    break
                else:
                    continue
            elif x == 'z':
                if len(data_objs) > 0:
                    restore(data_objs[-1], labeled_dir, data_dir)  # restores previous file to original filename & path
                    restored = True
                    csv_overwrite(csv_path)
                    i -= 1
                    break
                else:
                    print('no data sorted yet')
                    break
            elif x == 'exit':
                return

            elif x in attrs.keys():
                new_labels[attrs[x]] = edit_label(attrs[x])
                if constants:
                    set_labels = constants.copy()
                    set_labels.update(new_labels)   # merge new labels into a temporary dictionary
                    data_obj.set_new_labels(set_labels)   # update attributes in object
                else:
                    set_labels = {}
                    set_labels.update(new_labels)
                    data_obj.set_new_labels(set_labels)
            else:
                print('invalid input')
                continue


def resize(img, size, offset=0):
    img = imutils.resize(img, height=size)
    y, x = img.shape[0], img.shape[1]
    x_center = int(x/2 + offset)
    y_center = int(y/2)  
    img = img[(y_center-size//2):(y_center+size//2), (x_center-size//2):(x_center+size//2)]
    return img


def disp_vid(fpath, playback_delay):
    cap = cv2.VideoCapture(fpath)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get frame count to make sure it is a 30 frame example
    if frame_count != 30:
        print('Video is NOT 30 frames')
        bad_video = True
        return bad_video
    if not cap.isOpened():
        print('Could display video')
        bad_video = True
        return bad_video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = resize(frame, 256)
            cv2.imshow('playback_delay: '+str(playback_delay)+' ms', frame)
        else:
            break
        cv2.waitKey(playback_delay)
    cap.release()


def grab_files(root_dir):
    no_joints_dir = os.path.join(root_dir, 'no_joints')
    all_files = os.listdir(root_dir)
    vid_files = []
    joints_files = []
    for file in all_files:
        if file.startswith('._'):
            continue
        if file.endswith('.avi') or file.endswith('.mp4'):
            joints_file = file[:-len('.avi')]+'_joints.tensor' 
            joints_path = os.path.join(root_dir, joints_file)  # check for associated joints file
            if not os.path.exists(joints_path):
                if not os.path.exists(no_joints_dir):
                    os.mkdir(no_joints_dir)
                os.rename(os.path.join(root_dir, file), os.path.join(no_joints_dir, file))
                print(file, 'has no joints')
                continue
            vid_files.append(file)
            joints_files.append(joints_file)
        else:
            if not file.endswith('tensor'):
                print('not including:', file)
    return vid_files, joints_files


if __name__ == '__main__':
    while True:
        dir_name = input('Directory to sort from:')
        dir_path = os.path.join(os.getcwd(), dir_name)
        labeled_name = input('Specify path to labeled data folder: CurrentDir/')
        labeled_path = os.path.join(os.getcwd(), labeled_name)
        if not os.path.isdir(dir_path):
            print(dir_name, 'is not a directory\n')
            continue
        csv_filepath = os.path.join(os.getcwd(), 'labeled_data.csv')
        main_loop(labeled_path, dir_path, csv_filepath)
        while True:
            inp = input('\n[s] keep sorting\n[q] exit\n:')
            if inp == 's':
                break
            elif inp == 'q':
                sys.exit()
            else:
                print('\ninvalid input\n')
                continue
