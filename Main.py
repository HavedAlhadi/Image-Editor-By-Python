import tkinter as tk # مكتبة أدوات سطح المكتب
from PIL import ImageTk, Image
from LineDetection import D45Degree, Horizontal_D, Vertical_D, _45Degree
from SobelFilter import sobel
import imageEditor as edit
import cv2
from PIL import ImageOps
import numpy as np

from lapalcian import lapalcian


# كلاس فلاتر التنعيم
class SmoothingImages(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("150x250+1328+100")
        self.filter_ = None

        self.parent = parent

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        background_color1 = '#19191a'
        foreground_color = 'sky blue'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="SmoothingImages", background="black", foreground="#ba5a14", font="lucida 11 bold").pack(fill="x")

        filters_frame = tk.Frame(f1, background=background_color1)
        filters_frame.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(f1, background="black", pady=0)
        buttons_frame.pack(fill="both", expand=True)
        
        # avrgblur
        avrgblur_b = tk.Button(filters_frame, text="Main Blur", font="lucida 10 bold", command=lambda: self.filters(avrgblur_b),
                           foreground=foreground_color, background="black", padx=22, cursor="hand2")
        avrgblur_b.bind("<Enter>", lambda e: edit.mouse_hover(button=avrgblur_b))
        avrgblur_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=avrgblur_b))
        avrgblur_b.pack(pady=7)
        
        # Image MedianFilter  
        Medianblur = tk.Button(filters_frame, text="Median Filter", font="lucida 10 bold", command=lambda: self.filters(Medianblur),
                           foreground=foreground_color, background="black", padx=12, cursor="hand2")
        Medianblur.bind("<Enter>", lambda e: edit.mouse_hover(button=Medianblur))
        Medianblur.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Medianblur))
        Medianblur.pack(pady=7)
        
        # Image Gaussian Blur
        blur_b = tk.Button(filters_frame, text="Gaussian Blur", font="lucida 10 bold",
                           command=lambda: self.filters(blur_b), foreground=foreground_color,
                           background="black", padx=10, cursor="hand2")
        blur_b.bind("<Enter>", lambda e: edit.mouse_hover(button=blur_b))
        blur_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=blur_b))
        blur_b.pack(pady=7)


        # Image Bilateral Filter
        bilateral = tk.Button(filters_frame, text="Bilateral Filter", font="lucida 10 bold", command=lambda: self.filters(bilateral),
                           foreground=foreground_color, background="black", padx=8, cursor="hand2")
        bilateral.bind("<Enter>", lambda e: edit.mouse_hover(button=bilateral))
        bilateral.bind("<Leave>", lambda e: edit.mouse_not_hover(button=bilateral))
        bilateral.pack(pady=5)
        
        
        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, background='black',
                             foreground=foreground_color, font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: edit.mouse_hover(button=cancel_b))
        cancel_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=cancel_b))
        cancel_b.pack(side="left")

        apply_b = tk.Button(f1, text="Apply", command=self.apply, background='black', foreground=foreground_color,
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: edit.mouse_hover(button=apply_b))
        apply_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=apply_b))
        apply_b.pack(side="left")

    def filters(self, button):
        self.filter_ = button['text'].lower()

        if self.filter_ == 'bilateral filter':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_avrgblu= cv2.bilateralFilter(My_image,13,91,91)        
            self.modified_img_resized = Image.fromarray(image_avrgblu)
            self.modified_img = Image.fromarray(image_avrgblu)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)
        
        elif self.filter_ == 'main blur':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_avrgblu=cv2.blur(My_image,(13,13))
            # image_avrgblu1=box_blur(My_image,3)                     
            self.modified_img_resized = Image.fromarray(image_avrgblu)
            self.modified_img = Image.fromarray(image_avrgblu)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'median filter':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_avrgblu= cv2.medianBlur(My_image,13)        
            self.modified_img_resized = Image.fromarray(image_avrgblu)
            self.modified_img = Image.fromarray(image_avrgblu)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)
        elif self.filter_ == ' filter':
            self.modified_img = ImageOps.grayscale(self.image_copy)
            self.modified_img_resized = ImageOps.grayscale(self.image_copy_resized)
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'gaussian blur':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_avrgblu= cv2.GaussianBlur(My_image,(13,13),0)        
            self.modified_img_resized = Image.fromarray(image_avrgblu)
            self.modified_img = Image.fromarray(image_avrgblu)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)            
        
    def cancel(self):
        self.grab_release()

        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.grab_release()

        self.parent.image_copy = self.modified_img

        self.parent.image_copy_resized = self.modified_img_resized
        if self.filter_:
            self.parent.save_b.configure(state="normal")

        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()


# كلاس رسم الحواف 
class ScalesEdges(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("150x250+1328+100")
        self.filter_ = None

        self.parent = parent

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        background_color1 = '#19191a'
        foreground_color = 'sky blue'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="Edge Detection", background="black", foreground="#ba5a14", font="lucida 11 bold").pack(fill="x")

        filters_frame = tk.Frame(f1, background=background_color1)
        filters_frame.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(f1, background="black", pady=0)
        buttons_frame.pack(fill="both", expand=True)
        
        #  Laplacian #
        Lap_b = tk.Button(filters_frame, text="Laplacian", font="lucida 12 bold", command=lambda: self.filters(Lap_b),
                           foreground=foreground_color, background="black", padx=8, cursor="hand2")
        Lap_b.bind("<Enter>", lambda e: edit.mouse_hover(button=Lap_b))
        Lap_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Lap_b))
        Lap_b.pack(pady=2)
        
        #  prewitt  
        prewitt_b = tk.Button(filters_frame, text="Prewitt", font="lucida 12 bold", command=lambda: self.filters(prewitt_b),
                           foreground=foreground_color, background="black", padx=18, cursor="hand2")
        prewitt_b.bind("<Enter>", lambda e: edit.mouse_hover(button=prewitt_b))
        prewitt_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=prewitt_b))
        prewitt_b.pack(pady=2)

        #  canny  
        canny_b = tk.Button(filters_frame, text="Canny", font="lucida 12 bold", command=lambda: self.filters(canny_b),
                           foreground=foreground_color, background="black", padx=18, cursor="hand2")
        canny_b.bind("<Enter>", lambda e: edit.mouse_hover(button=canny_b))
        canny_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=canny_b))
        canny_b.pack(pady=2)
        
        # Sobel
        Sobel_b = tk.Button(filters_frame, text="Sobel", font="lucida 12 bold",
                           command=lambda: self.filters(Sobel_b), foreground=foreground_color,
                           background="black", padx=22, cursor="hand2")
        Sobel_b.bind("<Enter>", lambda e: edit.mouse_hover(button=Sobel_b))
        Sobel_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Sobel_b))
        Sobel_b.pack(pady=2)


        # Roberts
        Roberts_b = tk.Button(filters_frame, text="Roberts", font="lucida 12 bold", command=lambda: self.filters(Roberts_b),
                           foreground=foreground_color, background="black", padx=15, cursor="hand2")
        Roberts_b.bind("<Enter>", lambda e: edit.mouse_hover(button=Roberts_b))
        Roberts_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Roberts_b))
        Roberts_b.pack(pady=2)
        
        
        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, background='black',
                             foreground=foreground_color, font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: edit.mouse_hover(button=cancel_b))
        cancel_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=cancel_b))
        cancel_b.pack(side="left")

        apply_b = tk.Button(f1, text="Apply", command=self.apply, background='black', foreground=foreground_color,
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: edit.mouse_hover(button=apply_b))
        apply_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=apply_b))
        apply_b.pack(side="left")

    def filters(self, button):
        self.filter_ = button['text'].lower()

        if self.filter_ == 'laplacian':
            My_image=np.array(self.image_copy.convert('RGB'))            
            # lap=lapalcian(My_image)
            lap = cv2.Laplacian(My_image, cv2.CV_64F)
            lap = np.uint8(np.absolute(lap))
            self.modified_img_resized = Image.fromarray(lap)
            self.modified_img = Image.fromarray(lap)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)
        elif self.filter_ == 'canny':
            My_image=np.array(self.image_copy.convert('RGB'))            
            blur = cv2.GaussianBlur(My_image, (7, 7), 0)
            canny = cv2.Canny(blur, 30, 160)            
            self.modified_img_resized = Image.fromarray(canny)
            self.modified_img = Image.fromarray(canny)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'prewitt':
            My_image=np.array(self.image_copy.convert('RGB'))            
            kernal_prewitt_x=np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
            kernal_prewitt_y=np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
            img_prewitt_x=cv2.filter2D(My_image,-1,kernal_prewitt_x)
            img_prewitt_y=cv2.filter2D(My_image,-1,kernal_prewitt_y)
            img_prewitt = cv2.bitwise_or(img_prewitt_x, img_prewitt_y)            
            self.modified_img_resized = Image.fromarray(img_prewitt)
            self.modified_img = Image.fromarray(img_prewitt)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'sobel':
            My_image=np.array(self.image_copy.convert('RGB'))            
            # Soble=sobel(My_image)
            sobel_x = np.uint8(np.absolute(cv2.Sobel(My_image, cv2.CV_64F, 1, 0)))
            sobel_y = np.uint8(np.absolute(cv2.Sobel(My_image, cv2.CV_64F, 0, 1)))
            Soble = cv2.bitwise_or(sobel_x, sobel_y)
            self.modified_img_resized = Image.fromarray(Soble)
            self.modified_img = Image.fromarray(Soble)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'roberts':
            My_image=np.array(self.image_copy.convert('RGB'))            
            kernal_robert_x=np.array([[0,1],[-1,0]])
            kernal_robert_y=np.array([[1,0],[0,-1]])
            img_robert_x=cv2.filter2D(My_image,0,kernal_robert_x)
            img_robert_y=cv2.filter2D(My_image,0,kernal_robert_y)
            img_robert = cv2.bitwise_or(img_robert_x, img_robert_y)
            self.modified_img_resized = Image.fromarray(img_robert)
            self.modified_img = Image.fromarray(img_robert)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)            
        
    def cancel(self):
        self.grab_release()

        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.grab_release()

        self.parent.image_copy = self.modified_img

        self.parent.image_copy_resized = self.modified_img_resized
        if self.filter_:
            self.parent.save_b.configure(state="normal")

        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()


# كلاس الفلاتر الرمادي والشعاعي والترابي
class Filters(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("150x200+1328+100")
        self.filter_ = None

        self.parent = parent

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        background_color1 = '#19191a'
        foreground_color = 'sky blue'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="Filters", background="black", foreground="#ba5a14", font="lucida 11 bold").pack(fill="x")

        filters_frame = tk.Frame(f1, background=background_color1)
        filters_frame.pack(fill="both", expand=True)
        # نافذة أزرار الفلاتر
        buttons_frame = tk.Frame(f1, background="black", pady=0)
        buttons_frame.pack(fill="both", expand=True)

        emboss_b = tk.Button(filters_frame, text="Emboss", font="lucida 11 bold", command=lambda: self.filters(emboss_b),
                             foreground=foreground_color, background="black", padx=19, cursor="hand2")
        emboss_b.bind("<Enter>", lambda e: edit.mouse_hover(button=emboss_b))
        emboss_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=emboss_b))
        emboss_b.pack(pady=5)

        grey_b = tk.Button(filters_frame, text="Grey", font="lucida 11 bold", command=lambda: self.filters(grey_b),
                           foreground=foreground_color, background="black", padx=30, cursor="hand2")
        grey_b.bind("<Enter>", lambda e: edit.mouse_hover(button=grey_b))
        grey_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=grey_b))
        grey_b.pack(pady=5)

        negative_b = tk.Button(filters_frame, text="Negative", font="lucida 11 bold",
                               command=lambda: self.filters(negative_b), foreground=foreground_color,
                               background="black", padx=16, cursor="hand2")
        negative_b.bind("<Enter>", lambda e: edit.mouse_hover(button=negative_b))
        negative_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=negative_b))
        negative_b.pack(pady=5)

        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, background='black',
                             foreground=foreground_color, font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: edit.mouse_hover(button=cancel_b))
        cancel_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=cancel_b))
        cancel_b.pack(side="left")

        apply_b = tk.Button(f1, text="Apply", command=self.apply, background='black', foreground=foreground_color,
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: edit.mouse_hover(button=apply_b))
        apply_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=apply_b))
        apply_b.pack(side="left")

    def filters(self, button):
        self.filter_ = button['text'].lower()

        if self.filter_ == 'emboss':
            My_image=np.array(self.image_copy.convert('RGB'))
            height, width = My_image.shape[:2]
            y = np.ones((height, width), np.uint8) * 128
            output = np.zeros((height, width), np.uint8)
            kernel1 = np.array([[0, -1, -1], # kernel for embossing bottom left side
                    [1, 0, -1],
                    [1, 1, 0]])
            kernel2 = np.array([[-1, -1, 0], # kernel for embossing bottom right side
                    [-1, 0, 1],
                    [0, 1, 1]])
            gray = cv2.cvtColor(My_image, cv2.COLOR_BGR2GRAY)
            output1 = cv2.add(cv2.filter2D(gray, -1, kernel1), y) # emboss on bottom left side
            output2 = cv2.add(cv2.filter2D(gray, -1, kernel2), y)
            for i in range(height):
              for j in range(width):
                 output[i, j] = max(output1[i, j], output2[i, j]) 
            self.modified_img_resized = Image.fromarray(output)
            self.modified_img = Image.fromarray(output)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'negative':
            My_image=np.array(self.image_copy.convert('RGB'))
            negative=255-My_image
            self.modified_img_resized = Image.fromarray(negative)
            self.modified_img = Image.fromarray(negative)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == 'grey':
            My_image=np.array(self.image_copy.convert('RGB'))
            gray=cv2.cvtColor(My_image, cv2.COLOR_BGR2GRAY)
            self.modified_img_resized = Image.fromarray(gray)
            self.modified_img = Image.fromarray(gray)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

    def cancel(self):
        self.grab_release()
        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.grab_release()
        self.parent.image_copy = self.modified_img
        self.parent.image_copy_resized = self.modified_img_resized
        if self.filter_:
            self.parent.save_b.configure(state="normal")
        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

#class filter Line Detection
class LineDetection(tk.Toplevel):
    def __init__(self, parent, image_copy, modified_img, image_copy_resized, modified_img_resized):
        super().__init__(parent)

        self.configure(background="grey")
        self.wm_overrideredirect(True)
        self.grab_set()
        self.winfo_parent()
        self.geometry("150x250+1328+100")
        self.filter_ = None

        self.parent = parent

        self.image_copy = image_copy
        self.modified_img = modified_img

        self.image_copy_resized = image_copy_resized
        self.modified_img_resized = modified_img_resized

        background_color1 = '#19191a'
        foreground_color = 'sky blue'

        f1 = tk.Frame(self, background=background_color1)
        f1.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(f1, text="LineDetection", background="black", foreground="#ba5a14", font="lucida 11 bold").pack(fill="x")

        filters_frame = tk.Frame(f1, background=background_color1)
        filters_frame.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(f1, background="black", pady=0)
        buttons_frame.pack(fill="both", expand=True)
        
        # Filter Vertical
        Vertical = tk.Button(filters_frame, text="Vertical", font="lucida 10 bold", command=lambda: self.filters(Vertical),
                           foreground=foreground_color, background="black", padx=22, cursor="hand2")
        Vertical.bind("<Enter>", lambda e: edit.mouse_hover(button=Vertical))
        Vertical.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Vertical))
        Vertical.pack(pady=7)
        
        # Filter Horizontal  
        Horizontal = tk.Button(filters_frame, text="Horizontal", font="lucida 10 bold", command=lambda: self.filters(Horizontal),
                           foreground=foreground_color, background="black", padx=12, cursor="hand2")
        Horizontal.bind("<Enter>", lambda e: edit.mouse_hover(button=Horizontal))
        Horizontal.bind("<Leave>", lambda e: edit.mouse_not_hover(button=Horizontal))
        Horizontal.pack(pady=7)
        
        # Filter 45 Degree
        D45Degree = tk.Button(filters_frame, text="45 Degree", font="lucida 10 bold",
                           command=lambda: self.filters(D45Degree), foreground=foreground_color,
                           background="black", padx=15, cursor="hand2")
        D45Degree.bind("<Enter>", lambda e: edit.mouse_hover(button=D45Degree))
        D45Degree.bind("<Leave>", lambda e: edit.mouse_not_hover(button=D45Degree))
        D45Degree.pack(pady=7)


        # Filter _45Degree
        _45Degree = tk.Button(filters_frame, text="-45 Degree", font="lucida 10 bold", command=lambda: self.filters(_45Degree),
                           foreground=foreground_color, background="black", padx=12, cursor="hand2")
        _45Degree.bind("<Enter>", lambda e: edit.mouse_hover(button=_45Degree))
        _45Degree.bind("<Leave>", lambda e: edit.mouse_not_hover(button=_45Degree))
        _45Degree.pack(pady=5)
        
        
        cancel_b = tk.Button(f1, text="Cancel", command=self.cancel, background='black',
                             foreground=foreground_color, font="lucida 12 bold", cursor="hand2")
        cancel_b.bind("<Enter>", lambda e: edit.mouse_hover(button=cancel_b))
        cancel_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=cancel_b))
        cancel_b.pack(side="left")

        apply_b = tk.Button(f1, text="Apply", command=self.apply, background='black', foreground=foreground_color,
                            font="lucida 12 bold", padx=8, cursor="hand2")
        apply_b.bind("<Enter>", lambda e: edit.mouse_hover(button=apply_b))
        apply_b.bind("<Leave>", lambda e: edit.mouse_not_hover(button=apply_b))
        apply_b.pack(side="left")

    def filters(self, button):
        self.filter_ = button['text'].lower()

        if self.filter_ == 'horizontal':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_Horizontal=Horizontal_D(My_image)            
            self.modified_img_resized = Image.fromarray(image_Horizontal)
            self.modified_img = Image.fromarray(image_Horizontal)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)
        
        elif self.filter_ == 'vertical':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_vertical=Vertical_D(My_image)            
            self.modified_img_resized = Image.fromarray(image_vertical)
            self.modified_img = Image.fromarray(image_vertical)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == '45 degree':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_d45degree=D45Degree(My_image)            
            self.modified_img_resized = Image.fromarray(image_d45degree)
            self.modified_img = Image.fromarray(image_d45degree)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)

        elif self.filter_ == '-45 degree':
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_d45degree=_45Degree(My_image)            
            self.modified_img_resized = Image.fromarray(image_d45degree)
            self.modified_img = Image.fromarray(image_d45degree)          
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.parent.show_image(modified=im)
        
    def cancel(self):
        self.grab_release()

        im = ImageTk.PhotoImage(self.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()

    def apply(self):
        self.grab_release()

        self.parent.image_copy = self.modified_img

        self.parent.image_copy_resized = self.modified_img_resized
        if self.filter_:
            self.parent.save_b.configure(state="normal")

        im = ImageTk.PhotoImage(self.parent.image_copy_resized)
        self.parent.show_image(modified=im)
        self.destroy()
