'''
Newton's method to finding the roots of a function
Translated from TVG's matlab code

Inputs:
    f: f(x) [function] defining the values of your function w.r.t. the independent variable x
    fprime: f'(x) [funciton] first derivative of f w.r.t. x
    guess: approximate location of zero of f(x)
    tolerance: desired precision of zero location

Outputs:
    x_zero: location of the zero

History:
    03.02.2021: Translated by TVG and debugged

'''

import numpy

def newton(f, fprime, guess, tolerance):
    
    xx = [0, guess]

    ii = 1
    iter = 1
    iterlim = 1e2

    while (numpy.absolute(tolerance) < numpy.absolute(xx[ii]-xx[ii-1]) or iter == 1) and iter < iterlim:
        ffprime = fprime(xx[ii])
        ff = f(xx[ii])
        
        if ffprime == 0:
            print('Error, slope at point = 0. Choose a different initial condition')
            exit()
        
        xx.append(xx[ii] - ff/ffprime)
        ii += 1 
        iter += 1
    
    x_zero = xx[-1]

    return x_zero


if __name__ == "__main__":

    f = lambda x: 2*x**2 - 4*x + 1
    fprime = lambda x: 4*x + 4

    x_zero = newton(f, fprime, 1, 1e-6)
    print(x_zero)
    print((4+numpy.sqrt(4**2-2*4*1))/(2*2))





