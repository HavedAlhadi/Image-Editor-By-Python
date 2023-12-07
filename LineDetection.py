from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np

gamma = 1.8  # a parameter

def Convertgrey(input_image):
    [nx, ny, nz] = np.shape(input_image)  # nx: height, ny: width, nz: colors (RGB)
    # إستخراج كل لون في مصفوفة منفردة
    r_img, g_img, b_img = input_image[:, :, 0], input_image[:, :, 1], input_image[:, :, 2]

    # عملية تحويل صورة الألون إلى صورة رمادية
    #gamma = 1.9  # a parameter
    r_const, g_const, b_const = 0.2126, 0.7152, 0.0722  # على التوالي RGB أوزان مكونات التحويل للصورة   
    grayscale_image = r_const * r_img ** gamma + g_const * g_img ** gamma + b_const * b_img ** gamma
    return grayscale_image


"""
المرشح العمود والمرشح الأفقي الخاص بـ
             _               _                     _                _
            |                 |                   |                  |
            |-1.0  -1.0  -1.0 |                   | -1.0   2.0  -1.0 |
Horizontal =| 2.0   2.0   2.0 |    and Vertical = | -1.0   2.0  -1.0 |
            |-1.0  -1.0  -1.0 |                   | -1.0   2.0  -1.0 |
            |_               _|                   |_                _|
"""

def Vertical_D(input_image):
    grayscale_image=Convertgrey(input_image)
   # هنا قمنا بتعريف مصفوفات القناع الأفقي والعمودي التابعة لفلتر
    Gy = np.array([[-1.0, 2.0, -1.0], [-1.0, 2.0, -1.0], [-1.0, 2.0, -1.0]])
    [rows, columns] = np.shape(grayscale_image)  # we need to know the shape of the input grayscale image
    filtered_image = np.zeros(shape=(rows, columns))  # مسك الفلتر 
    # Gy & Gx ونقوم بضرب الصورة بالقناع الأفقي والعمودي ونخزن الناتج في   y وأيضا في أتجاه xسنمر على الصورة في إتجاه 
    for i in range(rows - 2):
        for j in range(columns - 2):
            gy = np.sum(np.multiply(Gy, grayscale_image[i:i + 3, j:j + 3]))  # x direction
            filtered_image[i + 1, j + 1] = np.sqrt(gy)  # حساب معادلة  sqrt(GY^2)
    return filtered_image

def Horizontal_D(input_image):
    grayscale_image=Convertgrey(input_image)

   # هنا قمنا بتعريف مصفوفات القناع الأفقي والعمودي التابعة لفلتر
    Gx = np.array([[-1.0, -1.0, -1.0], [2.0, 2.0, 2.0], [-1.0, -1.0, -1.0]])
    [rows, columns] = np.shape(grayscale_image)  # we need to know the shape of the input grayscale image
    filtered_image = np.zeros(shape=(rows, columns))  # مسك الفلتر 
    # Gy & Gx ونقوم بضرب الصورة بالقناع الأفقي والعمودي ونخزن الناتج في   y وأيضا في أتجاه xسنمر على الصورة في إتجاه 
    for i in range(rows - 2):
        for j in range(columns - 2):
            gx = np.sum(np.multiply(Gx, grayscale_image[i:i + 3, j:j + 3]))  # x direction
            filtered_image[i + 1, j + 1] = np.sqrt(gx)  # حساب معادلة sqrt(Gx^2)
    return filtered_image


"""
المرشح العمود والمرشح الأفقي الخاص بـ
             _               _                      _                _
            |                 |                    |                  |
            |-1.0  -1.0   2.0 |                    |  2.0  -1.0  -1.0 |
45 Degree = |-1.0   2.0  -1.0 |    and -45 Degree =| -1.0   2.0  -1.0 |
            | 2.0  -1.0  -1.0 |                    | -1.0  -1.0   2.0 |
            |_               _|                    |_                _|
"""


def D45Degree(input_image):
    grayscale_image=Convertgrey(input_image)

   # هنا قمنا بتعريف مصفوفات القناع التابعة لفلتر
    G = np.array([[-1.0, -1.0, 2.0], [-1.0, 2.0, -1.0], [2, -1.0, -1.0]])
    [rows, columns] = np.shape(grayscale_image)  # we need to know the shape of the input grayscale image
    filtered_image = np.zeros(shape=(rows, columns))  # مسك الفلتر 
    # نمر على الصورة في زاوية (45) 
    for i in range(rows - 2):
        for j in range(columns - 2):
            g = np.sum(np.multiply(G, grayscale_image[i:i + 3, j:j + 3]))  # x direction
            filtered_image[i + 1, j + 1] = np.sqrt(g)  # حساب معادلة sqrt(Gx^2)
    return filtered_image


def _45Degree(input_image):
    grayscale_image=Convertgrey(input_image)

   # هنا قمنا بتعريف مصفوفات القناع التابعة لفلتر
    G = np.array([[2, -1.0, -1.0], [-1.0, 2.0, -1.0],[-1.0, -1.0, 2.0]])
    [rows, columns] = np.shape(grayscale_image)  # we need to know the shape of the input grayscale image
    filtered_image = np.zeros(shape=(rows, columns))  # مسك الفلتر 
    #نمر على الصورة في زاوية (45-) 
    for i in range(rows - 2):
        for j in range(columns - 2):
            g = np.sum(np.multiply(G, grayscale_image[i:i + 3, j:j + 3]))  # x direction
            filtered_image[i + 1, j + 1] = np.sqrt(g)  # حساب معادلة sqrt(Gx^2)
    return filtered_image
