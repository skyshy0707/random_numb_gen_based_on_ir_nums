# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 04:16:41 2020

@author: SKY_SHY
"""

#see below a pretty simple example ///How To use///

from PRING_IRRN import irandom
import time

irandom.set_seed(581)

seq = irandom.randint(100100000000000000000000,2**3000, 10)


start = time.time()
for num in seq:
    print("^^^^", num)
end = time.time()

print(end-start)
