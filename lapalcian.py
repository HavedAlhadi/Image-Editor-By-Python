import cv2
import numpy as np

def lapalcian(f):        
    # تحويل مصفوفة الصورة من ملونة إلى رمادية, f --> F    
    f=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)    
    # تحويل مصفوفة الصورة من مجال الخاص إلى  مجال التردد, f --> F    
    F = np.fft.fft2(f)
    #إزاحة التردد المنخفض إلى المركز 
    Fshift = np.fft.fftshift(F)
    # تطبيق فلتر جاوسن لتنعيم الصورة  Low Pass Filter
    M,N = F.shape
    H = np.zeros((M,N), dtype=np.float32)
    D0 = 10
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            H[u,v] = np.exp(-D**2/(2*D0*D0))
    # تطبيق فلتر جاوسن لتنعيم الصورة: High pass filter
    HPF = 1 - H
    # Image Filters
    lap = Fshift * HPF
    G = np.fft.ifftshift(lap)
    g = np.abs(np.fft.ifft2(G))        
    return g