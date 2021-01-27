import os
import boto3
import cv2
import shutil
from tqdm import tqdm

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


def pull_classification(filename: str):
    table = dynamodb.Table('ClassificationBylivedevicepersoncaptureFilename')
    try:
        get_response = table.get_item(Key={'filename': filename})
        if 'Item' in get_response:
            classification_dict = get_response['Item']
        else:
            classification_dict = None
    except Exception as e:
        print(e)
        return None
    return classification_dict

def already_sorted(sorted_data_path):
    imgs = []
    for dir in os.listdir(sorted_data_path):
        dir_path = os.path.join(sorted_data_path, dir)
        if not os.path.isdir(dir_path):
            continue
        for f in os.listdir(dir_path):
            if f.endswith('.png'):
                imgs.append(f)
    return imgs

def main(data_path: str, sorted_data_path: str):
    if not os.path.exists(sorted_data_path):
        os.mkdir(sorted_data_path)
    print(f'sorting data into {sorted_data_path}...')
    sorted_files = already_sorted(sorted_data_path)
    for fname in tqdm(os.listdir(data_path)):
        if not fname.endswith('.png'):
            continue
        if fname in sorted_files:
            continue
        classification = pull_classification(fname)
        if classification is None:
            continue
        try:
            boxes = [[int(coord) for coord in classification['box']]]
        except TypeError:
            boxes = []
            for bx in classification['box']:
                boxes.append([int(coord) for coord in bx][:4])
        except KeyError:
            continue
        cls = classification['classification']
        cls_path = os.path.join(sorted_data_path, cls)
        if not os.path.exists(cls_path):
            os.mkdir(cls_path)
        img_path = os.path.join(cls_path, fname)
        box_path = img_path[:-len('.png')]+'.txt'
        with open(box_path, mode='a+') as bf:
            for bx in boxes:
                box_str = str(bx).strip('[')
                box_str = box_str.strip(']')
                bf.write(box_str + '\n')
        shutil.copy(os.path.join(data_path, fname), img_path)


def sort_imgs(dir_path):
    print(f'Sorting from {dir_path}...\n\nif mislabeled, sort into the following directories:')
    print('[1] sit\n[2] stand\n[3] in bed\n[4] empty\n[esc] continue')
    for f in os.listdir(dir_path):
        if not f.endswith('.png'):
            continue
        img_path = os.path.join(dir_path, f)
        det_path = img_path[:-len('.png')] + '.txt'
        key_press = show_img(img_path, det_path)
        if key_press == 27:  # ESC key
            continue
        elif key_press == 49: # 1: sit
            label = 'sit'
        elif key_press == 50:  # 2: stand
            label = 'stand'
        elif key_press == 51:  # 3: in bed
            label = 'in bed'
        elif key_press == 52:  # 4: empty
            label = 'empty'
        elif key_press == 53:  # 5: sit-stand
            label = 'sit-stand'
        else:
            raise TypeError('entered invalid key stroke')
        move_data(label, img_path, det_path)


def move_data(new_dir_name, img_path, detection_path):
    new_dir = os.path.join(os.path.dirname(img_path), new_dir_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    os.rename(img_path, os.path.join(new_dir, os.path.basename(img_path)))
    os.rename(detection_path, os.path.join(new_dir, os.path.basename(detection_path)))


def show_img(img_path, detection_path):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]  # B, G, R, blk
    detections = []
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    with open(detection_path, mode='r') as b:
        boxes = b.readlines()
        for box_str in boxes:
            box_str = box_str.strip('\n')
            if len(box_str) > 0:
                detections.append([float(num) for num in box_str.split(',')])
    for i, detection in enumerate(detections):
        start = (int(detection[0]), int(detection[1]))
        end = (int(detection[2]), int(detection[3]))
        thickness = 5
        img = cv2.line(img, start, end, colors[i], thickness)
    cv2.imshow('sort image', img)
    k = cv2.waitKey(0)
    return k

def get_data_dictionary(data_path):
    """returns a dictionary with different class names as keys and lists of image and box file names"""
    # todo: sort original images by datetime, excess data = newest data
    data_dict = {}
    for dir in os.listdir(data_path):
        dir_path = os.path.join(data_path, dir)
        if not os.path.isdir(dir_path):
            continue
        imgs = [f for f in os.listdir(dir_path) if f.endswith('.png')]
        boxes = [img[:-len('.png')] + '.txt' for img in imgs]
        data_dict[dir] = {'imgs': imgs, 'boxes': boxes}
    return data_dict

def split_data(percent_holdout: float, train_set_path: str):
    """creates a validation set from an existing training set of data"""

    data_dict = get_data_dictionary(train_set_path)
    min_class_size = min([len(data_dict[cls]['imgs']) for cls in data_dict])
    print(f"Trimming Data to N = {min_class_size/2}...")
    # trim excess data
    excess_data_dict = {cls: {'imgs': data_dict[cls]['imgs'][min_class_size:],
                              'boxes': data_dict[cls]['boxes'][min_class_size:]}
                        for cls in data_dict}
    excess_data_path = os.path.join(os.path.dirname(train_set_path), 'excess_data')
    if not os.path.exists(excess_data_path):
        os.mkdir(excess_data_path)
    for cls in excess_data_dict:
        class_dir = os.path.join(excess_data_path, cls)
        if not os.path.exists(class_dir):
            os.mkdir(class_dir)
        for i in range(len(excess_data_dict[cls]['imgs'])):
            src_path_img = os.path.join(train_set_path, cls, excess_data_dict[cls]['imgs'][i])
            os.rename(src_path_img, os.path.join(class_dir, excess_data_dict[cls]['imgs'][i]))
            src_path_box = os.path.join(train_set_path, cls, excess_data_dict[cls]['boxes'][i])
            os.rename(src_path_box, os.path.join(class_dir, excess_data_dict[cls]['boxes'][i]))

    holdout_idx = int(min_class_size * percent_holdout)
    print(f'Splitting Data into N_val = {holdout_idx/2} N_train = {(min_class_size - holdout_idx)/2}...')
    trimmed_data_dict = get_data_dictionary(train_set_path)
    val_data_dict = {cls: {'imgs': trimmed_data_dict[cls]['imgs'][:holdout_idx],
                           'boxes': trimmed_data_dict[cls]['boxes'][:holdout_idx]}
                     for cls in trimmed_data_dict}
    val_data_path = os.path.join(os.path.dirname(train_set_path), 'val_set')
    if not os.path.exists(val_data_path):
        os.mkdir(val_data_path)
    for cls in val_data_dict:
        class_dir = os.path.join(val_data_path, cls)
        if not os.path.exists(class_dir):
            os.mkdir(class_dir)
        for i in range(len(val_data_dict[cls]['imgs'])):
            src_path_img = os.path.join(train_set_path, cls, val_data_dict[cls]['imgs'][i])
            os.rename(src_path_img, os.path.join(class_dir, val_data_dict[cls]['imgs'][i]))
            src_path_box = os.path.join(train_set_path, cls, val_data_dict[cls]['boxes'][i])
            os.rename(src_path_box, os.path.join(class_dir, val_data_dict[cls]['boxes'][i]))

def check_sorted_data(data_path):
    data_dict = get_data_dictionary(data_path)
    for cls in data_dict:
        imgs = data_dict[cls]['imgs']
        boxes = data_dict[cls]['boxes']
        for i in range(len(imgs)):
            img_path = os.path.join(data_path, cls, imgs[i])
            try:
                assert os.path.exists(img_path)
            except AssertionError:
                print(img_path)
            box_path = os.path.join(data_path,cls, boxes[i])
            try:
                assert os.path.exists(box_path)
            except AssertionError:
                print(box_path)



if __name__ == '__main__':
    synced_data_path = '/Users/ricardorueda/Data/client1_november-2020'
    sorted_data_path = '/Users/ricardorueda/Data/client1_november-2020_sorted'
    main(synced_data_path, sorted_data_path)
    # imgs = [f for f in os.listdir(sorted_data_path) if f.endswith('.png')]
    # boxes = [img[:-len('.png')]+'.txt' for img in imgs]
    # for i in range(len(imgs)):
    #     img_path = os.path.join(sorted_data_path, imgs[i])
    #     box_path = os.path.join(sorted_data_path, boxes[i])
    #     k = show_img(img_path, box_path)
    #     if k == 27:
    #         os.rename(img_path, os.path.join(os.path.dirname(sorted_data_path), imgs[i]))
    #         os.rename(box_path, os.path.join(os.path.dirname(sorted_data_path), boxes[i]))
    # training_data_path = '/Users/ricardorueda/Data/NeuralNetData_client1_08-10_2020/train_set'
    # check_sorted_data(training_data_path)
    # split_data(percent_holdout=0.2, train_set_path=training_data_path)





