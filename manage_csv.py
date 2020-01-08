import csv
import os

def delete_empty_rows(file_path):
    with open(file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows_list = list(reader)
    fixed_rows_list = [row for row in rows_list if len(row)>0]
    with open(file_path[:-len('.csv')]+'_fixed.csv', mode='w') as fixed_csv_file:
        writer = csv.writer(fixed_csv_file)
        writer.writerows(fixed_rows_list)

def fix_csv(file_path):
    with open(file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows_list = list(reader)
    fixed_rows_list = [x[:24] for x in rows_list]
    with open(file_path[:-len('.csv')]+'_fixed.csv', mode='w') as fixed_csv_file:
        writer = csv.writer(fixed_csv_file)
        writer.writerows(fixed_rows_list)


def delete_duplicates(file_path, data_directory):
    files = os.listdir(data_directory)
    with open(file_path, mode='r') as inp, open(file_path[:-len('.csv')]+'_edit.csv', mode='w') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            try:
                if (row[0] in files):
                    writer.writerow(row)
                elif row[0] == 'fname':
                    writer.writerow(row)
            except IndexError:
                continue


def move_labeled(file_path, data_directory):
    files = os.listdir(data_directory)
    labeled_path = os.path.join(data_directory,'already_labeled')
    if not os.path.exists(labeled_path):
        os.mkdir(labeled_path)
    with open(file_path, mode='r') as inp:
        for row in csv.reader(inp):

            if row[19] == 'prev_fname':
                continue
            elif row[19] in files:
                from_path = os.path.join(data_directory,row[19])
                to_path = os.path.join(labeled_path,row[19])
                from_path_joints = os.path.join(data_directory,row[20])
                to_path_joints = os.path.join(labeled_path, row[20])
                os.rename(from_path, to_path)
                os.rename(from_path_joints, to_path_joints)

def print_double_prev(file_path):
    prev_fnames = []
    with open(file_path, mode='r') as inp:
        for row in csv.reader(inp):
            prev_fnames.append(row[19])
    for name in prev_fnames:
        if prev_fnames.count(name) > 1:
            print(name)

def compare_vid_csv(file_path, data_directory):
    data = os.listdir(data_directory)
    vids = [file for file in data if file.endswith('.avi')]
    labels = []
    with open(file_path, mode='r') as inp:
        for row in csv.reader(inp):
            if row[0] == 'fname':
                continue
            else:
                labels.append(row[0])
    if len(vids)>len(labels):
        print('more videos than labels')
        for vid in vids:
            if vid not in labels:
                # quick move
                # to_dir = os.path.join(os.getcwd(),'Rolling_Bed/unclear_labels')
                # os.rename(os.path.join(data_directory,vid), os.path.join(to_dir, vid))
                # os.rename(os.path.join(data_directory,vid[:-len('.avi')]+'_joints.tensor'), os.path.join(to_dir, vid[:-len('.avi')]+'_joints.tensor'))
                print(vid)
    elif len(labels)>len(vids):
        print('more labels than videos')
        for label in labels:
            if label not in vids:
                print(label)
    elif len(labels)==len(vids):
        gucci = True
        for label in labels:
            if label not in vids:
                gucci = False
        if gucci:
            print('All Good')
    print('Final Report')
    print('    label entries:',len(labels))
    print('    video entries:', len(vids))


def filter_bad():
    csv_dir = input('Path to csv file:')
    data_dir = input('Path to labeled data:')
    csv_path = os.path.join(os.getcwd(), csv_dir)
    data_path = os.path.join(os.getcwd(), data_dir)
    filtered_path = os.path.join(data_path,'filtered_data')
    if not os.path.exists(filtered_path):
        os.mkdir(filtered_path)
    filtered_rows = []
    with open(csv_path, mode='r') as f:
        for row in csv.reader(f):
            if (row[17] == 'True') or (row[18] == 'True'):
                fname_vid = row[0]
                fname_joints = fname_vid[:-len('.avi')]+'_joints.tensor'
                print(fname_vid)
                os.rename(os.path.join(data_path, fname_vid), os.path.join(filtered_path, fname_vid))
                os.rename(os.path.join(data_path, fname_joints), os.path.join(filtered_path, fname_joints))
            else:
                filtered_rows.append(row)
    with open(csv_path[:-len('.csv')]+'_filtered.csv', mode='w') as filtered:
        writer = csv.writer(filtered)
        writer.writerows(filtered_rows)


def merge_csv():
    inp = input('Path to folder with csv files: CurrentDir/')
    merge_path = os.path.join(os.getcwd(),inp)
    merged_rows =[]
    csv_list = os.listdir(merge_path)
    for i, csv_file in enumerate(csv_list):
        csv_path = os.path.join(merge_path,csv_file)
        with open(csv_path, mode='r') as f:
            for j, row in enumerate(csv.reader(f)):
                if j == 0:  # header
                    if i == 0:
                        merged_rows.append(row)
                    else:
                        continue
                else:
                    merged_rows.append(row)
    merged_csv_path = os.path.join(merge_path,'merged.csv')
    with open(merged_csv_path, mode='w', newline='') as m:
        writer = csv.writer(m)
        writer.writerows(merged_rows)


def get_count():
    inp = input('Path to csv file: CurrentDir/')
    csv_path = os.path.join(os.getcwd(),inp)
    falling_RRueda = 0
    falling_ATam = 0
    falling_ATwombly = 0
    sitting_RRueda = 0
    sitting_ATam = 0
    sitting_ATwombly = 0
    standing_RRueda = 0
    standing_ATam = 0
    standing_ATwombly = 0
    rollingBed_RRueda = 0
    rollingBed_ATam = 0
    rollingBed_ATwombly = 0
    stillBed_RRueda = 0
    stillBed_ATam = 0
    stillBed_ATwombly = 0
    rollingGround_RRueda = 0
    rollingGround_ATam = 0
    rollingGround_ATwombly = 0
    stillGround_RRueda = 0
    stillGround_ATam = 0
    stillGround_ATwombly = 0
    with open(csv_path, mode='r') as f:
        for row in csv.reader(f):
            action = row[2]
            person = row[3]
            bad = row[17]
            quest = row[19]
            if (bad == 'False' or bad =='FALSE') and (quest == 'False' or quest =='FALSE'):
                if action == 'Falling':
                    if person == 'VBaena':
                        falling_RRueda += 1
                    elif person == 'ATam':
                        falling_ATam += 1
                    elif person == 'ATwombly':
                        falling_ATwombly += 1
                elif action == 'SittingUp':
                    if person == 'VBaena':
                        sitting_RRueda += 1
                    elif person == 'ATam':
                        sitting_ATam += 1
                    elif person == 'ATwombly':
                        sitting_ATwombly += 1
                elif action == 'Standing':
                    if person == 'VBaena':
                        standing_RRueda += 1
                    elif person == 'ATam':
                        standing_ATam += 1
                    elif person == 'ATwombly':
                        standing_ATwombly += 1
                elif action == 'RollingBed':
                    if person == 'VBaena':
                        rollingBed_RRueda += 1
                    elif person == 'ATam':
                        rollingBed_ATam += 1
                    elif person == 'ATwombly':
                        rollingBed_ATwombly += 1
                elif action == 'StillBed':
                    if person == 'VBaena':
                        stillBed_RRueda += 1
                    elif person == 'ATam':
                        stillBed_ATam += 1
                    elif person == 'ATwombly':
                        stillBed_ATwombly += 1
                elif action == 'RollingGround':
                    if person == 'VBaena':
                        rollingGround_RRueda += 1
                    elif person == 'ATam':
                        rollingGround_ATam += 1
                    elif person == 'ATwombly':
                        rollingGround_ATwombly += 1
                elif action == 'StillGround':
                    if person == 'VBaena':
                        stillGround_RRueda += 1
                    elif person == 'ATam':
                        stillGround_ATam += 1
                    elif person == 'ATwombly':
                        stillGround_ATwombly += 1
    print('Falling:\n    VBaena: '+str(falling_RRueda)+'\n    ATam: '+str(
        falling_ATam)+'\n    ATwombly: '+str(falling_ATwombly))
    print('Sitting Up:\n    VBaena: ' + str(sitting_RRueda) + '\n    ATam: ' + str(
        sitting_ATam) + '\n    ATwombly: ' + str(sitting_ATwombly))
    print('Standing:\n    VBaena: ' + str(standing_RRueda) + '\n    ATam: ' + str(
        standing_ATam) + '\n    ATwombly: ' + str(standing_ATwombly))
    print('Rolling Bed:\n    VBaena: ' + str(rollingBed_RRueda) + '\n    ATam: ' + str(
        rollingBed_ATam) + '\n    ATwombly: ' + str(rollingBed_ATwombly))
    print('Still Bed:\n    VBaena: ' + str(stillBed_RRueda) + '\n    ATam: ' + str(
        stillBed_ATam) + '\n    ATwombly: ' + str(stillBed_ATwombly))
    print('Rolling Ground:\n    VBaena: ' + str(rollingGround_RRueda) + '\n    ATam: ' + str(
        rollingGround_ATam) + '\n    ATwombly: ' + str(rollingGround_ATwombly))
    print('Still Ground:\n    VBaena: ' + str(stillGround_RRueda) + '\n    ATam: ' + str(
        stillGround_ATam) + '\n    ATwombly: ' + str(stillGround_ATwombly))



if __name__ == '__main__':
    # csv_dir = input('Path to csv file:')
    # data_dir = input('Path to labeled data:')
    # csv_path = os.path.join(os.getcwd(), csv_dir)
    # data_path = os.path.join(os.getcwd(), data_dir)
    # move_labeled(csv_path, data_path)
    # print_double_prev(csv_path)
    # compare_vid_csv(csv_path,data_path)
    # delete_empty_rows(csv_path)
    # merge_csv()
    # filter_bad()
    get_count()