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


if __name__ == '__main__':
    synced_data_path = '/Users/ricardorueda/Data/livedevicepersoncapture_client1'
    sorted_data_path = '/Users/ricardorueda/Data/livedevicepersoncapture_client1_sorted'
    main(data_path=synced_data_path,
         sorted_data_path=sorted_data_path)
    # for dir in os.listdir(sorted_data_path):
    #     dir_path = os.path.join(sorted_data_path, dir)
    #     if not os.path.isdir(dir_path):
    #         continue
    #     sort_imgs(dir_path)


