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

from cgitb import text
import os, sys
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt6.QtWidgets import QGroupBox, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QCheckBox, QComboBox, QSlider, QFileDialog
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtGui     import QPixmap
from PyQt6.QtCore    import Qt, pyqtSignal

# required for pyinstaller: pytorch
os.environ["PYTORCH_JIT"] = "0"

# set up delodify
#from deoldify import device
#from deoldify.device_id import DeviceId
#device.set(device = DeviceId.GPU0)
#from deoldify.visualize import *
#torch.backends.cudnn.benchmark = True

# set up image enhance
import cv2
from cv2 import dnn_superres

# import other modules
#import threading
#import tensorflow as tf
import shutil
import os
#import urllib.request
#import io
#import numpy as np
#import time

# set working directory
# used for development vs bundled paths
try:
   wd = sys._MEIPASS
except AttributeError:
   wd = os.path.dirname(os.path.realpath(__file__))
   #wd = os.getcwd()
os.chdir(wd)

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
        self.showImage(QPixmap(f'{wd}/dustbowl.jpg'))

        # frame - status
        frame_status = QGroupBox(self)
        frame_status.setTitle("Status")
        layout_status = QVBoxLayout()
        lbl_status = QLabel("Load a photo to start.")
        frame_status.setLayout(layout_status)
        layout_status.addWidget(lbl_status)

        # frame - step 1
        frame_step1 = QGroupBox(self)
        frame_step1.setTitle("Step 1: Load Photo")
        layout_step1 = QHBoxLayout()
        lbl_step1_or = QLabel("   or      ")
        frame_step1.setLayout(layout_step1)
        btn_loadlocal = QPushButton("Load Local Photo")
        btn_loadlocal.clicked.connect(self.loadLocal)
        text_step1_url = QLineEdit()
        btn_load_url = QPushButton("Load URL")
        layout_step1.addWidget(btn_loadlocal)
        layout_step1.addWidget(lbl_step1_or)
        layout_step1.addWidget(text_step1_url, 1)
        text_step1_url.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # wtf.
        layout_step1.addWidget(btn_load_url)

        # frame - step 2
        frame_step2 = QGroupBox(self)
        frame_step2.setTitle("Step 2: Colorize")
        layout_step2 = QHBoxLayout()
        cbox_step2 = QCheckBox("Colorize")
        cbox_step2.setChecked(1)
        ddown_step2 = QComboBox()
        ddown_step2.addItems(["Stable", "Artistic"])
        sldr_step2 = QSlider(Qt.Orientation.Horizontal)
        min_rndr_fctr = 7
        max_rndr_fctr = 45
        sldr_step2.setMinimum(min_rndr_fctr)
        sldr_step2.setMaximum(max_rndr_fctr)
        frame_step2.setLayout(layout_step2)
        layout_step2.addWidget(cbox_step2)
        layout_step2.addWidget(QLabel("     Model:"))
        layout_step2.addWidget(ddown_step2)
        layout_step2.addWidget(QLabel("    Render Factor:"))
        layout_step2.addWidget(sldr_step2, 1)
        self.renderLabel = QLabel("7")
        layout_step2.addWidget(self.renderLabel)
        sldr_step2.valueChanged.connect(self.updateRenderLabel)

        # frame - step 3
        frame_step3 = QGroupBox(self)
        frame_step3.setTitle("Step 3: Enhance")
        layout_step3 = QHBoxLayout()
        cbox_step3 = QCheckBox("Enhance")
        ddown_step3 = QComboBox()
        ddown_step3.addItems(["EDSR", "ESPCN", "FSRCNN", "LapSRN"])
        frame_step3.setLayout(layout_step3)
        layout_step3.addWidget(cbox_step3)
        layout_step3.addWidget(QLabel("    Model:"))
        layout_step3.addWidget(ddown_step3)
        layout_step3.addWidget(QLabel("          Multiplier:"))
        sldr_step3 = QSlider(Qt.Orientation.Horizontal)
        value_list_lo = [2, 3, 4]
        value_list_hi = [2, 4, 8]
        layout_step3.addWidget(sldr_step3, 1)
        self.multLabel = QLabel(str(value_list_lo[0]))
        layout_step3.addWidget(self.multLabel)
        sldr_step3.valueChanged.connect(self.updateMultLabel)

        # frame - step 4
        frame_step4 = QGroupBox(self)
        frame_step4.setTitle("Step 4: Finish Up")
        layout_step4 = QHBoxLayout()
        btn_slidetime = QPushButton("Slide Time!")
        btn_savenewphoto = QPushButton("Save New Photo")
        frame_step4.setLayout(layout_step4)
        layout_step4.addWidget(btn_slidetime, 1)
        layout_step4.addWidget(btn_savenewphoto)

        # overall layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.img_lbl)#alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(frame_status, stretch=0)
        self.vbox.addWidget(frame_step1, stretch=0)
        self.vbox.addWidget(frame_step2, stretch=0)
        self.vbox.addWidget(frame_step3, stretch=0)
        self.vbox.addWidget(frame_step4, stretch=0)
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
        filepath = QFileDialog.getOpenFileName(self, 'Load photo', wd)
        if filepath[0]:
            f = open(filepath[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)

    def showImage(self, pix_map):
        """
        Show the given QPixMap
        """
        self.pix_map = pix_map
        self.img = self.pix_map.scaled(init_canv_width, init_canv_height,
            aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation)
        self.img_lbl = QLabel()
        self.img_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.img_lbl.setMinimumSize(init_canv_width, init_canv_height)
        self.img_lbl.setPixmap(self.img)
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)

def main():
    app = QApplication(sys.argv)
    ex = timeslideApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()