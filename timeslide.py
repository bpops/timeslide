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

# canvas
canv_width  = 500
canv_height = 400
bg_color    = "#ECEBEC"

class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master, bg=bg_color)   
        #reference to the master widget, which is the tk window                 
        self.master = master
        self.init_window()

    # initialize window
    def init_window(self):

        # setup
        self.master.title("timeslide")
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

        # button frame
        btn_frame = tk.Frame(self, background=bg_color)
        btn_frame.pack()

        # open_file button
        btn_open_photo = ttk.Button(btn_frame, text="Load Photo",
            command=self.open_file)
        btn_open_photo.pack(side=tk.LEFT)

        # colorize button
        self.btn_colorize = ttk.Button(btn_frame, text="Colorize!",
            command=self.colorize)
        self.btn_colorize['state'] = 'disabled'
        self.btn_colorize.pack(side=tk.LEFT)

        # save as button
        self.btn_save_photo = ttk.Button(btn_frame, text="Save Photo",
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

        # enable save button
        self.btn_colorize['state'] = 'normal'

    # colorize
    def colorize(self):

        self.result_path = colorizer.plot_transformed_image(
            path = self.file_path, render_factor = render_factor,
            compare = False)
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
root.geometry("%ix434" % canv_width)
root.configure(bg=bg_color)

# creation of an instance
app = Window(root)

# mainloop 
root.mainloop()  