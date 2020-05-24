import cv2
import imutils
import os
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

class DataSet:
    """This class holds methods to manage mercury datasets"""
    def __init__(self, labels_path: str):
        if not os.path.exists(labels_path):
            raise FileExistsError(f'{labels_path} does not exist')
        self.labels_path = labels_path
        self.labels_df = None
        self.features = None
        self.cls_count = None
        self.classes = None
        self.load_df()

    def load_df(self):
        """reloads the datset .csv file into a dataframe and obtains updated attributes"""
        labels_df = pd.read_csv(self.labels_path)
        self.labels_df = labels_df.where(pd.notnull(labels_df), None)  # NaNs to None
        self.features = self.labels_df.columns  # an index object, iterable
        self.cls_count = self.labels_df['classID'].value_counts() # access as dictionary
        self.classes = [class_id for class_id in self.labels_df.classID.unique() if class_id is not None]

    def vis_feature(self, feature: str, cls: str = None, normalize: bool = True) -> plt.axes:
        """visualize the distribution of a feature for the whole dataset or for a certain class"""
        if feature not in self.features:
            raise ValueError(f'{feature} is not a feature of this dataset')
        if cls is not None:
            if cls not in self.classes:
                raise ValueError(f'{cls} is not a class of this dataset')
            cls_subset = self.labels_df[self.labels_df['classID'] == cls]
            feature_counts = cls_subset[feature].value_counts(normalize=normalize)
        else:
            feature_counts = self.labels_df[feature].value_counts(normalize=normalize)
        x_labels = feature_counts.index.to_list()
        ax = plt.axes()
        feature_counts.plot(kind='bar', ax=ax)
        ax.set_xticklabels(x_labels, rotation=0)
        if normalize:
            ax.set_ylabel('%')
        else:
            ax.set_ylabel('#')
        if cls is not None:
            ax.set_title(f'Distribution for {cls}')
        else:
            ax.set_title('Distribution for all classes')
        return ax

    def check_videos(self, video_dirs: list, move_to_dir: str = None):
        """method to check if there are videos not included in the dataset csv"""
        all_videos = []
        for directory in video_dirs:
            if not os.path.exists(directory):
                raise FileExistsError(f'{directory} does not exist')
            if not os.path.isdir(directory):
                raise NotADirectoryError(f'{directory} is not a directory')
            videos_in_dir = [f for f in os.listdir(directory) if f.endswith('.avi') or f.endswith('.mp4')]
            all_videos = all_videos + videos_in_dir

        videos_in_dataset = self.labels_df['fname'].to_list()
        prev_videos_in_dataset = self.labels_df['prev_fname'].to_list()
        not_in_dataset = list(set(all_videos) - set(videos_in_dataset)) #- set(prev_videos_in_dataset))
        not_in_dataset_paths = []
        for dir in video_dirs:
            for vid in not_in_dataset:
                if vid in os.listdir(dir):
                    not_in_dataset_paths.append(os.path.join(dir, vid))
        if move_to_dir is not None:
            if not os.path.exists(move_to_dir):
                os.mkdir(move_to_dir)
            for vid_path in not_in_dataset_paths:
                os.rename(vid_path, os.path.join(move_to_dir, os.path.basename(vid_path)))
        return not_in_dataset_paths


if __name__ == '__main__':
    csv_path = os.path.join(os.getcwd(), 'datasets/ricky_room_IR/ricky_room_IR_labels.csv')
    dataset = DataSet(csv_path)
    videos_path0 = os.path.join(os.getcwd(), 'datasets/ricky_room_IR/half_labeled')
    videos_path1 = os.path.join(os.getcwd(), 'datasets/ricky_room_IR/labeled')
    missed_videos_path = os.path.join(os.getcwd(), 'datasets/ricky_room_IR/not_in_csv')
    not_in_csv = dataset.check_videos([videos_path0, videos_path1], move_to_dir=missed_videos_path)
    #testing commit from new computer
    # hist_ax = dataset.vis_feature(feature='classID', normalize=False)


