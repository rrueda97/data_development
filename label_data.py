import cv2
import imutils
import os
import time
import sys
import pandas as pd

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
displace_labels = ['front', 'back', 'left', 'right', 'clockwise', 'counterclockwise']
ALL_LABELS = {'classID': classID_labels, 'personID': personID_labels, 'roomID': roomID_labels, 'camID': camID_labels,
              'splitNum': splitNum_labels, 'position': position_labels, 'clothing': clothing_labels,
              'gender': gender_labels, 'displacement': displace_labels}
ALL_LABELS.update(dict.fromkeys(['skinTone', 'lighting', 'roomInfo', 'zoom', 'vidSpeed', 'variance'], descrip_labels))

SAVED_CAPTIONS = []


class DataObject:
    """Holds meta data of a video, loads and saves to a csv file"""
    def __init__(self, file_name: str, root_dir: str, labels_path: str, constants: dict = None):
        self.fname = file_name
        joints_path = os.path.join(root_dir, self.fname[:-len('.avi')]+'_joints.tensor')  # check for joints
        if os.path.exists(joints_path):
            self.has_joints = True
            self.fname_joints = self.fname[:-len('.avi')]+'_joints.tensor'
        else:
            self.has_joints = False
            self.fname_joints = None
        loaded = self.load_labels(labels_path)
        if loaded:
            return
        elif constants:  # load from constants
            self.set_labels(constants)
            self.bad = False
            self.bad_info = None
            self.questionable = False
            self.quest_info = None
            self.prev_fname = None
            self.prev_fname_joints = None
        else:  # load empty
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
            self.bad_info = None
            self.questionable = False
            self.quest_info = None
            self.prev_fname = None
            self.prev_fname_joints = None

    def load_labels(self, labels_file_path: str):
        restored = False
        try:
            all_labels_df = pd.read_csv(labels_file_path)
        except FileNotFoundError:
            return False
        if self.fname in all_labels_df.fname.to_list():
            labels_df = all_labels_df.loc[all_labels_df['fname'] == self.fname]
        elif self.fname in all_labels_df.prev_fname.to_list():
            labels_df = all_labels_df.loc[all_labels_df['prev_fname'] == self.fname]
            restored = True
        else:
            return False
        print(f'\nFOUND:\n{self.fname}\nIN:\n{labels_file_path}\nLOADING LABELS...\n')
        labels_df = labels_df.where(pd.notnull(labels_df), None)  # turning nans to None types
        loaded_labels = labels_df.to_dict('records')[0]
        self.set_labels(loaded_labels)
        if restored:
            self.fname = self.prev_fname
            self.prev_fname = None
            if self.has_joints:
                self.fname_joints = self.fname_joints
                self.prev_fname_joints = None
        return True

    def set_labels(self, labels_dictionary: dict):
        for attr in labels_dictionary:
            setattr(self, attr, labels_dictionary[attr])

    def new_name(self): # assuming videos will already be time stamped, append labels to the front.
        split_fname = self.fname.split('_')
        if len(split_fname) == 9:  # video has been labeled before and has new format of date stamp
            date_stamp = '_'.join(split_fname[-4:])
        elif len(split_fname) == 6: # video has been labeled before and has old format of date stamp
            date_stamp = split_fname[-1]
        elif len(split_fname) == 4: # video has not been labeled before and has new format of date stamp
            date_stamp = self.fname
        else:
            raise ValueError(f'video has an unknown file name format\n{self.fname}')
        assert '.avi' in date_stamp or '.mp4' in date_stamp

        fname_new = f'{self.classID}_{self.personID}_{self.roomID}_{self.camID}_{self.splitNum}_{date_stamp}'
        if self.has_joints:
            fname_joints_new = fname_new[:-len('.avi')]+'_joints.tensor'
        else:
            fname_joints_new = None
        return fname_new, fname_joints_new

    def re_name(self, root_dir, labeled_dir):
        if not os.path.exists(labeled_dir):
            os.mkdir(labeled_dir)
        # update filename attributes, store previous filename, rename files
        self.prev_fname = self.fname
        if self.has_joints:
            self.prev_fname_joints = self.fname[:-len('.avi')]+'_joints.tensor'
        else:
            self.prev_fname_joints = None
        self.fname, self.fname_joints = self.new_name()
        os.rename(os.path.join(root_dir, self.prev_fname), os.path.join(labeled_dir, self.fname))
        if self.has_joints:
            os.rename(os.path.join(root_dir, self.prev_fname_joints), os.path.join(labeled_dir, self.fname_joints))

    def is_bad(self, bad_info):
        self.bad = True
        self.bad_info = bad_info

    def is_quest(self, quest_info):
        self.questionable = True
        self.quest_info = quest_info

    def output_to_csv(self, labels_path):
        if os.path.exists(labels_path):
            all_labels_df = pd.read_csv(labels_path)
            all_labels_df = all_labels_df.where(pd.notnull(all_labels_df), None)
        else:
            columns = list(self.__dict__.keys())
            all_labels_df = pd.DataFrame(columns=columns)
        labels_dictionary = self.__dict__
        labels_list = []  # pandas wants a list in the right order instead of a dictionary for some fucking reason
        for c in all_labels_df.columns:
            labels_list.append(labels_dictionary[c])
        restored_entry = all_labels_df.loc[all_labels_df['prev_fname'] == self.fname]
        prev_labeled_entry = all_labels_df.loc[all_labels_df['fname'] == self.prev_fname]

        if not restored_entry.empty:  # replace the row for this data file if it's been restored due to wrong labeling
            all_labels_df.iloc[restored_entry.index] = [labels_list]
        elif not prev_labeled_entry.empty:  # replace the row for this data file if it's been previously labeled
            all_labels_df.iloc[prev_labeled_entry.index] = [labels_list]
        else:
            all_labels_df = all_labels_df.append(labels_dictionary, ignore_index=True)
        print(f'\nWRITING LABELS TO {labels_path}\n')
        all_labels_df.to_csv(labels_path, index=False)


def sort_attrs(data_obj: DataObject):
    """creates dictionary where empty attributes of type None are first (have keys 0-n)

    Args:
        data_obj: a DataObject of a video

    Returns:
        sorted_dict: dictionary with sorted list indices as keys and attributes as values
    """
    ignored = ['fname', 'prev_fname', 'has_joints', 'prev_fname_joints', 'fname_joints', 'bad', 'questionable']
    sorted_dict = {}
    sorted_ls = []
    attrs_dict = vars(data_obj)
    for attr in attrs_dict:  # creates a list where empty attributes ( = None) are on top
        if attr in ignored:
            continue
        if attrs_dict[attr] is None:
            sorted_ls.insert(0, attr)
        else:
            sorted_ls.append(attr)
    for item in sorted_ls:  # dictionary with list indices as keys
        sorted_dict[str(sorted_ls.index(item))] = item
    return sorted_dict


def set_constants(constants: dict = None):
    """input previous set constants"""
    if constants is None:
        constants_dict = {}
    else:
        constants_dict = constants
    while True:
        constants_ls = []
        print('\nSelect Constant Attribute Labels')
        for i, attr in enumerate(ALL_LABELS):
            if attr in constants_dict:
                constants_ls.append(attr)
                print(f'[{i}] {attr}: {constants_dict[attr]}')  # show constants that have been set
            else:
                constants_ls.append(attr)
                print(f'[{i}] {attr}')
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
        print(f'\n{attr_sel}:')
        for j, label in enumerate(ALL_LABELS[attr_sel]):
            print(f'[{j}] {label}')
        print('[n] None')
        new_label_i = input('\nSelect a Label: ')

        if new_label_i == 'n':
            new_label = None
        elif new_label_i.isnumeric():
            if len(ALL_LABELS[attr_sel]) <= int(new_label_i):
                print('invalid input')
                continue
            else:
                new_label = ALL_LABELS[attr_sel][int(new_label_i)]
        else:
            print('invalid input')
            continue 
        constants_dict[attr_sel] = new_label
    for key in ALL_LABELS:  # set everything else to None
        if key not in constants_dict:
            constants_dict[key] = None
    return constants_dict


def edit_label(attr):
    while True:
        print('\nLabels for', attr)
        for i, label in enumerate(ALL_LABELS[attr]):
            print(f'[{i}] {label}')
        new_label_i = input('Select New Label: ')
        if new_label_i.isnumeric():
            if int(new_label_i) >= len(ALL_LABELS[attr]):  # if out of range
                print('invalid input')
                continue
            else:
                new_label = ALL_LABELS[attr][int(new_label_i)]
                return new_label
        else:
            print('invalid input')


def restore_vid(prev_data_obj: DataObject, from_dir: str, to_dir: str):
    from_path = os.path.join(from_dir, prev_data_obj.fname)
    to_path = os.path.join(to_dir, prev_data_obj.prev_fname)
    os.rename(from_path, to_path)
    prev_data_obj.fname = prev_data_obj.prev_fname
    prev_data_obj.prev_fname = None
    if prev_data_obj.has_joints:
        from_path_joints = os.path.join(from_dir, prev_data_obj.fname_joints)
        to_path_joints = os.path.join(to_dir, prev_data_obj.prev_fname_joints)
        os.rename(from_path_joints, to_path_joints)
        prev_data_obj.fname_joints = prev_data_obj.prev_fname_joints
        prev_data_obj.prev_fname_joints = None


def preview(data_dir):
    videos = [f for f in os.listdir(data_dir) if not f.startswith('._') and (f.endswith('.avi') or f.endswith('.mp4'))]
    i = 0
    while i < len(videos):
        cv2.destroyAllWindows()
        fpath_vid = os.path.join(data_dir, videos[i])
        play_vid(fpath_vid, playback_delay=10)
        # Function should start here
        while True:
            usr_inp = input('Previewing Data\n[enter] replay\n[a] previous video\n[d] next video\n[q] exit preview\n:')
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


def label_data(labeled_dir, data_dir, csv_path):
    labeled_count = 0
    constants = None  # initialize with no constants
    videos = [f for f in os.listdir(data_dir) if not f.startswith('._') and (f.endswith('.avi') or f.endswith('.mp4'))]
    data_objs = []
    i = 0
    while i < len(videos):
        cv2.destroyAllWindows()
        fname_vid = videos[i]
        fpath_vid = os.path.join(data_dir, fname_vid)
        if not os.path.exists(fpath_vid):
            print(f'video no longer exists as {fpath_vid}\nlook in {labeled_dir}')
            i += 1
            continue

        is_bad_video = play_vid(fpath_vid, playback_delay=50)
        if is_bad_video:
            i += 1
            continue
        data_obj = DataObject(file_name=fname_vid, root_dir=data_dir, labels_path=csv_path, constants=constants)
        opts_dict = {'[exit]': 'exit',
                     '[enter]': 'replay',
                     '[p]': 'preview videos',
                     '[c]': 'set constant labels',
                     '[z]': 'undo',
                     '[b]': 'bad',
                     '[q]': 'questionable',
                     '[f]': 'confirm labels'
                     }
        new_labels = {}
        while True:  # GUI Loop
            print(f'\nVIDEOS LABELED: {labeled_count}\n')
            print('\nOPTIONS\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            for opt in opts_dict:
                print(opt, opts_dict[opt])
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(f'\nCLASS: {data_obj.classID}\nFILE NAME: {data_obj.fname}\nHAS JOINTS: {data_obj.has_joints}\n')
            print('CURRENT LABELS\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            sorted_attrs = sort_attrs(data_obj)
            attr_labels = vars(data_obj)
            for index in sorted_attrs:
                print(f'[{index}] {sorted_attrs[index]}: {attr_labels[sorted_attrs[index]]}')  # [1] classID: Standing
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            x = input('\nAttribute to Edit: ')
            if not x:  # replay
                play_vid(fpath_vid, playback_delay=50)
            elif x == 'p':  # preview
                preview(data_dir)
                break
            elif x == 'b':
                for i in range(len(SAVED_CAPTIONS)):
                    print(f'[{i}] {SAVED_CAPTIONS[i]}')
                bad_info = input('\nNote on why its bad: ')
                if bad_info.isnumeric():
                    try:
                        quest_info = SAVED_CAPTIONS[int(bad_info)]
                    except IndexError:
                        print('invalid input')
                        break
                else:
                    SAVED_CAPTIONS.append(bad_info)
                data_obj.is_bad(bad_info)
            elif x == 'q':
                for i in range(len(SAVED_CAPTIONS)):
                    print(f'[{i}] {SAVED_CAPTIONS[i]}')
                quest_info = input('\nNote on why its questionable: ')
                if quest_info.isnumeric():
                    try:
                        quest_info = SAVED_CAPTIONS[int(quest_info)]
                    except IndexError:
                        print('invalid input')
                        break
                else:
                    SAVED_CAPTIONS.append(quest_info)
                data_obj.is_quest(quest_info)
            elif x == 'c':
                constants = set_constants(constants)  # initializes/updates constants
                break
            elif x == 'f':
                confirm = input('Are you sure?[y/n]: ')
                if confirm == 'y':
                    data_obj.re_name(data_dir, labeled_dir)  # rename files & put them into labeled_data
                    data_objs.append(data_obj)  # append object for accessing later
                    data_obj.output_to_csv(labels_path=csv_path)
                    i += 1
                    labeled_count += 1
                    break
                else:
                    continue
            elif x == 'z':
                if len(data_objs) > 0:
                    restore_vid(data_objs[-1], labeled_dir, data_dir)  # restores previous file to original filename & path
                    # restored = True
                    i -= 1
                    labeled_count -= 1
                    break
                else:
                    print('no data sorted yet')
                    break
            elif x == 'exit':
                return

            elif x in sorted_attrs.keys():
                # quest_info and bad_info should not be edited without the setter method
                if sorted_attrs[x] == 'quest_info':
                    print(f'\npress [q] to edit quest_info\n')
                    continue
                elif sorted_attrs[x] == 'bad_info':
                    print(f'\npress [b] to edit bad_info\n')
                    continue

                new_labels[sorted_attrs[x]] = edit_label(sorted_attrs[x])
                if constants:
                    set_labels = constants.copy()
                    set_labels.update(new_labels)   # merge new labels into a temporary dictionary
                    data_obj.set_labels(set_labels)   # update attributes in object
                else:
                    set_labels = {}
                    set_labels.update(new_labels)
                    data_obj.set_labels(set_labels)
            else:
                print('invalid input')
                continue


def resize_img(img, size, offset=0):
    img = imutils.resize(img, height=size)
    y, x = img.shape[0], img.shape[1]
    x_center = int(x/2 + offset)
    y_center = int(y/2)  
    img = img[(y_center-size//2):(y_center+size//2), (x_center-size//2):(x_center+size//2)]
    return img


def play_vid(fpath, playback_delay):
    cap = cv2.VideoCapture(fpath)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get frame count to make sure it is a 30 frame example
    if frame_count != 30:
        print('Video is NOT 30 frames')
        bad_video = True
        return bad_video
    if not cap.isOpened():
        print('Could NOT display video')
        bad_video = True
        return bad_video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = resize_img(frame, 256)
            cv2.imshow(fpath, frame)
        else:
            break
        cv2.waitKey(playback_delay)
    cap.release()


def main():
    while True:
        dir_name = input('Directory to sort from:')
        dir_path = os.path.join(os.getcwd(), dir_name)
        if not os.path.isdir(dir_path):
            print(f'{dir_name} is not a directory\n')
            continue
        labeled_name = input('Create/Select a labeled data folder: CurrentDir/')
        labeled_path = os.path.join(os.getcwd(), labeled_name)
        if not os.path.exists(labeled_path):
            try:
                os.mkdir(labeled_path)
            except FileNotFoundError:
                print(f'{labeled_path} is not a valid path')
                continue
        csv_fname = input('Create/Select a labels csv file: CurDir/')
        csv_fpath = os.path.join(os.getcwd(), csv_fname)
        label_data(labeled_path, dir_path, csv_fpath)
        while True:
            inp = input('\n[s] keep sorting\n[q] exit\n:')
            if inp == 's':
                break
            elif inp == 'q':
                sys.exit()
            else:
                print('\ninvalid input\n')
                continue


if __name__ == '__main__':
    main()
