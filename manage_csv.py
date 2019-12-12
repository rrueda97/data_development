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
            if (row[17] == 'TRUE') or (row[18] == 'TRUE'):
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
    filter_bad()