import numpy as np
import os
import cv2

def restore_file(from_dir, to_dir, file_name):
    try:
        os.rename(os.path.join(from_dir, file_name), os.path.join(to_dir, file_name))
        return True
    except:
        return False


def main(root_dir):
    files = os.listdir(root_dir)
    del_dir = os.path.join(root_dir, 'bad_examples')
    save_dir = os.path.join(root_dir, 'good_examples')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if not os.path.exists(del_dir):
        os.mkdir(del_dir)
    i=0
    while i < len(files):
        try:
            f = files[i]
            if '.avi' not in f:
                continue
            file_path = os.path.join(root_dir, f)
            cap = cv2.VideoCapture(file_path)
            print(i, f)
            j = 0
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('frame',frame)
                else:
                    break
                cv2.waitKey(10)


            cap.release()
            cv2.destroyAllWindows()
            inp = input('delete? [d] replay previous? [r]')
            if inp == 'd':
                os.rename(file_path, os.path.join(del_dir, f))
            elif inp == 'r':
                    in_saved, in_del = restore_file(save_dir, root_dir, files[i-1]), restore_file(del_dir, root_dir, files[i-1])
                    if in_saved or in_del:
                        i-=1
                        continue
            elif inp == 'a':
                check_file = files[i];
                root_name = check_file[:27]
                for file in files:
                    if file.find(root_name) > -1:
                        file_path2 = os.path.join(root_dir, file)
                        print(restart_index, file)
                        os.rename(file_path2, os.path.join(del_dir, file))
                        if file[27] > check_file[27]:
                            i += 1
            else:
                os.rename(file_path, os.path.join(save_dir, f))
        except Exception as e:
            raise
            print(e)

        i += 1

if __name__ == '__main__':
    root_dir = os.getcwd()
    print(root_dir)
    main(root_dir)
