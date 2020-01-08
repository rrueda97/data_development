import csv
import os
import shutil


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


if __name__ == '__main__':
    generate_data()








