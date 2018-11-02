from tkinter import *
from tkinter import filedialog,simpledialog
from PIL import Image,ImageTk
import os
import cv2 as cv
import numpy as np

class Window():

    def __init__(self,master=None):
        self.master = master
        self.GS_IMG = 1
        self.RGB_IMG = 2
        self.init_window()

    def init_window(self):
        self.master.title("Image Processing")
        self.init_menubar()

        self.labelOri = Label(self.master,text="Image Original",font=("Arial",20))
        self.labelOri.grid(row=0,column=0)

        image = Image.open(os.curdir + "/noimage.jpg")
        img = ImageTk.PhotoImage(self.adjustAspectRatio(image))   
        self.labelImageOri = Label(self.master,image=img , borderwidth=2, relief="groove",font=("Arial",15))
        self.labelImageOri.image = img
        self.labelImageOri.grid(row=1,column=0,sticky=N+E+W+S,padx=5,pady=5)

        self.labelResult = Label(self.master,text="Result Image",font=("Arial",20))
        self.labelResult.grid(row=0,column=1)

        image = Image.open(os.curdir + "/noimage.jpg")
        img = ImageTk.PhotoImage(self.adjustAspectRatio(image)) 
        self.labelImageResult = Label(self.master,image=img ,borderwidth=2, relief="groove",font=("Arial",15))
        self.labelImageResult.image = img
        self.labelImageResult.grid(row=1,column=1,sticky=N+E+W+S,padx=5,pady=5)


    def init_menubar(self):
        #Menu Bar
        self.menubar = Menu(self.master)

        #Menu File
        self.filemenu = Menu(self.menubar,tearoff=0)
        #Adding command Browse,Save,Exit to file menu
        self.filemenu.add_command(label="Browse",command=self.openFile)
        self.filemenu.add_command(label="Save File",command=self.saveFile)

        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",command=self.master.destroy)

        #Menu Process
        self.processmenu = Menu(self.menubar,tearoff=0)

        #Adding command Grayscale to processmenu
        self.processmenu.add_command(label="GrayScale",command=self.grayScale)
        
        #SubMenu Edge Detection
        self.edgemenu = Menu(self.processmenu,tearoff=0)
        #SubMenu Filtering
        self.filteringmenu = Menu(self.processmenu,tearoff=0)
        #SubMenu Morfologi
        self.morfologimenu = Menu(self.processmenu,tearoff=0)

        #Adding command canny,laplacian to submenu edge detection
        self.edgemenu.add_command(label="Canny",command=self.getCustomTreshold)
        self.edgemenu.add_command(label="Laplacian",command=self.laplacian)

        #Adding command mean,gaussian,median to submenu morfologi
        self.filteringmenu.add_command(label="Mean",command=lambda : self.filtering("mean"))
        self.filteringmenu.add_command(label="Gaussian",command=lambda : self.filtering("gaussian"))
        self.filteringmenu.add_command(label="Median",command=lambda : self.filtering("median"))

        #Adding command erosi,dilasi,opening,closing to submenu morfologi 
        self.morfologimenu.add_cascade(label="Erosi",menu=self.getKernelMenu("erosi"))
        self.morfologimenu.add_cascade(label="Dilasi",menu=self.getKernelMenu("dilasi"))
        self.morfologimenu.add_cascade(label="Opening",menu=self.getKernelMenu("opening"))
        self.morfologimenu.add_cascade(label="Closing",menu=self.getKernelMenu("closing"))

        #Adding submenu edge detection,filtering,morfologi to process menu
        self.processmenu.add_cascade(label="Edge Detection",menu=self.edgemenu)
        self.processmenu.add_cascade(label="Filtering",menu=self.filteringmenu)
        self.processmenu.add_cascade(label="Morfologi",menu=self.morfologimenu)

        #Adding menu file,process to menubar
        self.menubar.add_cascade(label="File",menu=self.filemenu)
        self.menubar.add_cascade(label="Process",menu=self.processmenu)

        #Adding menubar to window
        self.master.config(menu=self.menubar)
    
    def getCustomTreshold(self):
        treshold = simpledialog.askstring("Treshold","Masukkan rentang treshold dengan format : lowTreshold-highTreshold (Min=0 , Max=255). Contoh : 20-150",parent=self.master)
        self.canny(treshold)
    #Dialog untuk memasukkan angka (N) yang nantinya akan menjadi kernel NxN
    def getCustomKernel(self,operation=None,kernel=None):
        self.n = simpledialog.askinteger("Kernel","Masukkan Ukuran Kernel yang akan dibuat",parent=self.master,minvalue=2,maxvalue=100)
        self.morphologi(operation,kernel)

    #Membuat menu kernel yang tersedia pada masing-masing command (erosi,dilasi,opening,closing)
    def getKernelMenu(self,operation=None):
        menu = Menu(self.morfologimenu,tearoff=0)
        menu.add_command(label="Kernel 5x5 Rectangle",command=lambda: self.morphologi(operation,"rectangle"))
        menu.add_command(label="Kernel 5x5 Ellips",command=lambda: self.morphologi(operation,"ellips"))
        menu.add_command(label="Kernel 5x5 Cross",command=lambda: self.morphologi(operation,"cross"))
        menu.add_separator()
        menu.add_command(label="Custom NxN",command=lambda: self.getCustomKernel(operation,"custom"))
        return menu

    #Membuka file dari explorer dan menampilkannya pada bagian label "Image Original" pada GUI
    def openFile(self):
        self.filepath = filedialog.askopenfilename(initialdir="/",title="Select File",filetypes=(("all files","*.*"),("jpeg files","*.jpg")))
        image = Image.open(self.filepath)
        img = ImageTk.PhotoImage(self.adjustAspectRatio(image))            
        self.labelImageOri.configure(image=img)
        self.labelImageOri.image = img

    
    #Menyimpan image yang sudah di proses dengan format .jpg
    def saveFile(self):
        fileSavePath = filedialog.asksaveasfilename(initialdir="/",title="Save File")
        cv.imwrite(fileSavePath + ".jpg",self.procedImage)
    
    #Operasi yang tersedia pada submenu filtering
    def filtering(self,operation=None):
        if operation == "gaussian":
            self.filteringGaussian()
        if operation == "mean":
            self.filteringMean()
        if operation == "median":
            self.filteringMedian()
            
    #Operasi filtering gaussian
    def filteringGaussian(self):
        imgCV = cv.imread(self.filepath)
        gaussian = cv.GaussianBlur(imgCV,(5,5),0)
        self.setImgResultBGR2RGB(gaussian)
    
    #Operasi filtering mean
    def filteringMean(self):
        imgCV = cv.imread(self.filepath)
        mean = cv.blur(imgCV,(5,5))
        self.setImgResultBGR2RGB(mean)

    #Operasi filtering median    
    def filteringMedian(self):
        imgCV = cv.imread(self.filepath)
        median = cv.medianBlur(imgCV,5)
        self.setImgResultBGR2RGB(median)

    #Menyesuaikan image yang di load dengan aspect ratio dalam kasus ini terdapat 2 kondisi
    def adjustAspectRatio(self,image=None):
        width,height = image.size
        newImg= None
        print(str(height) + " " + str(width))
        if width<height:
            newHeight = 750
            newWidth = newHeight * int((height/width))
            newImg = image.resize((newWidth,newHeight),Image.ANTIALIAS)
        else:
            newWidth = 750
            newHeight = newWidth * int((width/height))
            newImg = image.resize((newWidth,newHeight),Image.ANTIALIAS)
        return newImg
    
    def getKernel(self,name=None):
        kernel = None
        if name == "rectangle":
            kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
        if name == "ellips":
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
        if name == "cross":
            kernel = cv.getStructuringElement(cv.MORPH_CROSS,(5,5))
        if name == "custom":
            kernel = np.ones((self.n,self.n),np.uint8)
        return kernel

    def morphologi(self,operation=None,structuringElement=None):
        print(operation + " " + structuringElement)
        kernel = self.getKernel(structuringElement)
        if operation == "erosi":
            self.morphologiErosi(kernel)
        if operation == "dilasi":
            self.morphologiDilasi(kernel)
        if operation == "opening":
            self.morphologiOpening(kernel)
        if operation == "closing":
            self.morphologiClosing(kernel)

    def refreshImgResult(self,arrImg = None,code=None):
        newImg = Image.fromarray(arrImg)
        img = ImageTk.PhotoImage(self.adjustAspectRatio(newImg))
        self.labelImageResult.configure(image=img,text="")
        self.labelImageResult.image = img
        if code == self.GS_IMG:
            self.procedImage = arrImg
        elif code == self.RGB_IMG:
            rgb2bgr = cv.cvtColor(arrImg,cv.COLOR_RGB2BGR)
            self.procedImage = rgb2bgr


    def setImgResultBGR2RGB(self,imgOperationResult=None):
        newImg = cv.cvtColor(imgOperationResult,cv.COLOR_BGR2RGB)
        self.refreshImgResult(newImg,self.RGB_IMG)

    def morphologiErosi(self,kernel=None):
        imgCV = cv.imread(self.filepath)
        erosi = cv.erode(imgCV,kernel,iterations=1)
        self.setImgResultBGR2RGB(erosi)

    def morphologiDilasi(self,kernel=None):
        imgCV = cv.imread(self.filepath)
        dilasi = cv.dilate(imgCV,kernel,iterations=1)
        self.setImgResultBGR2RGB(dilasi)

    def morphologiOpening(self,kernel=None):
        imgCV = cv.imread(self.filepath)
        opening = cv.morphologyEx(imgCV,cv.MORPH_OPEN,kernel)
        self.setImgResultBGR2RGB(opening)
    
    def morphologiClosing(self,kernel=None):
        imgCV = cv.imread(self.filepath)
        closing = cv.morphologyEx(imgCV,cv.MORPH_CLOSE,kernel)
        self.setImgResultBGR2RGB(closing)

    def canny(self,th=None):
        imgCV = cv.imread(self.filepath)
        grayImg = cv.cvtColor(imgCV,cv.COLOR_BGR2GRAY)
        treshold = th.split("-")
        if len(treshold) != 2:
            print("Inputan tidak valid")
        else:
            lowTresh = int(treshold[0])
            highTresh = int(treshold[1])
            if (lowTresh > 255 or lowTresh < 0) or (highTresh>255 or highTresh< 0):
                print("Inputan tidak valid")
            else:
                cannyImg = cv.Canny(grayImg,lowTresh,highTresh)
                self.refreshImgResult(cannyImg,self.GS_IMG)

    def laplacian(self):
        imgCV = cv.imread(self.filepath)
        grayImg = cv.cvtColor(imgCV,cv.COLOR_BGR2GRAY)
        laplacianImg = cv.Laplacian(grayImg,cv.CV_16U,3)
        absLaplacianImg = cv.convertScaleAbs(laplacianImg)
        self.refreshImgResult(absLaplacianImg,self.GS_IMG)
    
    def grayScale(self):
        imgCV = cv.imread(self.filepath)
        grayImage = cv.cvtColor(imgCV,cv.COLOR_BGR2GRAY)
        self.refreshImgResult(grayImage,self.GS_IMG)

root = Tk()
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.rowconfigure(1,weight=1)

app = Window(root)
root.mainloop()
