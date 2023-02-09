import numpy as np
from numpy.core.function_base import linspace
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.ndim)
print(np.shape(a))
a = a.reshape(6, 1)
print(a)
print(a.size)
print(a.dtype)
print(a.itemsize)
#data = [1, 2, 3, 4, 5, 6]
a = np.array([1, 2, 3])
b = np.copy(a)
a[0] = 6
print(a)
print(b)
print(np.arange(5))
print(np.arange(10, 20, 2))
print(np.linspace(10, 20, 4))
a = [[1, 2, 3], [11, 22, 33]]
b = [[4, 5, 6], [44, 55, 66]]
c = np.concatenate([a, b])
print('Concatention', c)
d = np.vstack((a, b))
print('Vstack\n', d)
e = np.hstack((a, b))
print('Hstack\n', e)