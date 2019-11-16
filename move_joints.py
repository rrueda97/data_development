import os


def move_joints(from_path, to_path):
    vid_list = os.listdir(to_path)
    for f in vid_list:
        if f.startswith('._'): 
            vid_list.remove(f)
            continue
        if not (f.endswith('.avi') or f.endswith('.mp4')):
            vid_list.remove(f)
    print('finding joints for ', len(vid_list), ' videos')
    all_joints = os.listdir(from_path)
    for file in all_joints:
        if file.startswith('._'):
            all_joints.remove(file)
            continue
        if not file.endswith('.tensor'):
            all_joints.remove(file)
    print('looking through', len(all_joints), 'joints files')
    i = 0
    #print(vid_list)
    for joints in all_joints:
        vid_avi = joints[:-len('_joints.tensor')]+'.avi'
        vid_mp4 = joints[:-len('_joints.tensor')] + '.mp4'
        if (vid_mp4 in vid_list) or (vid_avi in vid_list):
            i += 1
            os.rename(os.path.join(from_path, joints), os.path.join(to_path, joints))
    print('found ', i)


if __name__ == '__main__':
    root = os.getcwd()
    from_name = input('Move Joints From: ')
    to_name = input('To: ')
    from_folder = os.path.join(root, from_name)
    to_folder = os.path.join(root, to_name)
    move_joints(from_folder, to_folder)
