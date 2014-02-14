import random
import math

# Declare the inverse cdf functions here
def inverse_expo(t, lamb):
    try:
        return math.log(1/(1-t))*(1.0/lamb)
    except ZeroDivisionError:
        if lamb == 0: return float('Nan')
        return float('Inf')

# Declare the pdf functions here
def expo(x, lamb):
    try:
        return math.exp(-1*lamb*x)*lamb
    except ValueError:
        return float('nan')

# Don't alter the below two functions
def sample_inverse(func, *args):
    t = random.uniform(0, 1)
    return func(t, *args)

def sample_reject(func, a, b, M, *args):
    while True:
        t = random.uniform(0, 1)
        x = a + t*(b-a)
        ret = func(x, *args)
        if ret < 0: return float('-Inf')
        u = random.uniform(0, M)
        if u <= ret: return u

def inverse_method():
    # Put the inverse cdf params here
    param1 = 1
    func = inverse_expo
    return sample_inverse(func, param1)

def rejective_method():
    # Put the cdf params here
    param1 = 1
    func = expo
    # Put the rejective sampling function params here
    a, b, M = 1, 10, 1
    return sample_reject(func, a, b, M, param1)
