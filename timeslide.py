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


# pyqt6 requirements
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QCheckBox, QComboBox, QSlider, QFileDialog
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtGui     import QPixmap
from PyQt6.QtCore    import Qt, pyqtSignal

# required for pyinstaller: pytorch
import os
os.environ["PYTORCH_JIT"] = "0"

# set up delodify
from deoldify import device
from deoldify.device_id import DeviceId
device.set(device = DeviceId.GPU0)
from deoldify.visualize import *
torch.backends.cudnn.benchmark = True
import torchvision

# set up image enhance
#import cv2
#from cv2 import dnn_superres

# other
import sys
#import threading
#import tensorflow as tf
#from cgitb import text
#import shutil
from PIL import Image
import urllib.request
import validators
import requests
#import urllib.request
from io import BytesIO
#import numpy as np
#import time

# set working directory
# (used for development vs bundled paths)
try:
   wd = sys._MEIPASS
except AttributeError:
   wd = os.path.dirname(os.path.realpath(__file__))
   #wd = os.getcwd()
os.chdir(wd)
model_dir = f"{wd}/models"

# load pretrained torch models
os.environ["TORCH_HOME"] = model_dir
resnet = torchvision.models.resnet34(pretrained=True)
resnet = torchvision.models.resnet101(pretrained=True)

# canvas
init_canv_width  = 640
init_canv_height = 440
init_win_width   = 600
init_win_height  = 738

class timeslideApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(init_win_width, init_win_height)

        # image canvas
        self.img_lbl = QLabel()
        self.img_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.img_lbl.setMinimumSize(init_canv_width, init_canv_height)
        img_pth = f'{wd}/imgs/dustbowl.jpg'
        self.showImage(img_pth)

        # frame - status
        frame_status = QGroupBox(self)
        frame_status.setTitle("Status")
        layout_status = QVBoxLayout()
        self.lbl_status = QLabel("")
        frame_status.setLayout(layout_status)
        layout_status.addWidget(self.lbl_status)
        self.setStatus("Load a photo to start.")

        # load photo
        frame_loadstep = QGroupBox(self)
        frame_loadstep.setTitle("Load Photo")
        layout_loadstep = QHBoxLayout()
        lbl_loadstep_or = QLabel("   or      ")
        frame_loadstep.setLayout(layout_loadstep)
        btn_loadlocal = QPushButton("Load Local Photo")
        btn_loadlocal.clicked.connect(self.loadLocal)
        self.text_loadstep_url = QLineEdit()
        btn_load_url = QPushButton("Load URL")
        btn_load_url.clicked.connect(self.loadURL)
        layout_loadstep.addWidget(btn_loadlocal)
        layout_loadstep.addWidget(lbl_loadstep_or)
        layout_loadstep.addWidget(self.text_loadstep_url, 1)
        self.text_loadstep_url.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # wtf.
        layout_loadstep.addWidget(btn_load_url)

        # colorize
        frame_stepcolor = QGroupBox(self)
        frame_stepcolor.setTitle("Colorize")
        layout_stepcolor = QHBoxLayout()
        self.cbox_stepcolor = QCheckBox("Colorize")
        self.cbox_stepcolor.setChecked(1)
        self.ddown_stepcolor = QComboBox()
        self.ddown_stepcolor.addItems(["Stable", "Artistic"])
        self.sldr_stepcolor = QSlider(Qt.Orientation.Horizontal)
        min_rndr_fctr = 7
        max_rndr_fctr = 45
        self.sldr_stepcolor.setMinimum(min_rndr_fctr)
        self.sldr_stepcolor.setMaximum(max_rndr_fctr)
        frame_stepcolor.setLayout(layout_stepcolor)
        layout_stepcolor.addWidget(self.cbox_stepcolor)
        layout_stepcolor.addWidget(QLabel("     Model:"))
        layout_stepcolor.addWidget(self.ddown_stepcolor)
        layout_stepcolor.addWidget(QLabel("    Render Factor:"))
        layout_stepcolor.addWidget(self.sldr_stepcolor, 1)
        self.renderLabel = QLabel("7")
        layout_stepcolor.addWidget(self.renderLabel)
        self.sldr_stepcolor.valueChanged.connect(self.updateRenderLabel)

        # enhance
        #frame_stepenhance = QGroupBox(self)
        #frame_stepenhance.setTitle("Enhance (Upscale)")
        #layout_stepenhance = QHBoxLayout()
        #cbox_stepenhance = QCheckBox("Enhance")
        #ddown_stepenhance = QComboBox()
        #ddown_stepenhance.addItems(["EDSR", "ESPCN", "FSRCNN", "LapSRN"])
        #frame_stepenhance.setLayout(layout_stepenhance)
        #layout_stepenhance.addWidget(cbox_stepenhance)
        #layout_stepenhance.addWidget(QLabel("    Model:"))
        #layout_stepenhance.addWidget(ddown_stepenhance)
        #layout_stepenhance.addWidget(QLabel("          Multiplier:"))
        #sldr_stepenhance = QSlider(Qt.Orientation.Horizontal)
        #value_list_lo = [2, 3, 4]
        #value_list_hi = [2, 4, 8]
        #layout_stepenhance.addWidget(sldr_stepenhance, 1)
        #self.multLabel = QLabel(str(value_list_lo[0]))
        #layout_stepenhance.addWidget(self.multLabel)
        #sldr_stepenhance.valueChanged.connect(self.updateMultLabel)

        # finalize
        frame_stepslide = QGroupBox(self)
        frame_stepslide.setTitle("Finalize")
        layout_stepslide = QHBoxLayout()
        btn_slidetime = QPushButton("Slide Time!")
        btn_slidetime.clicked.connect(self.slideTime)
        btn_savenewphoto = QPushButton("Save New Photo")
        frame_stepslide.setLayout(layout_stepslide)
        layout_stepslide.addWidget(btn_slidetime, 1)
        layout_stepslide.addWidget(btn_savenewphoto)

        # overall layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.img_lbl)#alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(frame_status,    stretch=0)
        self.vbox.addWidget(frame_loadstep,  stretch=0)
        self.vbox.addWidget(frame_stepcolor, stretch=0)
        #self.vbox.addWidget(frame_stepenhance, stretch=0)
        self.vbox.addWidget(frame_stepslide, stretch=0)
        self.setLayout(self.vbox)

        self.setWindowTitle('TimeSlide v0.5')
        self.show();
        self.centerWindow()

    def updateRenderLabel(self, value):
        self.renderLabel.setText(str(value))
    def updateMultLabel(self, value):
        self.multLabel.setText(str(value))

    def resizeEvent(self, event):
        self.img = self.pix_map.scaled(self.img_lbl.size().width(), self.img_lbl.size().height(),
            aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.FastTransformation)
        self.img_lbl.setPixmap(self.img)
        return super().resizeEvent(event)

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadLocal(self):
        """
        Load local file
        """
        filepath = QFileDialog.getOpenFileName(self, 'Load photo', wd)
        if filepath[0]:
            self.setStatus(f"Opened {filepath[0]}")
            self.showImage(filepath[0])

    def loadURL(self):
        """
        Load URL
        """
        url = self.text_loadstep_url.text()
        if not validators.url(url):
            self.setStatus("Invalid URL")
        else:
            self.showImage(url)

    def setStatus(self, text):
        """
        Set Status Text
        """
        self.lbl_status.setText(text)
        self.lbl_status.repaint()
        QApplication.processEvents()

    def showImage(self, img_pth):
        """
        Show the given image
        """

        # load the pixel map
        if not validators.url(img_pth): # local path
            self.pix_map = QPixmap(img_pth)
            is_url = False
        else:                           # url
            img_data = urllib.request.urlopen(img_pth).read()
            self.pix_map = QPixmap()
            self.pix_map.loadFromData(img_data)
            is_url = True
        
        # set canvas properties
        self.img = self.pix_map.scaled(self.img_lbl.size().width(),
            self.img_lbl.size().height(),
            aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio,
            transformMode   = Qt.TransformationMode.SmoothTransformation)
        self.img_lbl.setPixmap(self.img)
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # open the image
        if is_url:
            self.setStatus("Downloading. Please wait...")
            response = requests.get(img_pth)
            self.img_base = Image.open(BytesIO(response.content))
            self.setStatus(f"Downloaded {img_pth}")
        else:
            self.img_base = Image.open(img_pth)
        self.update()

    def slideTime(self):

        # colorize
        if self.cbox_stepcolor.isChecked():

            # get settings
            model_i   = self.ddown_stepcolor.currentIndex()
            model     = self.ddown_stepcolor.currentText()
            artistic  = False if model_i == 0 else True
            rndr_fctr = self.sldr_stepcolor.value()
            
            # set status
            self.setStatus(f"Colorizing ({model} {rndr_fctr}). Please wait...")

            # set colorizer
            colorizer = get_image_colorizer(artistic=artistic)

def main():
    app = QApplication(sys.argv)
    ex = timeslideApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()