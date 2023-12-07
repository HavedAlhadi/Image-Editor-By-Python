from PIL import Image
import operator
import cv2
import numpy 
import matplotlib.pyplot as plt

gamma = 1.8  # a parameter
n=7
img = cv2.imread("Photos\image44.jpg")
def Convertgrey(input_image):
    [nx, ny, nz] = numpy.shape(input_image)  # nx: height, ny: width, nz: colors (RGB)
    # إستخراج كل لون في مصفوفة منفردة
    r_img, g_img, b_img = input_image[:, :, 0], input_image[:, :, 1], input_image[:, :, 2]

    # عملية تحويل صورة الألون إلى صورة رمادية
    #gamma = 1.9  # a parameter
    r_const, g_const, b_const = 0.2126, 0.7152, 0.0722  # على التوالي RGB أوزان مكونات التحويل للصورة   
    grayscale_image = r_const * r_img ** gamma + g_const * g_img ** gamma + b_const * b_img ** gamma
    return grayscale_image

def square_matrix(square):
    tot_sum = 0      
    # Calculate sum of all the pixels in n * n matrix
    for i in range(n):
        for j in range(n):
            tot_sum += square[i][j]
              
    return tot_sum // (n*n)     # return the average of the sum of pixels
  
def MeanBlur(image):
    square = []     
    square_row = []   
    blur_row = []   
    blur_img = [] 
    n_rows = len(image) 
      
    # number of columns in the given image
    n_col = len(image[0]) 
      
    # rp is row pointer and cp is column pointer
    rp, cp = 0, 0 
    while rp <= n_rows - n: 
        while cp <= n_col-n:              
            for i in range(rp, rp + n):                  
                for j in range(cp, cp + n):                      
                    # append all the pixels in a row of n * n matrix
                    square_row.append(image[i][j])                      
                # append the row in the square i.e. n * n matrix 
                square.append(square_row)
                square_row = []
              
            # calculate the blurred pixel for given n * n matrix 
            blur_row.append(square_matrix(square))
            square = []              
            # increase the column pointer
            cp = cp + 1          
        # append the blur_row in blur_image
        blur_img.append(blur_row)
        blur_row = []
        rp = rp + 1 # increase row pointer
        cp = 0 # start column pointer from 0 again
      
    return blur_img



def median_filter(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = numpy.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final



img=Convertgrey(img)
img=median_filter(img,3)
# img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
plt.figure(figsize=(n,n))
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()
cv2.waitKey(0)
