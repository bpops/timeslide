#     __                                    ___            __
#    /\ \__  __                            /\_ \    __    /\ \
#    \ \ ,_\/\_\    ___ ___      __    ____\//\ \  /\_\   \_\ \     __
#     \ \ \/\/\ \ /' __` __`\  /'__`\ /',__\ \ \ \ \/\ \  /'_` \  /'__`\
#      \ \ \_\ \ \/\ \/\ \/\ \/\  __//\__, `\ \_\ \_\ \ \/\ \L\ \/\  __/
#       \ \__\\ \_\ \_\ \_\ \_\ \____\/\____/ /\____\\ \_\ \___,_\ \____\
#        \/__/ \/_/\/_/\/_/\/_/\/____/\/___/  \/____/ \/_/\/__,_ /\/____/
#
#        a beautifully simple gui to slide old photographs into TODAY
#

# set up delodify
from deoldify import device
from deoldify.device_id import DeviceId
device.set(device = DeviceId.GPU0)
from deoldify.visualize import *
torch.backends.cudnn.benchmark = True
colorizer = get_image_colorizer(artistic=True)
render_factor = 30

# other modules
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import shutil
import os
import urllib.request
import io

# canvas
canv_width  = 500
canv_height = 400
bg_color    = "#ECECEC"

class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master, bg=bg_color)   
        #reference to the master widget, which is the tk window                 
        self.master = master
        self.init_window()

    # initialize window
    def init_window(self):

        # load_method = (None, "open_file", "load_url")
        self.load_method=None

        # setup
        self.master.title("TimeSlide")
        self.pack(fill=tk.BOTH, expand=1)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # create the file menu
        file = tk.Menu(menu)
        file.add_command(label="Load Photo...", command=self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        # image canvas
        self.canvas = tk.Canvas(self, width=canv_width, height=canv_height,
            background='black')
        self.image_id = self.canvas.create_image(canv_width, canv_height,
            anchor='se')
        self.canvas.pack()

        # FRAME - load old photo

        frame_load = tk.LabelFrame(self, text="Step 1: Load Old Photo",
            pady=4, bg=bg_color)
        frame_load.pack(fill="x", padx=4)
        
        # open_file button
        btn_open_photo = ttk.Button(frame_load, text="Open Local File...",
            command=self.open_file)
        btn_open_photo.pack(side=tk.LEFT)
        label_or = ttk.Label(frame_load, text="  or  ", background=bg_color)
        label_or.pack(sid=tk.LEFT, padx=22)
        
        # load_url button
        btn_load_url = ttk.Button(frame_load, text="Load URL",
            command=self.load_url)
        btn_load_url.pack(side=tk.RIGHT)
        
        # url_string
        self.str_url = tk.Text(frame_load, width=40, height=1)
        self.str_url.pack(side=tk.RIGHT, padx=4)

        # FRAME - finish

        frame_finish = tk.LabelFrame(self, text="Step 2: Finish Up",
            pady=4, bg=bg_color)
        frame_finish.pack(fill="x", padx=4)
       
        # colorize button
        self.btn_colorize = ttk.Button(frame_finish, text="Slide Time!",
            command=self.colorize)
        self.btn_colorize['state'] = 'disabled'
        self.btn_colorize.pack(side=tk.LEFT)

        # save as button
        self.btn_save_photo = ttk.Button(frame_finish, text="Save New Photo...",
            command=self.save_file)
        self.btn_save_photo['state'] = 'disabled'
        self.btn_save_photo.pack(side=tk.LEFT)

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

        # enable colorize button
        self.btn_colorize['state'] = 'normal'

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

        # enable colorize button
        self.btn_colorize['state'] = 'normal'

        # set load method
        self.load_method="load_url"

    # colorize
    def colorize(self):

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
        img = img.resize((canv_width, canv_height), Image.ANTIALIAS)
        self.canvas.img_tk = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.image_id, image=self.canvas.img_tk)

        # enable save button
        self.btn_save_photo['state'] = 'normal'

    def save_file(self):
        file_types = [
            ('Image files', '*.jpg *.jpeg')
        ]
        save_file = tk.filedialog.asksaveasfile(filetypes = file_types)
        from_path = str(os.getcwd()) + "/" + str(self.result_path)
        print(from_path)
        print(save_file.name)
        shutil.copyfile(from_path, save_file.name)

    # exit
    def client_exit(self):
        exit()

# configure primary window        
root = tk.Tk()
root.geometry("%ix514" % canv_width)
root.configure(bg=bg_color)

# creation of an instance
app = Window(root)

# mainloop 
root.mainloop()  