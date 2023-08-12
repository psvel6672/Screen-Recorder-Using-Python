# Tkinter Components

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
import pyautogui as pag

import cv2
import threading
import os, time, datetime, shutil

class ScreenRecorder:

    def __init__(self):

        self.ScreenShotFolder = "Screen Shots"

        if not os.path.isdir(self.ScreenShotFolder):
            os.mkdir(self.ScreenShotFolder)

        self.startRecording = False
        self.tmpFolder = "tmp_files"
        self.outputFolder = "Screen_Recordings"
        if not os.path.isdir(self.outputFolder):
            os.mkdir(self.outputFolder)
        
        self.SRWind = Tk()
        self.SRWind.geometry("500x75+400+400")
        self.SRWind.resizable(0, 0)
        self.SRWind.title("PS Screen Recorder")
        self.SRWind.iconbitmap('./src_files/SCR-ICON1.ico')
        
        self.recordAction = Button(self.SRWind, text='Click to Start', width=13, command = self._recordingActionThread)
        self.recordAction.place(x = 4, y = 5)

        self.scrnshotBtn = Button(self.SRWind, text='Take Screenshot', width=16, command=self._takeScreenShotThread)
        self.scrnshotBtn.place(x = 145, y = 5)

        self.statusAct = Label(self.SRWind, text='Status :: Ready', font=("Times New Roman bold", 9), foreground='red')
        self.statusAct.place(x = 325, y = 12)

        chkCurrentYear = datetime.datetime.now().strftime("%Y")

        if int(chkCurrentYear) > 2023:
            cpyrightYear = "2023 - "+str(chkCurrentYear)
        else:
            cpyrightYear = "2023"

        self.authorLabel = Label(self.SRWind, text='PS Thamizhan - © '+str(cpyrightYear)+'. V1.0', font=("Segoe UI", 7))
        self.authorLabel.pack(side=BOTTOM, ipady=5)

    def _takeScreenShotThread(self):
        getScreenShotThread = threading.Thread(target=self.takeScreenShot, name='Take Screen Shot')
        getScreenShotThread.start()

    def takeScreenShot(self):

        try:
            now = datetime.datetime.now().strftime("%I%M%S%p")
            filename = str(self.ScreenShotFolder)+"/Screen_Shot_" + str(now) + ".jpg"
            pag.screenshot(filename)

            messagebox.showinfo("Screen Recorder Alert", "Screen shot Saved.\nFile Name : "+str(filename))

        except:
            messagebox.showinfo("Screen Recorder Alert", "Something Wrong to take Screen shot.           ")

        return True

    def _recordingActionThread(self):

        if self.startRecording == False:
            self.startRecording = True
            startSRThread = threading.Thread(target=self.startRecoding, name='Start a Screen Recorder')
            startSRThread.start()
        else:
            self.startRecording = False
            time.sleep(2)
            stopSRThread = threading.Thread(target=self.stopRecoding, name='Stop a Screen Recorder')
            stopSRThread.start()

        return True

    def startRecoding(self):
        
        if not os.path.isdir(self.tmpFolder):
            os.mkdir(self.tmpFolder)

        self.statusAct.config(text = "Status :: Recording...")
        self.recordAction.config(text = "Click to Stop")
        
            
        while self.startRecording:
            now = datetime.datetime.now().strftime("%I%M%S%p")
            filename = str(self.tmpFolder)+"/tmp_" + str(now) + ".jpg"
            pag.screenshot(filename)
        return True

    def stopRecoding(self):
        
        tmpImgArr = []

        VideoFileName = ""

        try:
            tmpFiles = os.listdir(self.tmpFolder)
            for img in tmpFiles:
                filePath = str(self.tmpFolder)+'/'+str(img)
                imgFile = cv2.imread(filePath)
                height, width, layers = imgFile.shape
                self.imgSize = (width, height)
                tmpImgArr.append(imgFile)
            
            dateNow = datetime.datetime.now().strftime("%b%d%Y_%I%M%S%p")
            VideoFileName = 'Screen_Recording_'+str(dateNow)+'.avi'
            finalFileName = str(self.outputFolder)+'/'+str(VideoFileName)
            writeActualVideo = cv2.VideoWriter(finalFileName, cv2.VideoWriter_fourcc(*"XVID"), 24, self.imgSize)

            for tmpSS in range(len(tmpImgArr)):
                writeActualVideo.write(tmpImgArr[tmpSS])
            writeActualVideo.release()

            try:
                shutil.rmtree(self.tmpFolder)
            except:
                os.unlink(self.tmpFolder)

        except:
            self.statusAct.config(text = "Status :: Error.")
            self.recordAction.config(text = "Click to Start")
            messagebox.showinfo("Screen Recorder Alert", "Screen Recording Error.                               ")
            return False

        self.statusAct.config(text = "Status :: Completed.")
        self.recordAction.config(text = "Click to Start")

        messagebox.showinfo("Screen Recorder Alert", "Screen Recording Completed.\nFile Name : "+str(VideoFileName))

        return True

    def runModule(self):
        self.SRWind.mainloop()


recorder = ScreenRecorder()
recorder.runModule()
