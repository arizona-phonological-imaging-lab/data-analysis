'''
 neutralContour.py
 Copyright (C) 2010 Jeff Berry
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''

import sys, math
import pylab as p
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class LinguaGram():
    def __init__(self):
        '''center points determined by transforming the point (426, 393)
           several times with peterotron, and taking the average.
        '''
        self.centerX = 665	                                 	        # these come from hand tuning to find the smallest
        self.centerY = 525                                                      # range of y values of polar mags

    def loadContours(self, wordList):
        '''Opens a .csv file and returns contents as matrices of x and y
        vectors -- 1 column of the x matrix corresponds to 1 column of y
        matrix, to make a single frame.
        '''
        X = []
        Y = []
        for i in range(0,len(wordList),32):
            xs = []
            ys = []
            for j in range(32):
                xs.append(eval(wordList[i+j][2]))
                ys.append(eval(wordList[i+j][3]))
            X.append(xs)
            Y.append(ys)
        return X, Y

    def linguaGram(self,X,Y):
        x1 = array(X)
        y1 = array(Y)
        Z = []
        for i in range(len(X)):
            zs = []
            for j in range(32):
                zs.append(i+1)
            Z.append(zs)
        z1 = array(Z)

        fig = p.figure()
        ax = Axes3D(fig)
        ax.plot_surface(z1, -x1, -y1, rstride=1, cstride=1, cmap=cm.jet)
        ax.view_init(elev=25., azim=45.)
        p.show()

    def main(self,wordList):
        X, Y = self.loadContours(wordList)
        self.linguaGram(X, Y)
