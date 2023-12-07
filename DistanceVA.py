import numpy as np
import camel_tools
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.cli.utils import open_files

from camel_tools.cli.utils import open_files

#أولا نعرف كلا من المتجهة والمصفوفة
vector=[1,5,3]
array=[[3,5,9],[9,3,2],[3,5,2]]

# Ecnlidean نقوم بحساب المسافة بين متجهة ومصفوفة  
distances=[]
for arr in array:
    sum_Of_Squer=0
    for v in range(len(vector)):
        point=vector[v]-arr[v]
        Squer=point**2 
        sum_Of_Squer+=Squer
    distance=np.sqrt(sum_Of_Squer)
    distances.append(distance)

# طباعة النقطة الأقرب بالنسبة للمتجهة
Closest_Point= distances.index(min(distances))
print("The Closest Point Is: ",array[Closest_Point])