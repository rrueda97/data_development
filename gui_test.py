import curses
import os
import time
from label_data import DataObject

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
displace_labels = ['front', 'back', 'left', 'right', 'clockwise', 'counterclockwise']
ALL_LABELS = {'classID': classID_labels, 'personID': personID_labels, 'roomID': roomID_labels, 'camID': camID_labels,
              'splitNum': splitNum_labels, 'position': position_labels, 'clothing': clothing_labels,
              'gender': gender_labels, 'displacement': displace_labels}
ALL_LABELS.update(dict.fromkeys(['skinTone', 'lighting', 'roomInfo', 'zoom', 'vidSpeed', 'variance'], descrip_labels))
features = [f for f in ALL_LABELS]


class ConsoleDisplay:
    """object class controlling displays to console"""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.feature_cursor_pos = 0
        self.label_cursor_pos = 0
        self.feature_selected = True
        self.label_selected = False
        ignored_features = ['fname', 'prev_fname', 'has_joints', 'prev_fname_joints', 'fname_joints', 'bad',
                            'questionable']
        self.feature_label_dict = {f: ALL_LABELS[f] for f in ALL_LABELS if f not in ignored_features}
        self.cons_h, self.cons_w = stdscr.getmaxyx()
        self.current_feature = None
        curses.use_default_colors()
        curses.curs_set(0)  # cursor blinking?
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)

    def run_display(self, data_obj):
        """method to show display"""
        menu_options = 'OPTIONS\n%%%%%%%%%%%%\n[f] confirm labels\n[c] set constant labels\n[z] undo\n[b] bad video\n' \
                       '[q] questionable video\n[r] replay video'
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, menu_options)
            self.current_feature = self.display_data_features(data_obj)
            self.stdscr.refresh()
            key_press = self.stdscr.getch()
            if key_press == curses.KEY_ENTER:
                if self.feature_selected is False:
                    self.feature_selected = True
                elif self.feature_selected is True and self.label_selected is False:  # pressed enter on a label
                    self.label_selected = True
            if self.feature_selected is False:  # only controls up/down features
                if key_press == curses.KEY_UP and self.feature_cursor_pos > 0:
                    self.feature_cursor_pos -= 1
                elif key_press == curses.KEY_DOWN and self.feature_selected < len(self.feature_label_dict):
                    self.label_cursor_pos += 1
            if self.feature_selected is True:
                if key_press == curses.KEY_UP and self.label_cursor_pos > 0:
                    self.label_cursor_pos -= 1
                elif key_press == curses.KEY_DOWN and self.feature_selected < len(self.feature_label_dict[self.current_feature]):
                    self.label_cursor_pos += 1

    def display_data_features(self, data_obj: DataObject):
        """displays the features and labels of a data object"""
        data_title = f'CLASS: {data_obj.classID}\nFILENAME: {data_obj.fname}\nHAS JOINTS: {data_obj.has_joints}'
        data_title_x = 0
        data_title_y = 10  # mess with this
        labels_column_x = 20
        self.stdscr.addstr(data_title_y, data_title_x, data_title)

        feature_highlighted = None
        for i, feature in enumerate(self.feature_label_dict):
            feature_text = f'{feature}: {data_obj[feature]}'
            if self.feature_cursor_pos == i:
                feature_highlighted = feature
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(data_title_y + i + 2, 0, feature_text)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(data_title_y + i + 2, 0, feature_text)
        if self.feature_selected is True and self.label_selected is False:
            feature_labels = self.feature_label_dict[feature_highlighted]
            for j, label in enumerate(feature_labels):
                if self.label_cursor_pos == j:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(data_title_y + j + 2, labels_column_x, label)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(data_title_y + j + 2, labels_column_x, label)
        return feature_highlighted














def main(stdscr):
    curr_feature_idx = 0
    curr_label_idx = 0
    feature_selected = False
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)  # selection color pair
    menu_options = 'OPTIONS\n%%%%%%%%%%%%\n[f] confirm labels\n[c] set constant labels\n[z] undo\n[b] bad video\n' \
                   '[q] questionable video\n[r] replay video'
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, menu_options)
        display_data_obj(stdscr, curr_feature_idx, feature_selected, curr_label_idx)
        key_press = stdscr.getch()
        if key_press == curses.KEY_UP:
            if feature_selected is True and curr_label_idx > 0:
                curr_label_idx -= 1
            elif curr_feature_idx > 0:
                curr_feature_idx -= 1
        elif key_press == curses.KEY_DOWN:
            if feature_selected is True and curr_label_idx < len(ALL_LABELS[feature]):
                curr_label_idx += 1
            elif curr_feature_idx < len(ALL_LABELS)-1:
                curr_feature_idx += 1
        elif key_press == curses.KEY_ENTER or feature_selected is False:
            feature_selected = True
            feature = list(ALL_LABELS.keys())[curr_feature_idx]
        elif key_press == curses.KEY_BACKSPACE:
            feature_selected = False
            curr_label_idx = 0
        stdscr.refresh()


def display_data_obj(stdscr, feature_idx: int, feature_sel: bool, label_idx):
    # ignored = ['fname', 'prev_fname', 'has_joints', 'prev_fname_joints', 'fname_joints', 'bad', 'questionable']
    menu_dict = ALL_LABELS
    y_bias = 13
    h, w = stdscr.getmaxyx()  # terminal h, w
    data_title = 'CLASS: \nFILENAME: \nHAS JOINTS: '
    stdscr.addstr(y_bias-3, 0, data_title)
    for i, key in enumerate(menu_dict):
        y = i + y_bias
        if i == feature_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, 0, key)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, 0, key)
        if feature_sel is True:
            for j, label in enumerate(menu_dict[key]):
                if j == label_idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, 15, label)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, 15, label)
    stdscr.refresh()



curses.wrapper(main)
