#     __                                    ___            __
#    /\ \__  __                            /\_ \    __    /\ \
#    \ \ ,_\/\_\    ___ ___      __    ____\//\ \  /\_\   \_\ \     __
#     \ \ \/\/\ \ /' __` __`\  /'__`\ /',__\ \ \ \ \/\ \  /'_` \  /'__`\
#      \ \ \_\ \ \/\ \/\ \/\ \/\  __//\__, `\ \_\ \_\ \ \/\ \L\ \/\  __/
#       \ \__\\ \_\ \_\ \_\ \_\ \____\/\____/ /\____\\ \_\ \___,_\ \____\
#        \/__/ \/_/\/_/\/_/\/_/\/____/\/___/  \/____/ \/_/\/__,_ /\/____/
#
#           a super-simple gui to slide old photographs into TODAY
#

# required for pyinstaller: pytorch
import os, sys
os.environ["PYTORCH_JIT"] = "0"

# to be used for dev vs bundled paths
try:
   wd = sys._MEIPASS
except AttributeError:
   wd = os.getcwd()
os.chdir(wd)

# set up delodify
from deoldify import device
from deoldify.device_id import DeviceId
device.set(device = DeviceId.GPU0)
from deoldify.visualize import *
torch.backends.cudnn.benchmark = True

# set up super-resolution
#import matplotlib.pyplot as plt
#from data import DIV2K
#from model.edsr import edsr
#from model.wdsr import wdsr_b, wdsr_a
#from model import resolve_single
#from utils import load_image, plot_sample

# set up image enhance
import cv2
from cv2 import dnn_superres

# import other modules
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import threading
from PIL import Image, ImageTk
import tensorflow as tf
import shutil
import os
import urllib.request
import io
import numpy as np
import time

# tooltip class
# CREDIT: https://stackoverflow.com/questions/3221956/
#         how-do-i-display-tooltips-in-tkinter
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # milliseconds
        self.wraplength = 240   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.hidetip()
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

# ef slider callback
value_list_lo = [2, 3, 4]
value_list_hi = [2, 4, 8]
def ef_slider_callback(value):
    if app.weights_vars.get() in "LapSRN":
        this_list = value_list_hi
    else:
        this_list = value_list_lo
    newvalue = min(this_list, key=lambda x:abs(x-float(value)))
    app.scale_ef.set(newvalue)

# ef model callback
def ef_weights_callback(value):
    if value in "LapSRN":
        app.scale_ef.configure(from_=min(value_list_hi), to=max(value_list_hi))
        app.scale_ef.set(min(value_list_hi))        
    else:
        app.scale_ef.configure(from_=min(value_list_lo), to=max(value_list_lo))
        app.scale_ef.set(min(value_list_lo))

# canvas
canv_width  = 640
canv_height = 440
bg_color    = "#ECECEC"

class Window(tk.Frame):

    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master, bg=bg_color)   
        self.master = master
        self.init_window()

    # initialize window
    def init_window(self):

        # load_method = (None, "open_file", "load_url")
        self.load_method=None

        # setup
        self.master.title("TimeSlide v0.3")
        self.pack(fill=tk.BOTH, expand=1)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # create the file menu
        file = tk.Menu(menu)
        file.add_command(label="Open Local Photo...", command=self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        # image canvas
        self.canvas = tk.Canvas(self, width=canv_width, height=canv_height,
            background='black')
        self.image_id = self.canvas.create_image(canv_width, canv_height,
            anchor='se')
        self.canvas.pack()

        # FRAME - status

        frame_status = tk.LabelFrame(self,
            text="Status", pady=4, bg=bg_color)
        frame_status.pack(fill="x", padx=4)
        self.label_status = ttk.Label(frame_status, text="Welcome to TimeSlide.", background=bg_color)
        self.label_status.pack(side=tk.LEFT, padx=120)

        # FRAME - load old photo

        frame_load = tk.LabelFrame(self,
            text="Step 1: Load Old Black-and-White Photo", pady=4, bg=bg_color)
        frame_load.pack(fill="x", padx=4)
        
        # open_file button
        btn_open_photo = ttk.Button(frame_load, text="Open Local Photo...",
            command=self.open_file)
        btn_open_photo.pack(side=tk.LEFT)
        label_or = ttk.Label(frame_load, text="  or  ", background=bg_color)
        label_or.pack(side=tk.LEFT, padx=22)
        
        # load_url button
        btn_load_url = ttk.Button(frame_load, text="Load URL",
            command=self.load_url)
        btn_load_url.pack(side=tk.RIGHT)
        
        # url_string
        self.str_url = tk.Text(frame_load, width=40, height=1)
        self.str_url.pack(side=tk.RIGHT, padx=4)

        # FRAME - colorize

        frame_colorize = tk.LabelFrame(self, text="Step 2: Colorize",
            pady=4, bg=bg_color)
        frame_colorize.pack(fill="x", padx=4)

        # colorize check box
        self.colorize_int = tk.IntVar()
        self.colorize_int.set(1)
        chk_colorize = ttk.Checkbutton(frame_colorize, text="Colorize",
            variable=self.colorize_int, offvalue=0, onvalue=1)
        chk_colorize.pack(side=tk.LEFT)
       
        # colorize model dropdown
        self.model_vars = tk.StringVar(frame_colorize)
        self.model_vars.set("Stable")
        model_label = tk.Label(frame_colorize, text='Model:', bg=bg_color)
        model_label.pack(side=tk.LEFT, padx=(15,0))
        self.colorize_model = tk.OptionMenu(frame_colorize, self.model_vars,
            "Stable", "Artistic")
        self.colorize_model.pack(side=tk.LEFT, padx=0)
        
        # colorize render factor
        min_rndr_fctr = 7
        max_rndr_fctr = 45
        self.scale_rf = tk.Scale(frame_colorize,
            from_=min_rndr_fctr, to=max_rndr_fctr, orient="horizontal",
            length=250, bg=bg_color)
        self.scale_rf.pack(side=tk.RIGHT, fill="x")
        self.scale_rf.set(35)
        label_rf = ttk.Label(frame_colorize, text="Render Factor: ",
            background=bg_color)
        label_rf.pack(sid=tk.RIGHT)

        # FRAME - enhance

        frame_enhance = tk.LabelFrame(self, text="Step 3: Enhance (Up-sample)",
            pady=4, bg=bg_color)
        frame_enhance.pack(fill="x", padx=4)

        # enhance check box
        self.enhance_int = tk.IntVar()
        self.enhance_int.set(0)
        chk_enhance = ttk.Checkbutton(frame_enhance, text="Enhance",
            variable=self.enhance_int, offvalue=0, onvalue=1)
        chk_enhance.pack(side=tk.LEFT)
       
        # enhance model dropdown
        self.weights_vars = tk.StringVar(frame_enhance)
        self.weights_vars.set("EDSR")
        weights_label = tk.Label(frame_enhance, text='Model:', bg=bg_color)
        weights_label.pack(side=tk.LEFT, padx=(15,0))
        self.weights_model = tk.OptionMenu(frame_enhance, self.weights_vars,
            "EDSR", "ESPCN", "FSRCNN", "LapSRN", command=ef_weights_callback)
        self.weights_model.pack(side=tk.LEFT, padx=0)

        # enhance multiplier
        self.scale_ef = tk.Scale(frame_enhance,
            from_=min(value_list_lo), to=max(value_list_lo),
            orient="horizontal",
            length=250, bg=bg_color, command=ef_slider_callback)
        self.scale_ef.pack(side=tk.RIGHT, fill="x")
        self.scale_ef.set(2)
        label_ef = ttk.Label(frame_enhance, text="Multiplier: ",
            background=bg_color)
        label_ef.pack(sid=tk.RIGHT)

        # FRAME - finish

        frame_finish = tk.LabelFrame(self, text="Step 4: Finish Up",
            pady=4, bg=bg_color)
        frame_finish.pack(fill="x", padx=4)
       
        # timeslide button
        #self.btn_timeslide = ttk.Button(frame_finish, text="Slide Time!",
        #    command=run_func_with_loading_popup(self, self.timeslide, 'Calculating...'))
        self.btn_timeslide = ttk.Button(frame_finish, text="Slide Time!",
            command=self.timeslide)
        self.btn_timeslide['state'] = 'disabled'
        self.btn_timeslide.pack(side=tk.LEFT)

        # save as button
        self.btn_save_photo = ttk.Button(frame_finish, text="Save New Photo...",
            command=self.save_file)
        self.btn_save_photo['state'] = 'disabled'
        self.btn_save_photo.pack(side=tk.LEFT)

        # TOOLTIPS

        # colorize tooltip
        CreateToolTip(chk_colorize, \
            "If checked, will colorize the image using the deoldify project, "
            "using their pre-trained model weights.")

        # colorize model tooltip
        CreateToolTip(model_label, \
            "Artistic: More colorful.\n"
            "Stable: Not as colorful, but fewer glitches.\n"
            "According to De-oldify, Stable should be used for landscapes"
            " and portraits; Artistic otherwise.")

        # render factor tooltip
        CreateToolTip(label_rf, \
            "According to De-oldify, older images tend to benefit from a "
            "lower render factor (which is faster). Newer images tend to "
            "benefit from a higher render factor.")

        # enhance tooltip
        CreateToolTip(chk_enhance, \
            "Enhance should ONLY be used on very small images. It is memory "
            "intensive to the point that it will max out your RAM, and then "
            "start filling your hard drive, and take forever!")

        # enhance model tooltip
        CreateToolTip(weights_label, \
            "EDSR is best performance, but is the slowest. ESPCN and FSRCNN"
            " are small, fast models. LapSRN is a medium-sized model, that "
            "can go up to 8x.")

        # enhance factor tooltip
        CreateToolTip(label_ef, \
            "This value is the multiplied factor for each dimension of"
            " the photo.")

    # open file
    def open_file(self):

        # load file dialog
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png'),
        ]
        self.file_path = tk.filedialog.askopenfilename(filetypes=file_types)
        
        # open image and resize
        img = Image.open(self.file_path)
        img = img.resize((canv_width, canv_height), Image.ANTIALIAS)
        self.canvas.img_tk = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.image_id, image=self.canvas.img_tk)

        # set status
        self.label_status.config(text="Old photo loaded from local file.")

        # enable timeslide button
        self.btn_timeslide['state'] = 'normal'

        # set load method
        self.load_method="open_file"

    # load from url
    def load_url(self):
        
        # load raw data and display
        raw_data = urllib.request.urlopen(self.str_url.get("1.0",tk.END)).read()
        img = Image.open(io.BytesIO(raw_data))
        img = img.resize((canv_width, canv_height), Image.ANTIALIAS)
        self.canvas.img_tk = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.image_id, image=self.canvas.img_tk)

        # set status
        self.label_status.config(text="Old photo loaded from URL.")

        # enable timeslide button
        self.btn_timeslide['state'] = 'normal'

        # set load method
        self.load_method="load_url"

    # timeslide
    def timeslide(self):

        # colorization
        if (self.colorize_int.get() == 1):

            # set status
            self.label_status.config(text="Colorizing. Please stand by...")
            self.update()

            # determine colorizer model
            if (self.model_vars.get() == "Artistic"):
                colorizer = get_image_colorizer(artistic=True)
            elif (self.model_vars.get() == "Stable"):
                colorizer = get_image_colorizer(artistic=False)

            # get render factor
            render_factor = self.scale_rf.get()

            if self.load_method in "open_file":
                self.result_path = colorizer.plot_transformed_image(
                    path = self.file_path, render_factor = render_factor,
                    compare = False)
            elif self.load_method in "load_url":
                print(self.str_url.get("1.0",tk.END))
                self.result_path = colorizer.plot_transformed_image_from_url(
                    url=self.str_url.get("1.0",tk.END), path='//tmp/tmp.png',
                    render_factor = render_factor, compare = False)
            img = Image.open(self.result_path)

            # display to canvas
            img = img.resize((canv_width, canv_height), Image.ANTIALIAS)
            self.canvas.img_tk = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_id, image=self.canvas.img_tk)
            self.update()

        # do enhancement
        if (self.enhance_int.get() == 1):

            # set status
            self.label_status.config(text="Enhancing. Please stand by...")
            self.update()

            # determine which file we're reading
            if (self.colorize_int.get() == 1):
                filepath = self.result_path
            else:
                filepath = self.file_path

            # Create an SR object
            sr = dnn_superres.DnnSuperResImpl_create()

            # Read image
            image = cv2.imread(str(filepath))

            # Read the desired model, enhance factor
            model = self.weights_vars.get()
            enhance_factor = int(self.scale_ef.get())
            path = "models/%s_x%i.pb" % (model, enhance_factor)
            sr.readModel(path)

            print(model)
            print(enhance_factor)

            # Set the desired model and scale to get correct pre- and post-processing
            sr.setModel(model.lower(), enhance_factor)

            # Upscale the image
            result = sr.upsample(image)

            # Save the image
            self.result_path = './tmp_enhance.jpg'
            cv2.imwrite(self.result_path, result)
                
            # display to canvas
            img = Image.open(self.result_path)
            img = img.resize((canv_width, canv_height), Image.ANTIALIAS)
            self.canvas.img_tk = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_id, image=self.canvas.img_tk)
            self.update()

            # open file
            #img = load_image(filepath)

            # EDSRx4 model
            #if (self.weights_vars.get() == "EDSRx4"):
            #    depth = 16
            #    scale = 4
            #    weights_dir = f'weights/edsr-{depth}-x{scale}'
            #    weights_file = os.path.join(weights_dir, 'weights.h5')
            #    os.makedirs(weights_dir, exist_ok=True)
            #    
            #    model = edsr(scale=scale, num_res_blocks=depth)
            #    model.load_weights(weights_file)
            #    img = resolve_single(model, img)

            # WDSRx4 model
            #if (self.weights_vars.get() == "WDSRx4"):
            #    depth = 32
            #    scale = 4
            #    weights_dir = f'weights/wdsr-b-{depth}-x{scale}'
            #    weights_file = os.path.join(weights_dir, 'weights.h5')
            #    os.makedirs(weights_dir, exist_ok=True)
            #    
            #    model = wdsr_b(scale=scale, num_res_blocks=depth)
            #    model.load_weights(weights_file)
            #    img = resolve_single(model, img)

            # save result to file
            #img = tf.keras.preprocessing.image.array_to_img(img)
            #if (self.colorize_int.get() == 1):
            #    img.save(self.result_path)
            #else:
            #    img.save('./tmp_enhance.jpg')
            #    self.result_path = './tmp_enhance.jpg'

        # set status to complete
        self.label_status.config(text="TimeSlide complete!")

        # enable save button
        self.btn_save_photo['state'] = 'normal'

    def save_file(self):
        file_types = [
            ('Image files', '*.jpg *.jpeg'),
        ]
        print(str(self.result_path))
        save_file = tk.filedialog.asksaveasfile(filetypes = file_types,
            defaultextension=".jpg")
        from_path = str(os.getcwd()) + "/" + str(self.result_path)
        shutil.copyfile(from_path, save_file.name)

    # exit
    def client_exit(self):
        exit()

# configure primary window        
root = tk.Tk()
root.geometry("%ix738" % canv_width)
root.configure(bg=bg_color)

# creation of an instance
app = Window(root)

# mainloop 
root.mainloop()  