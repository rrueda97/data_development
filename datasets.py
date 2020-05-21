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

if __name__ == '__main__':
    csv_path = os.path.join(os.getcwd(), 'datasets/test_dataset/test_labels.csv')
    dataset = DataSet(csv_path)
    hist_ax= dataset.vis_feature(feature='classID', normalize=False)


