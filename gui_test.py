import curses
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
