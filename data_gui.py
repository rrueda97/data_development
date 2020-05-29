import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

def display_joints():
    # place holder for overlaying joints on video
    print('Joints displayed')

def display_radar():
    # placeholder for overlaying radar data on frame
    print('Radar displayed')



# root_win = tk.Tk()
# # GUI App Goes here
# mercury_blue = '#84C6FF'
# frame_blue = '#2E86C1'
# label_font = ('Century', 18)
# height = 720
# width = 1280
# canvas = tk.Canvas(root_win, height=height, width=width)
# canvas.pack()
#
# main_frame = tk.Frame(root_win, bg=mercury_blue)
# main_frame.place(relwidth=1, relheight=1)
# # ttk.Style().configure('green/black.TLabel', background='black')
# dataset_frame = tk.Frame(root_win, bg=frame_blue)
# dataset_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.18)
#
# video_frame = tk.Frame(root_win, bg=frame_blue)
# video_frame.place(relx=0.01, rely=0.20, relwidth=0.48, relheight=0.74)
#
# toggle_frame = tk.Frame(root_win, bg=frame_blue)
# toggle_frame.place(relx=0.01, rely=0.96, relwidth=0.48, relheight=0.03)
#
# datacount_frame = tk.Frame(root_win, bg=frame_blue)
# datacount_frame.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.18)
#
# features_frame = tk.Frame(root_win, bg=frame_blue)
# features_frame.place(relx=0.51, rely=0.20, relwidth=0.48, relheight=0.39)
#
# labels_frame = tk.Frame(root_win, bg=frame_blue)
# labels_frame.place(relx=0.51, rely=0.60, relwidth=0.48, relheight=0.39)
#
# from_dir_label = tk.Label(dataset_frame, text='FROM:', bg=frame_blue)
# from_dir_label.place(relx=0.01, rely=0.6)
#
# from_dir_entry = tk.Entry(dataset_frame, bg='white')
# from_dir_entry.place(relx=0.09, rely=0.6)
#
# to_dir_label = tk.Label(dataset_frame, text='TO:', bg=frame_blue)
# to_dir_label.place(relx=0.51, rely=0.6)
#
# to_dir_entry = tk.Entry(dataset_frame, bg='white')
# to_dir_entry.place(relx=0.56, rely=0.6)
#
# features_label = tk.Label(features_frame, text='FEATURES', bg=frame_blue, foreground='white', font=label_font)
# features_label.place(relx=0.01, rely=0.01)
#
# hist_label = tk.Label(features_frame, text='DISTRIBUTION', bg=frame_blue, foreground='white', font=label_font)
# hist_label.place(relx=0.6, rely=0.01)
#
# joints_toggle = ttk.Button(toggle_frame, text='JOINTS', command=lambda: display_joints())
# joints_toggle.place(relx=0.20)
# radar_toggle = ttk.Button(toggle_frame, text='RADAR', command=lambda: display_radar())
# radar_toggle.place(relx=0.60)
#
# root_win.mainloop()
