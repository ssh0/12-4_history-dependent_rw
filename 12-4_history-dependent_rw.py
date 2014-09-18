#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, June 2014.

from HistoryDependentRW import HistoryDependentRW


def ex_a(alpha=0.75, caluculate_prob=False, n=400):
    rw = HistoryDependentRW(alpha=alpha)
    N = xrange(1, 512)
    rw.random_walk_d1(N)
    if caluculate_prob:
        rw.caluculate_prob(_n=n)
    else:
        rw.calc_ave()
        rw.show()


def ex_b(alpha=0.25, target='nu', N=xrange(1, 1001)):

    if not (target == 'nu' or 'D'):
        print "ArgumentError: target must be 'nu' or 'D'. "
        return 0

    else:

        if target == 'delta_x2':
            N = [8, 64, 256, 512]

        rw = HistoryDependentRW(alpha=alpha)
        rw.random_walk_d1(N)
        rw.calc_ave()

        if target == 'delta_x2':
            for n in N:
                print '<\Delta x^{2}(%d)> = ' % n, str(rw.variance_x[n - 1])
            return 0

        parameter0 = [1.0, 1.0]  # initial values for optimize

        def fit_func(parameter0, x, y):
            a = parameter0[0]
            b = parameter0[1]
            residual = y - (a * x + b)
            return residual

        import scipy.optimize as optimize
        import numpy as np

        if target == 'nu':
            import matplotlib.pyplot as plt
            variance_x = [rw.variance_x[nvalue - 1] for nvalue in N]
            ln_N = np.log(N)
            ln_variance_x = np.log(variance_x)

            result = optimize.leastsq(
                fit_func, parameter0, args=(ln_N, ln_variance_x))

            print 'nu =', result[0][0] / 2.

            plt.xlabel(r'$N$', fontsize=16)
            plt.ylabel(r'$<\Delta x^{2}(N)>$', fontsize=16)
            plt.xscale('log')
            plt.yscale('log')
            plt.axis('equal')
            plt.plot(N, variance_x)
            plt.show()

        elif target == 'D':

            result = optimize.leastsq(fit_func, parameter0,
                                      args=(
                                          np.arange(1, max(N) + 1), rw.x_2_ave)
                                      )
            print 'D =', result[0][0] / 4.


def ex_c():

    rw = HistoryDependentRW(alpha=0.75, l=(1, 0), nwalkers=1000)
    N = xrange(1, 512)
    rw.random_walk_d1(N)
    rw.caluculate_prob(_n=300)

if __name__ == '__main__':

#    ex_a(alpha=0.75, caluculate_prob=False, n=400)

    ex_b(alpha=0.75, target='delta_x2', N=xrange(1, 1001))
    # taget must be 'delta_x2' or 'nu' or 'D'

#    ex_c()
