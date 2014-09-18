#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, June 2014.

import numpy as np
import matplotlib.pyplot as plt


class HistoryDependentRW():

    def __init__(self, alpha=0.75, l=(1, 1), nwalkers=1000, x0=0):
        """ Initialize the values.

        alpha    : probability that a particle moves the same direction of the before one
        l        : step length
        nwalkers : number of trials
        x0       : initial position
        """
        self.alpha = alpha
        self.l = l
        self.nwalkers = nwalkers
        self.x0 = x0

    def random_walk_d1(self, N):
        """ Caluculate the displacements of each walkers.

        N : A list of walk steps
        """
        x = np.zeros([self.nwalkers, max(N)], 'i')
        x_direction = np.zeros([self.nwalkers, max(N)], 'i')
        p = np.random.random([self.nwalkers, max(N) - 1])
                             # generate random number in [0,1)
        alpha = self.alpha
        l = self.l
        x0 = self.x0

        for n in xrange(self.nwalkers):
            x[n][0] = x0
            x_direction[n][0] = +1 if n < int(self.nwalkers / 2) else -1
            for i in xrange(1, max(N)):
                if p[n][i - 1] < alpha:
                    x_direction[n][i] = x_direction[n][i - 1]
                else:
                    x_direction[n][i] = -x_direction[n][i - 1]

                if x_direction[n][i] > 0:
                    x[n][i] = x[n][i - 1] + x_direction[n][i] * l[0]
                else:
                    x[n][i] = x[n][i - 1] + x_direction[n][i] * l[1]

        self.x = x
        self.N = N

    def calc_ave(self):
        """ Caluculate the average of displacements after max(N) steps.

        You can call the results by "self.N", "self.x_ave", and "self.x_2_ave"
        """
        self.x_ave = np.sum(
            self.x, axis=0, dtype=np.float32) / self.nwalkers * 1.
        self.x_2_ave = np.sum(
            self.x ** 2, axis=0, dtype=np.float32) / self.nwalkers * 1.
        self.variance_x = self.x_2_ave - self.x_ave ** 2

    def show(self):
        """ Show the graph.
        """
        fig = plt.figure('random walk', figsize=(8, 8))

        x_ave = [self.x_ave[nvalue - 1] for nvalue in self.N]
        x_2_ave = [self.x_2_ave[nvalue - 1] for nvalue in self.N]
        variance_x = [self.variance_x[nvalue - 1] for nvalue in self.N]

        ax1 = fig.add_subplot(311)
        ax1.plot(self.N, x_ave)
        ax1.set_ylabel(r'$<x(N)>$', fontsize=16)

        ax2 = fig.add_subplot(312)
        ax2.plot(self.N, x_2_ave)
        ax2.set_ylabel(r'$<x^{2}(N)>$', fontsize=16)

        ax3 = fig.add_subplot(313)
        ax3.set_ylabel(r'$<\Delta x^{2}(N)>$', fontsize=16)
        ax3.plot(self.N, variance_x)
        ax3.set_xlabel(r'$N$')

        plt.show()

    def caluculate_prob(self, _n):
        N = max(self.N)
        x = self.x
        count_box = np.zeros([N, 2 * N + 1], 'f')
        for n in xrange(N):
            for walker in xrange(self.nwalkers):
                count_box[n][N + x[walker][n]] += 1
        prob = count_box / self.nwalkers

        def show_for_n(_n):

            xmin = -N
            xmax = N
            for _x in xrange(2 * N + 1):
                if prob[_n][_x] != 0:
                    xmin, xmax = _x - N, N - _x
                    break

            xmargin = xmax * 0.1
            ymax = np.amax(prob[_n])
            ymargin = ymax * 0.1

            fig = plt.figure('probability')
            ax = fig.add_subplot(111)
            ax.grid()
            ax.set_xlim(xmin - xmargin, xmax + xmargin)
            ax.set_ylim(0, ymax + ymargin)
            ax.plot(xrange(-N, N + 1), prob[_n])
            ax.set_xlabel(r'$x$', fontsize=16)
            ax.set_ylabel(r'$P(x,N)$', fontsize=16)
            plt.show()

        show_for_n(_n)

if __name__ == '__main__':
    rw = HistoryDependentRW()
    N = xrange(1, 512)
    rw.random_walk_d1(N)
    rw.caluculate_prob(_n=400)
    rw.calc_ave()
    rw.show()
