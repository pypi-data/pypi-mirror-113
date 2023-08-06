# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:15:31 2021

@author: ppina
"""

#### Numeros primos de una lista

#### Para comprobar que funciona:
    
# mm = int(input("introduzca el numero minimo de las lista: "))
# MM = int(input("introduzca el numero maximo de las lista: "))


# print("los numero primos entre", mm, "y", MM, "son:")

# for num in range(mm, MM + 1):
#     # primos son mayores de 1
#     if num > 1:
#         for i in range(2, num):
#             if (num % i) == 0:
#                 break
#         else:
#             print(num)
           
           
#### Definitivo

def primoslista(mm, MM):
    
    print("los numero primos entre", mm, "y", MM, "son:")

    for num in range(mm, MM + 1):
        # primos son mayores de 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
                else:
                    return (num)
                print(num)
          