# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 20:57:05 2015

@author: doanphongtung
"""

import time
import numpy as np

a = np.random.rand(1000000)
b = np.random.rand(1000000)

start = time.time()
df = a * b
end = time.time()
print sum(df)
print end - start

start = time.time()
df = 0
for i in xrange(1000000):
    df += a[i] * b[i]
end = time.time()
print df
print end - start