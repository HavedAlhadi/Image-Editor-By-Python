import time
import tkinter as tk # مكتبة أدوات سطح المكتب
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import filedialog
import webbrowser

from PIL import ImageTk, Image
import PIL
import imagehash

from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter

import cv2
import os
from PIL import ImageOps
import numpy as np

import Main as fl



Camera_vindow="Camera"
class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        # code for the splash screen
        #  شاشة البداية
        self.wm_overrideredirect(1)
        self.configure(background="black")

        window_width, window_height = 500, 320
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x_co = int(screen_width / 2 - window_width / 2)
        y_co = int(screen_height / 2 - window_height / 2) - 50



        self.loading_label = None

        self.geometry(f"{window_width}x{window_height}+{x_co}+{y_co}")

        self.splash_frame = tk.Frame(self, background="black")
        self.splash_frame.pack(fill="both", expand=True)

        self.image_editor_window = tk.Frame(self)

        wallpaper = Image.open('images_ie/splash.jpg')
        wallpaper = wallpaper.resize((window_width, window_height - 30), Image.ANTIALIAS)
        wallpaper = ImageTk.PhotoImage(wallpaper)

        self.loading = Image.open('images_ie/loding.png')
        self.loading = self.loading.resize((19, 19), Image.ANTIALIAS)
        self.loading = ImageTk.PhotoImage(self.loading)

        self.wallpaper_label = tk.Label(self, image=wallpaper, bd=0)
        self.wallpaper_label.place(x=0, y=0)

        self.delay = 100

        self.developer_label = tk.Label(self, text='Developed by Haved', foreground="white",
                                        font="lucida 10 bold", background='#1e2329')
        self.developer_label.place(x=350, y=260)

        self.x = 8

        # code for the image editor
        
        self.button_background = 'grey'
        self.original_image_resized = None
        self.image_copy_resized = None
        self.modified_img_resized = None
        self.image_before_draw = None
        self.draw_active = False
        self.crop_active = False
        self.mirrored = False
        self.current_index = None
        self.image_paths = []
        self.lines_drawn = []
        self.current_image_size = None
        self.current_resized_image_size = None
        self.original_image = None
        self.modified_img = None
        self.image_copy = None
        self.rect = None
        self.event_x = self.event_y = None 
        self.rectangles = []
        self.point_x = self.point_y = None
        self.image_x_co = self.image_y_co = None
        self.original_hash = None

        self.max_height = 812
        self.max_width = 1220

        self.degree = 90
        self.error = None

        # ____________________________icons
        flip_icon = Image.open('images_ie/flip2_ie.png')
        flip_icon = flip_icon.resize((25, 25), Image.ANTIALIAS)
        flip_icon = ImageTk.PhotoImage(flip_icon)

        rotate_icon = Image.open('images_ie/rotate_ie.png')
        rotate_icon = rotate_icon.resize((25, 25), Image.ANTIALIAS)
        rotate_icon = ImageTk.PhotoImage(rotate_icon)


        next_icon = Image.open('images_ie/right_ie.png')
        next_icon = next_icon.resize((25, 25), Image.ANTIALIAS)
        next_icon = ImageTk.PhotoImage(next_icon)

        previous_icon = Image.open('images_ie/left_ie.png')
        previous_icon = previous_icon.resize((25, 25), Image.ANTIALIAS)
        previous_icon = ImageTk.PhotoImage(previous_icon)

        adjust_icon = Image.open('images_ie/adjust_ie.png')
        adjust_icon = adjust_icon.resize((25, 25), Image.ANTIALIAS)
        adjust_icon = ImageTk.PhotoImage(adjust_icon)

        filter_icon = Image.open('images_ie/filter_ie.png')
        filter_icon = filter_icon.resize((25, 25), Image.ANTIALIAS)
        filter_icon = ImageTk.PhotoImage(filter_icon)

        filtere_icon = Image.open('images_ie/flter.png')
        filtere_icon = filtere_icon.resize((25, 25), Image.ANTIALIAS)
        filtere_icon = ImageTk.PhotoImage(filtere_icon)

        Smoothing_icon = Image.open('images_ie/smoothing.png')
        Smoothing_icon = Smoothing_icon.resize((25, 25), Image.ANTIALIAS)
        Smoothing_icon = ImageTk.PhotoImage(Smoothing_icon)
                
        save_icon = Image.open('images_ie/save_ie.png')
        save_icon = save_icon.resize((25, 25), Image.ANTIALIAS)
        save_icon = ImageTk.PhotoImage(save_icon)

        edges_icon = Image.open('images_ie/edges_ie.png')
        edges_icon = edges_icon.resize((25, 25), Image.ANTIALIAS)
        edges_icon = ImageTk.PhotoImage(edges_icon)

        delete_icon = Image.open('images_ie/delete_ie.png')
        delete_icon = delete_icon.resize((25, 25), Image.ANTIALIAS)
        delete_icon = ImageTk.PhotoImage(delete_icon)

        power_off_icon = Image.open('images_ie/power-button_ie.png')
        power_off_icon = power_off_icon.resize((25, 25), Image.ANTIALIAS)
        power_off_icon = ImageTk.PhotoImage(power_off_icon)

        self.error_icon = Image.open('images_ie/error_ie.png')
        self.error_icon = self.error_icon.resize((50, 50), Image.ANTIALIAS)
        self.error_icon = ImageTk.PhotoImage(self.error_icon)

        self.open_image_icon = Image.open('images_ie/open_image_ie.png')
        self.open_image_icon = self.open_image_icon.resize((150, 120), Image.ANTIALIAS)
        self.open_image_icon = ImageTk.PhotoImage(self.open_image_icon)
        
        self.open_camera_icon = Image.open('images_ie/open_camera_ie.png')
        self.open_camera_icon = self.open_camera_icon.resize((150, 120), Image.ANTIALIAS)
        self.open_camera_icon = ImageTk.PhotoImage(self.open_camera_icon)

        self.open_camera_small_icon = Image.open('images_ie/open_camera_ie.png')
        self.open_camera_small_icon = self.open_camera_small_icon.resize((50, 40), Image.ANTIALIAS)
        self.open_camera_small_icon = ImageTk.PhotoImage(self.open_camera_small_icon)

        self.open_camera_video_icon = Image.open('images_ie/open_vedio_ie.png')
        self.open_camera_video_icon = self.open_camera_video_icon.resize((150, 120), Image.ANTIALIAS)
        self.open_camera_video_icon = ImageTk.PhotoImage(self.open_camera_video_icon)
        
        self.open_camera_video_small_icon = Image.open('images_ie/open_vedio_ie.png')
        self.open_camera_video_small_icon = self.open_camera_video_small_icon.resize((50, 40), Image.ANTIALIAS)
        self.open_camera_video_small_icon = ImageTk.PhotoImage(self.open_camera_video_small_icon)

        self.open_image_small_icon = Image.open('images_ie/open_image_ie.png')
        self.open_image_small_icon = self.open_image_small_icon.resize((50, 40), Image.ANTIALIAS)
        self.open_image_small_icon = ImageTk.PhotoImage(self.open_image_small_icon)

        self.checked_icon = Image.open('images_ie/checked_ie.png')
        self.checked_icon = self.checked_icon.resize((25, 25), Image.ANTIALIAS)
        self.checked_icon = ImageTk.PhotoImage(self.checked_icon)

        self.unchecked_icon = Image.open('images_ie/unchecked_ie.png')
        self.unchecked_icon = self.unchecked_icon.resize((25, 25), Image.ANTIALIAS)
        self.unchecked_icon = ImageTk.PhotoImage(self.unchecked_icon)

        reset_icon = Image.open('images_ie/reset_ie.png')
        reset_icon = reset_icon.resize((25, 25), Image.ANTIALIAS)
        reset_icon = ImageTk.PhotoImage(reset_icon)

        color_picker_icon = Image.open('images_ie/color_picker_ie.png')
        color_picker_icon = color_picker_icon.resize((25, 25), Image.ANTIALIAS)
        color_picker_icon = ImageTk.PhotoImage(color_picker_icon)
        #End ____________________________icons
        heading = tk.Label(self.image_editor_window, text="Image Editor", background="sky blue", font="lucida 9 bold")
        heading.pack(fill="x")

        # DaweWindow
        self.image_canvas = tk.Canvas(self.image_editor_window, bd=0, highlightbackground="black", background="black")
        self.image_canvas.bind('<B1-Motion>', self.draw_crop)
        self.image_canvas.bind('<ButtonPress-1>', self.get_mouse_pos)
        self.image_canvas.bind('<ButtonRelease-1>', self.button_release)
        self.image_canvas.pack(fill="both", expand=True)

        self.button_frame_color = "#333331"
        # نافذة أزرار التنقل
        self.button_frame2 = tk.Frame(self.image_editor_window, background=self.button_frame_color)
        self.button_frame2.pack(fill="x")

        self.button_frame = tk.Frame(self.button_frame2, background=self.button_frame_color)
        self.button_frame.pack()

        # #########################3Buttouns
        
        previous_b = tk.Button(self.button_frame, text="Previous", image=previous_icon,
                               background=self.button_frame_color, command=self.previous_image,
                               padx=5, bd=0, cursor="hand2")
        previous_b.bind("<Enter>", lambda e: mouse_hover(previous_b, color='#1c1c1b'))
        previous_b.bind("<Leave>", lambda e: mouse_not_hover(previous_b, color=self.button_frame_color))
        previous_b.pack(side="left", padx=2)

        rotate_b = tk.Button(self.button_frame, text="Rotate", image=rotate_icon, background=self.button_frame_color,
                             command=self.rotate, padx=5, bd=0, cursor="hand2")
        rotate_b.bind("<Enter>", lambda e: mouse_hover(rotate_b, color='#1c1c1b'))
        rotate_b.bind("<Leave>", lambda e: mouse_not_hover(rotate_b, color=self.button_frame_color))
        rotate_b.pack(side="left", padx=10)

        flip_b = tk.Button(self.button_frame, text="Flip", background=self.button_frame_color,
                           image=flip_icon, command=self.mirror, padx=5, bd=0, cursor="hand2")
        flip_b.bind("<Enter>", lambda e: mouse_hover(flip_b, color='#1c1c1b'))
        flip_b.bind("<Leave>", lambda e: mouse_not_hover(flip_b, color=self.button_frame_color))
        flip_b.pack(side="left", padx=10)

        self.delete_b = tk.Button(self.button_frame, text="Flip", background=self.button_frame_color, image=delete_icon,
                                  command=self.delete,
                                  padx=5, bd=0, cursor="hand2", state="disable")
        self.delete_b.bind("<Enter>", lambda e: mouse_hover(self.delete_b, color='#1c1c1b'))
        self.delete_b.bind("<Leave>", lambda e: mouse_not_hover(self.delete_b, color=self.button_frame_color))
        self.delete_b.pack(side="left", padx=10)

        next_b = tk.Button(self.button_frame, text="Next", image=next_icon, command=self.next_image,
                           background=self.button_frame_color, padx=5, bd=0, cursor="hand2")
        next_b.bind("<Enter>", lambda e: mouse_hover(next_b, color='#1c1c1b'))
        next_b.bind("<Leave>", lambda e: mouse_not_hover(next_b, color=self.button_frame_color))
        next_b.pack(side="left", padx=2)

        exit_window = tk.Button(self.image_editor_window, image=power_off_icon, compound="left",
                                text="Exit", font="lucida 9 bold", foreground='white', background="black",
                                command=self.exit_window, padx=12, cursor="hand2")
        exit_window.bind("<Enter>", lambda e: mouse_hover(exit_window))
        exit_window.bind("<Leave>", lambda e: mouse_not_hover(exit_window))
        exit_window.place(x=1430, y=50)

        # نافذة أزرار التعديل
        self.side_frame = tk.Frame(self.image_editor_window, background="black")

        adjust_b = tk.Button(self.side_frame, text="Adjust", foreground="white", compound="left", font="lucida 9 bold",
                             image=adjust_icon, background="black", cursor="hand2",
                             command=self.open_adjustment_window,
                              padx=25
                             )
        adjust_b.bind("<Enter>", lambda e: mouse_hover(adjust_b))
        adjust_b.bind("<Leave>", lambda e: mouse_not_hover(adjust_b))
        adjust_b.pack(pady=5)

        filter_A = tk.Button(self.side_frame, text="Filters", foreground="white", compound="left",
                             font="lucida 9 bold", image=filter_icon, background="black", cursor="hand2",
                            command=self.open_filter_window,
                              padx=26
                             )
        filter_A.bind("<Enter>", lambda e: mouse_hover(filter_A))
        filter_A.bind("<Leave>", lambda e: mouse_not_hover(filter_A))
        filter_A.pack(pady=5)

        filter_b = tk.Button(self.side_frame, text="Smoothing", foreground="white", compound="left",
                             font="lucida 9 bold", image=Smoothing_icon, background="black", cursor="hand2",
                            command=self.open_SmoothingImages_window,
                              padx=18
                             )
        filter_b.bind("<Enter>", lambda e: mouse_hover(filter_b))
        filter_b.bind("<Leave>", lambda e: mouse_not_hover(filter_b))
        filter_b.pack(pady=5)

        filter_E = tk.Button(self.side_frame, text="Edge Detection", foreground="white", compound="left",
                             font="lucida 9 bold", image=filtere_icon, background="black", cursor="hand2",
                            command=self.open_s_edges_window,
                              padx=9
                             )
        filter_E.bind("<Enter>", lambda e: mouse_hover(filter_E))
        filter_E.bind("<Leave>", lambda e: mouse_not_hover(filter_E))
        filter_E.pack(pady=5)
        
        filter_L = tk.Button(self.side_frame, text="Line Detection", foreground="white", compound="left",
                             font="lucida 9 bold", image=filter_icon, background="black", cursor="hand2",
                            command=self.open_Detection_line,
                              padx=9
                             )
        filter_L.bind("<Enter>", lambda e: mouse_hover(filter_L))
        filter_L.bind("<Leave>", lambda e: mouse_not_hover(filter_L))
        filter_L.pack(pady=5)


        self.reset_b = tk.Button(self.image_editor_window, text="Reset", foreground="white", compound="left",
                                 font="lucida 9 bold", image=reset_icon, background="black",
                                 command=self.reset, padx=26, cursor="hand2")
        self.reset_b.bind("<Enter>", lambda e: mouse_hover(self.reset_b))
        self.reset_b.bind("<Leave>", lambda e: mouse_not_hover(self.reset_b))

        self.draw_b = tk.Button(self.image_editor_window, text="Draw", image=self.unchecked_icon, foreground="white",
                                font="lucida 9 bold", compound="left", background="black", command=self.activate_draw,
                                padx=3, cursor="hand2")
        self.draw_b.bind("<Enter>", lambda e: mouse_hover(self.draw_b))
        self.draw_b.bind("<Leave>", lambda e: mouse_not_hover(self.draw_b))

        self.crop_b = tk.Button(self.image_editor_window, text="Crop", image=self.unchecked_icon, foreground="white",
                                font="lucida 9 bold", compound="left", background="black",
                                command=self.activate_crop, padx=4, cursor="hand2")
        self.crop_b.bind("<Enter>", lambda e: mouse_hover(self.crop_b))
        self.crop_b.bind("<Leave>", lambda e: mouse_not_hover(self.crop_b))

        self.crop_save = tk.Button(self.image_editor_window, image=save_icon, compound='left', text="Save",
                                   foreground="white", font="lucida 9 bold", background="black",
                                   command=self.crop_image, padx=4, cursor="hand2")
        self.crop_save.bind("<Enter>", lambda e: mouse_hover(self.crop_save))
        self.crop_save.bind("<Leave>", lambda e: mouse_not_hover(self.crop_save))

        self.edges = tk.Button(self.image_editor_window, text="Draw Edges", foreground="white", compound="left",
                                font="lucida 9 bold", state='disabled', image=edges_icon, background="black",
                                command=self.edgesFun, padx=15, cursor="hand2")
        
        self.save_b = tk.Button(self.image_editor_window, text="Save image", foreground="white", compound="left",
                                font="lucida 9 bold", state='disable', image=save_icon, background="black",
                                command=self.save, padx=15, cursor="hand2")

        self.draw_save = tk.Button(self.image_editor_window, image=save_icon, compound='left', text="Save",
                                   foreground="white", font="lucida 10 bold", background="black",
                                   command=self.image_after_draw, padx=3, cursor="hand2")
        self.draw_save.bind("<Enter>", lambda e: mouse_hover(self.draw_save))
        self.draw_save.bind("<Leave>", lambda e: mouse_not_hover(self.draw_save))
        # #########################end Buttons
        
        version_label = tk.Label(self.button_frame2,text="By-Alhadi    v 1.0", background=self.button_frame_color,
                                   foreground="white", font="lucida 9 bold")
        version_label.place(x=20)
          
        # #########################أزرار الواجهة الرئيسية 
        self.status_bar = tk.Label(self.button_frame2, background=self.button_frame_color,
                                   foreground="white", font="lucida 10 bold")
        self.status_bar.place(x=1200)       
        
        self.open_camera_button = tk.Button(self.image_editor_window, command=self.open_camera, cursor="hand2",
                                           image=self.open_camera_icon, compound='top', text="Click To Open Camera",
                                           font="lucida 12 bold", foreground="white", bd=0, background="black",)
        self.open_camera_button.bind("<Enter>", lambda e: mouse_hover(self.open_camera_button, color='#1c1c1b'))
        self.open_camera_button.bind("<Leave>", lambda e: mouse_not_hover(self.open_camera_button))
        self.open_camera_button.place(x=389, y=350)

        self.open_camera_video_button = tk.Button(self.image_editor_window, command=self.open_camera_vedio, cursor="hand2",
                                           image=self.open_camera_video_icon, compound='top', text="Click To Regrsiter Video",
                                           font="lucida 12 bold", foreground="white", bd=0, background="black",)
        self.open_camera_video_button.bind("<Enter>", lambda e: mouse_hover(self.open_camera_video_button, color='#1c1c1b'))
        self.open_camera_video_button.bind("<Leave>", lambda e: mouse_not_hover(self.open_camera_video_button))
        self.open_camera_video_button.place(x=689, y=350)
       

        self.open_image_button = tk.Button(self.image_editor_window, command=self.open_image, cursor="hand2",
                                           image=self.open_image_icon, compound='top', text="Click To Open Image",
                                           font="lucida 12 bold", foreground="white", bd=0, background="black",)
        self.open_image_button.bind("<Enter>", lambda e: mouse_hover(self.open_image_button, color='#1c1c1b'))
        self.open_image_button.bind("<Leave>", lambda e: mouse_not_hover(self.open_image_button))
        self.open_image_button.place(x=989, y=350)

        self.error_b = tk.Button(self.image_editor_window, text="It appears that we don't support this file format.",
                                 image=self.error_icon, compound="left", font="lucida 11 bold",
                                 background="black", foreground="white", bd=0, padx=5)
        
        # #########################end Buttons

        self.pencil_size = 2
        self.pencil_color = 'blue'

        self.pencil_size_label = tk.Label(self.image_editor_window, text="Size", font="lucida 10 bold",
                                          background='black', foreground="white")

        self.pencil_size_scale = tk.Scale(self.image_editor_window, from_=1, to=15, sliderrelief='flat',
                                          orient="horizontal", fg='white', highlightthickness=0,
                                          command=self.change_pencil_size, cursor="hand2", background='black',
                                          troughcolor='#73B5FA', activebackground='#1065BF')

        self.color_chooser_button = tk.Button(self.image_editor_window, image=color_picker_icon, text="Color",
                                              font="lucida 10 bold", cursor="hand2", background='black',
                                              foreground="white", bd=0, command=self.choose_color)
        self.color_chooser_button.bind("<Enter>", lambda e: mouse_hover(self.color_chooser_button))
        self.color_chooser_button.bind("<Leave>", lambda e: mouse_not_hover(self.color_chooser_button))

        self.img2 = None
        self.start_time = time.time()

        self.show_splash_screen()
        self.mainloop()

    def show_splash_screen(self):
        # بروقرس بار 
        self.loading_label = tk.Label(self.splash_frame, image=self.loading, bd=0)
        self.loading_label.place(x=self.x, y=294)
        self.x += 22
        if self.x != 470:
            self.after(self.delay, self.show_splash_screen)
        else:
            self.developer_label.destroy()
            self.splash_frame.destroy()
            self.loading_label.destroy()
            self.wallpaper_label.destroy()
            self.wm_overrideredirect(0)
            self.image_editor_window.pack(fill="both", expand=True)
            self.wm_attributes('-fullscreen', True)

    def change_pencil_size(self, size):
        self.pencil_size = int(size)

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor='red')
        if color[0]:
            self.pencil_color = color[1]
    
    def FormatButton(self):
        self.open_image_button.configure(image=self.open_image_small_icon, text="Open Image", compound="left",
                                            font="lucida 9 bold")
        self.open_camera_button.configure(image=self.open_camera_small_icon, text="Open Camera", compound="left",
                                            font="lucida 9 bold")
        self.open_camera_video_button.configure(image=self.open_camera_video_small_icon, text="register video", compound="left",
                                            font="lucida 9 bold")
        self.open_image_button.place(x=1380, y=670)
        self.open_camera_button.place(x=1380, y=710)
        self.open_camera_video_button.place(x=1380, y=760)
        self.side_frame.place(x=1380, y=114)
        self.save_b.place(x=1380, y=630)
        self.edges.place(x=1380, y=530)
        self.draw_b.place(x=1455, y=440)
        self.crop_b.place(x=1380, y=440)
        self.reset_b.place(x=1380, y=340)
        self.edges.configure(state="normal")
        self.delete_b.configure(state="normal")
        # self.save_b.configure(state="normal")

    # فتح صورة
    def open_image(self):
        file_object = filedialog.askopenfile(filetype=(('jpg', '*.jpg'), ('png', '*.png')))
        if file_object:

            self.FormatButton()
            filename = file_object.name
            directory = filename.replace(os.path.basename(filename), "")
            files_list = os.listdir(directory)

            self.image_paths = []
            for file in files_list:
                if '.jpg' in file or '.png' in file or '.JPG' in file or '.JPEG' in file or '.PNG' in file:
                    self.image_paths.append(os.path.join(directory, file))

            for i, image in enumerate(self.image_paths):
                if image == filename:
                    self.current_index = i
            self.show_image(image=self.image_paths[self.current_index])
            

    def resize_image(self, image):
        image.thumbnail((self.max_width, self.max_height))

        self.original_hash = imagehash.average_hash(image)

        self.current_resized_image_size = (image.size[0], image.size[1])
        return image

    def photo_image_object(self, image):
        self.original_image = Image.open(image)
        self.current_image_size = self.original_image.size
        self.modified_img = self.original_image
        self.image_copy = self.original_image

        self.original_image_resized = Image.open(image)

        self.modified_img_resized = self.original_image_resized
        self.image_copy_resized = self.original_image_resized

        im = self.resize_image(self.original_image_resized)
        im = ImageTk.PhotoImage(im)
        return im
    
    def open_camera(self):
        image= cv2.VideoCapture(0)
        while True:
            ret,frame=image.read()
            frame=cv2.resize(frame,(800,500))                               
            cv2.imshow("Click on key -s- to Save or -q- to exit",frame)            
            if cv2.waitKey(1)& 0xFF==ord('s'):
                cv2.imwrite('Camera\image\imageHaved.png',frame) 
                break
            if cv2.waitKey(1)& 0xFF==ord('q'):
                break
        image.release
        cv2.destroyAllWindows()      

    def open_camera_vedio(self):
        Video= cv2.VideoCapture(0)
        while True:
            ret,frame=Video.read()
            cv2.imshow('Click on key -v- to starte or -q- to exit  ',frame)
            if cv2.waitKey(1)& 0xFF==ord('v'):
                break
            # elif cv2.waitKey(1)& 0xFF==ord('q'):
            #     return
            #     cv2.destroyAllWindows()
        codec=cv2.VideoWriter_fourcc(*'mp4v')
        fps=int(Video.get(cv2.CAP_PROP_FPS))
        frame_num=int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
        w=int(Video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h=int(Video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        colored_vidoe=True
        writer=cv2.VideoWriter('Camera\/video\haved.mp4',codec,fps,(w,h),colored_vidoe)
        while Video.isOpened():
            ret,frame=Video.read()
            # frame=cv2.resize(frame,(800,500))
            key=cv2.waitKey(1)
            if key& 0xFF==ord('q'):
                break
            cv2.imshow('video',frame)
            writer.write(frame)
        writer.release()
        Video.release()
        cv2.destroyAllWindows()
        webbrowser.open('haved.mp4')


    def show_image(self, image=None, modified=None):
        self.status_bar.configure(text=f"Image  :  {self.current_index + 1}  of  {len(self.image_paths)}")
        if self.error:
            self.error_b.place_forget()
            self.error = None

        im = None
        if image:
            try:
                im = self.photo_image_object(image)
            except:
                self.image_copy = self.modified_img = self.original_image_resized = self.original_image = None
                self.image_canvas.image = ''
                self.error_b.place(x=600, y=380)
                self.error = True
                return

        elif modified:
            im = modified

        image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
        self.image_x_co, self.image_y_co = (self.winfo_screenwidth() / 2) - image_width / 2, (
                self.max_height / 2) - image_height / 2
        self.image_canvas.image = im        
        if image_height < self.max_height:
            self.image_canvas.create_image(self.image_x_co, self.image_y_co, image=im, anchor="nw")
        else:
            self.image_canvas.create_image(self.image_x_co, 0, image=im, anchor="nw")
        cv2.imshow("dsf",self.photo_image_object(image))    

    def previous_image(self):
        if self.image_paths:
            self.save_b.configure(state="disable")

            if self.current_index != 0:
                self.current_index -= 1
            self.show_image(image=self.image_paths[self.current_index])

            self.delete_b.configure(state="normal")

    def next_image(self):
        if self.image_paths:
            self.save_b.configure(state="disable")

            if self.current_index != len(self.image_paths) - 1:
                self.current_index += 1
            self.show_image(image=self.image_paths[self.current_index])

            self.delete_b.configure(state="normal")

    # دالة التدوير 
    def rotate(self):
        if self.original_image and not self.error:                                   
            My_image=np.array(self.image_copy.convert('RGB'))            
            center=map(lambda x:x //2,My_image.shape[1::-1])
            m=cv2.getRotationMatrix2D(tuple(center),-self.degree,float(1))
            rotatt=cv2.warpAffine(My_image,m,(My_image.shape[1],My_image.shape[0]))            
            self.modified_img_resized = Image.fromarray(rotatt)
            self.modified_img = Image.fromarray(rotatt)
            self.image_copy = self.modified_img          
            self.compare_images()
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.show_image(modified=im)
            self.compare_images()            
            

    # دالة قلب الصورة
    def mirror(self):
        if self.original_image and not self.error:            
            My_image=np.array(self.image_copy.convert('RGB'))            
            image_flip=cv2.flip(My_image,1)
            self.modified_img_resized = Image.fromarray(image_flip)
            self.modified_img = Image.fromarray(image_flip)
            self.image_copy = self.modified_img          
            self.compare_images()
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.show_image(modified=im)
            self.compare_images()
   

    def get_mouse_pos(self, event):
        if not self.draw_active and self.crop_active:
            if self.rect:
                self.rectangles = []
                self.image_canvas.delete(self.rect)

            self.rect = self.image_canvas.create_rectangle(0, 0, 0, 0, outline="black", width=3)

        self.point_x, self.point_y = event.x, event.y

    def button_release(self, event):
        if self.crop_active:
            self.crop_save.place(x=1455, y=440)

    def activate_draw(self):
        if self.original_image and not self.error:
            if not self.draw_active:
                self.image_before_draw = Image.new('RGB', size=self.current_image_size)
                self.image_before_draw.paste(self.image_copy, (0, 0))
                self.pencil_size_label.place(x=1388, y=390)
                self.pencil_size_scale.place(x=1425, y=390)
                self.color_chooser_button.place(x=1430, y=490)
                self.image_canvas.configure(cursor='pencil')
                self.draw_save.place(x=1380, y=440)
                self.draw_b.configure(image=self.checked_icon)
                self.button_frame.pack_forget()
                self.side_frame.place_forget()
                self.FormatButton()

                print("draw activated..")
                self.draw_active = True
            else:
                if self.lines_drawn:
                    for line in self.lines_drawn:
                        self.image_canvas.delete(line)
                    self.lines_drawn = []
                    self.image_before_draw = None
                    self.image_before_draw = self.image_copy

                self.image_canvas.configure(cursor='arrow')
                self.draw_b.configure(image=self.unchecked_icon)
                print("draw deactivated..")
                self.draw_active = False
                self.button_frame.pack()
                self.FormatButton()
                self.pencil_size_label.place_forget()
                self.pencil_size_scale.place_forget()
                self.color_chooser_button.place_forget()
                self.draw_save.place_forget()

    def activate_crop(self):
        if self.original_image and not self.error:
            if self.draw_active:
                self.activate_draw()

            if not self.crop_active:
                self.crop_b.configure(image=self.checked_icon)
                self.image_canvas.configure(cursor='plus')
                self.crop_active = True
                # self.reset_b.place_forget()
                # self.button_frame.pack_forget()
                # self.side_frame.place_forget()
                self.draw_b.place_forget()
                # self.save_b.place_forget()
                

            else:
                self.image_canvas.configure(cursor='arrow')
                self.crop_b.configure(image=self.unchecked_icon)
                self.crop_save.place_forget()
                if self.rect:
                    self.image_canvas.delete(self.rect)

                self.crop_active = False
                self.side_frame.place(x=1418, y=114)
                # self.save_b.place(x=1418, y=680)
                # self.draw_b.place(x=1465, y=232)
                # self.crop_b.place(x=1390, y=232)
                # self.reset_b.place(x=1418, y=190)
                self.FormatButton()
                self.button_frame.pack()

    def draw_crop(self, event):
        if self.crop_active:
            if not self.rectangles:
                self.rectangles.append(self.rect)

            image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
            x_co_1, x_co_2 = int((self.winfo_screenwidth() / 2) - image_width / 2), int(
                (self.winfo_screenwidth() / 2) + image_width / 2)
            y_co_1, y_co_2 = int(self.max_height / 2 - image_height / 2), int((self.max_height / 2) + image_height / 2)

            if x_co_2 > event.x > x_co_1 and y_co_1 + 2 < event.y < y_co_2:
                self.image_canvas.coords(self.rect, self.point_x, self.point_y, event.x, event.y)
                self.event_x, self.event_y = event.x, event.y

        elif self.draw_active:
            image_width, image_height = self.current_resized_image_size[0], self.current_resized_image_size[1]
            x_co_1, x_co_2 = int((self.winfo_screenwidth() / 2) - image_width / 2), int(
                (self.winfo_screenwidth() / 2) + image_width / 2)
            y_co_1, y_co_2 = int(self.max_height / 2 - image_height / 2), int((self.max_height / 2) + image_height / 2)

            if x_co_2 > self.point_x > x_co_1 and y_co_1 < self.point_y < y_co_2:
                if x_co_2 > event.x > x_co_1 and y_co_1 < event.y < y_co_2:
                    lines = self.image_canvas.create_line(self.point_x, self.point_y, event.x, event.y,
                                                          fill=self.pencil_color, width=self.pencil_size)

                    # create line image and calculating x ,y coordinates as per original image size since
                    # here self.point_x - self.image_x_co and all are with respect to the resized image
                    x_co_1, y_co_1, x_co_2, y_co2 = ((self.point_x - self.image_x_co) * self.current_image_size[0])/self.current_resized_image_size[0], ((self.point_y - self.image_y_co)*self.current_image_size[1])/self.current_resized_image_size[1], ((event.x - self.image_x_co)*self.current_image_size[0])/self.current_resized_image_size[0], ((event.y - self.image_y_co)*self.current_image_size[1])/self.current_resized_image_size[1]

                    img = ImageDraw.Draw(self.image_before_draw)
                    img.line([(x_co_1, y_co_1), (x_co_2, y_co2)], fill=self.pencil_color, width=self.pencil_size + 1)

                    self.lines_drawn.append(lines)
                    self.point_x, self.point_y = event.x, event.y
                    

    def crop_image(self):
        if self.rectangles:
            x_co_1, y_co_1, x_co_2, y_co2 = ((self.point_x - self.image_x_co) * self.current_image_size[0])/self.current_resized_image_size[0], ((self.point_y - self.image_y_co) * self.current_image_size[1]) / self.current_resized_image_size[1], ((self.event_x - self.image_x_co) * self.current_image_size[0]) / self.current_resized_image_size[0], ((self.event_y - self.image_y_co) * self.current_image_size[1]) / self.current_resized_image_size[1]

            self.image_copy = self.image_copy.crop((int(x_co_1), int(y_co_1), int(x_co_2), int(y_co2)))
            x_co_1, y_co_1, x_co_2, y_co2 = self.point_x - self.image_x_co, self.point_y - self.image_y_co, self.event_x - self.image_x_co, self.event_y - self.image_y_co

            self.save()
        else:
            messagebox.showinfo(title="Can't crop !", message="Please select the portion of the image,"
                                                              " you want to crop")

    def image_after_draw(self):
        if self.lines_drawn:
            self.image_copy = self.image_before_draw
            self.save()
        else:
            messagebox.showinfo(title='Cannot save!', message='You have not drawn anything on the image.')

    def save(self):
        image_path_object = filedialog.asksaveasfile(defaultextension='.jpg')

        if image_path_object:
            image_path = image_path_object.name
            if self.draw_active:
                for line in self.lines_drawn:
                    self.image_canvas.delete(line)
                self.lines_drawn = []

                # as crop is still active after cropping the image so on calling activate_crop, it will get deactivated
                self.activate_draw()

            if self.crop_active:
                self.image_canvas.delete(self.rect)

                # as crop is still active after cropping the image so on calling activate_crop, it will get deactivated
                self.activate_crop()

            self.image_copy.save(image_path)
            self.image_paths.insert(self.current_index + 1, image_path)
            self.current_index += 1
            self.show_image(image=image_path)            

        self.delete_b.configure(state="normal")
        self.save_b.configure(state="disable")
        self.FormatButton()
    def edgesFun(self):
        My_image=np.array(self.image_copy.convert('RGB'))            
        image_GaussianBlur= cv2.GaussianBlur(My_image,(13,13),0) 
        dage=cv2.Canny(image_GaussianBlur,30,160)
        contours, _ =cv2.findContours(dage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(My_image,contours,-1,(0,255,0),2)        
        self.modified_img_resized = Image.fromarray(My_image)
        self.modified_img = Image.fromarray(My_image)
        self.image_copy = self.modified_img          
        self.compare_images()
        im = ImageTk.PhotoImage(self.modified_img_resized)
        self.show_image(modified=im)
        Contours_label = tk.Label(self.button_frame2,text="Count Contours:", background=self.button_frame_color,
                                   foreground="white", font="lucida 9 bold")
        Contours_label.place(x=50)
            

    def reset(self):
        if self.original_image and not self.error:
            if self.draw_active:
                for line in self.lines_drawn:
                    self.image_canvas.delete(line)
                    self.lines_drawn = []
                self.image_before_draw = self.image_copy
            else:
                current_original_image = self.image_paths[self.current_index]
                self.show_image(image=current_original_image)

            self.delete_b.configure(state="normal")
            self.save_b.configure(state="disable")

    
    def open_adjustment_window(self):
            My_image=np.array(self.image_copy.convert('RGB'))            
            m=np.ones(My_image.shape,dtype="uint8")*100
            copy2=cv2.add(My_image,m)
            self.modified_img_resized = Image.fromarray(copy2)
            self.modified_img = Image.fromarray(copy2)
            self.image_copy = self.modified_img          
            self.compare_images()
            im = ImageTk.PhotoImage(self.modified_img_resized)
            self.show_image(modified=im)

    def open_filter_window(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            fl.Filters(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)

    def open_Detection_line(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            fl.LineDetection(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)

    def open_SmoothingImages_window(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            fl.SmoothingImages(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)

    def open_s_edges_window(self):
        if self.original_image and not self.error:
            self.delete_b.configure(state="disable")
            fl.ScalesEdges(self, self.image_copy, self.modified_img, self.image_copy_resized, self.modified_img_resized)        

    def delete(self):
        if self.image_paths:
            import winshell
            self.original_image.close()
            winshell.delete_file(self.image_paths[self.current_index])
            print(len(self.image_paths), self.current_index)

            print(len(self.image_paths), self.current_index)
            if len(self.image_paths) - 1 == self.current_index:
                self.image_paths.remove(self.image_paths[self.current_index])
                self.current_index = 0
            else:
                self.image_paths.remove(self.image_paths[self.current_index])

            if self.image_paths:

                self.show_image(image=self.image_paths[self.current_index])
            else:
                self.status_bar.configure(text="")
                self.image_canvas.image = ''

                self.open_image_button.configure(image=self.open_image_icon, command=self.open_image,
                                                 text="Click To Open Image", font="lucida 12 bold")
                self.open_image_button.place(x=685, y=350)

                if self.error:
                    self.error_b.place_forget()
                    self.error = None

    def compare_images(self):
        if self.original_hash == imagehash.average_hash(self.image_copy_resized):
            self.save_b.configure(state="normal")
        else:
            self.save_b.configure(state='disable')

    def exit_window(self):
        self.destroy()


def mouse_not_hover(button, color=None):
    if not color:
        color = 'black'
    button.configure(bg=color)


def mouse_hover(button, color=None):
    if not color:
        color = '#473f3f'
    button.configure(bg=color)


if __name__ == "__main__":
    ImageEditor()