import numpy as np


a = np.arange(12).reshape(3, 4)
print(a)
print(a[:, 0][np.array([True, False, True])])
print([a[:, 0]>2])