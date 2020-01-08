import csv
import os
import shutil
import matplotlib.pyplot as plt


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


def visualize_attr(attribute, labels_path):
    all_labels = labels_dict[attribute]  # list of labels
    x = list(range(0,len(all_labels)))
    x_class = list(range(0,len(classID_labels)))
    labels = {}
    all_classes = {}
    y_classes = {}
    for action in classID_labels:
        with open(labels_path, mode='r', newline='', encoding='utf-8') as labels_file:
            reader = csv.DictReader(labels_file)
            action_labels = [row[attribute] for row in reader if row['classID'] == action]
            labels[action] = action_labels
            all_classes[action] = len(action_labels)
            y_classes[action] = [action_labels.count(label) for label in all_labels]

    fig, axes = plt.subplots(2,4, sharey='all')
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.90, wspace=0.10, hspace=0.80)
    fig.suptitle(attribute)
    axes[0, 0].set_title('Total')
    axes[0, 0].bar(x_class, [all_classes[i] for i in classID_labels])
    axes[0, 0].set_xticks(x_class)
    axes[0, 0].set_xticklabels(classID_labels, rotation=90)
    axes[1, 0].set_title('Sitting Up')
    axes[1, 0].bar(x, y_classes['SittingUp'])
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(all_labels)
    axes[0, 1].set_title('Falling')
    axes[0, 1].bar(x, y_classes['Falling'])
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(all_labels)
    axes[0, 2].set_title('Still on Bed')
    axes[0, 2].bar(x, y_classes['StillBed'])
    axes[0, 2].set_xticks(x)
    axes[0, 2].set_xticklabels(all_labels)
    axes[0, 3].set_title('Rolling on Bed')
    axes[0, 3].bar(x, y_classes['RollingBed'])
    axes[0, 3].set_xticks(x)
    axes[0, 3].set_xticklabels(all_labels)
    axes[1, 1].set_title('Standing')
    axes[1, 1].bar(x, y_classes['Standing'])
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(all_labels)
    axes[1, 2].set_title('Still on Ground')
    axes[1, 2].bar(x, y_classes['StillGround'])
    axes[1, 2].set_xticks(x)
    axes[1, 2].set_xticklabels(all_labels)
    axes[1, 3].set_title('Rolling on Ground')
    axes[1, 3].bar(x, y_classes['RollingGround'])
    axes[1, 3].set_xticks(x)
    axes[1, 3].set_xticklabels(all_labels)
    plt.show()


def generate_data():
    # returns data set in folder and associated file with stats
    # Labels From sort-data.py
    N = 126
    count_dict = {}
    classID_labels = ['Falling', 'SittingUp', 'Standing', 'StillGround', 'StillBed', 'RollingGround', 'RollingBed']
    persons = ['ATam', 'ATwombly']
    for person in persons:
        count_dict[person] = {}
        for action in classID_labels:
            count_dict[person][action] = 0

    csv_path = input('Path to labels csv: CurDirectory/')
    labeled_data_path = input('Path to labeled data folder: CurDirectory/')
    new_dataset_path = input('Path to generated dataset folder: CurDirectory/')
    if not os.path.exists(new_dataset_path):
        os.mkdir(new_dataset_path)

    with open(csv_path, mode='r', newline='', encoding='utf-8') as labels_file, open(new_dataset_path+'/dataset_labels.csv', mode='w', newline='', encoding='utf-8') as new_csv:
        reader = csv.DictReader(labels_file)
        writer = csv.DictWriter(new_csv, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if (row['bad'] == 'TRUE') or (row['bad'] == 'True') or (row['questionable'] == 'TRUE') or (row['questionable'] == 'True'):
                continue

            class_label = row['classID']
            person_label = row['personID']
            video_file = row['fname']
            joints_file = row['fname_joints']


            if (class_label in classID_labels) and (person_label in persons):
                if count_dict[person_label][class_label] < N:
                    count_dict[person_label][class_label] += 1  # update count in dictionary
                    writer.writerow(row)
                    from_vid_path = os.path.join(labeled_data_path, video_file)
                    from_joints_path = os.path.join(labeled_data_path, joints_file)
                    to_vid_path = os.path.join(new_dataset_path, video_file)
                    to_joints_path = os.path.join(new_dataset_path, joints_file)
                    shutil.copyfile(from_vid_path, to_vid_path)
                    shutil.copyfile(from_joints_path, to_joints_path)
            else:
                continue
    print('Final Count:')
    print('    ATam:')
    for key in count_dict['ATam']:
        print('        '+str(key)+': '+str(count_dict['ATam'][key]))
    print('    ATwombly:')
    for key in count_dict['ATwombly']:
        print('        ' + str(key) + ': ' + str(count_dict['ATwombly'][key]))



def main():
    file_path = input('Path to labels csv: ')
    with open(file_path, mode='r', newline='', encoding='utf-8') as labels_csv:
        reader = csv.DictReader(labels_csv)
        attrs = [x for x in reader.fieldnames if x not in ['fname','has_joints','classID','bad','bad_info','quest_info'
                 ,'questionable','prev_fname','prev_fname_joints', 'fname_joints']]
    while True:
        print('\nSelect attribute to visualize\n')
        for i, attr in enumerate(attrs):
            print('['+str(i)+'] '+str(attr))
        selection = input(':')
        visualize_attr(attrs[int(selection)], file_path)


if __name__ == '__main__':
    main()








