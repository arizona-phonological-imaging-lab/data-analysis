import csv
import sys, math
import pylab as p
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class NeutralSubtraction():
	
    def __init__(self, contours, neutral):
        '''center points determined by transforming the point (426, 393)
           several times with peterotron, and taking the average.
        '''
        self.centerX = 665	                                        	# these come from hand tuning to find the smallest
        self.centerY = 525                                                      # range of y values of polar mags
        self.main(contours,neutral)

    def getNeutral(self, neutralList):
        '''Finds the neutral tongue by averaging the values of the 
        neutral tongue traces.
        '''
        xaves = []
        yaves = []
        for i in range(1,33):
            for j in range(i,len(neutralList),32):
                xs = []
                ys = []
                xs.append(eval(neutralList[j][2]))
                ys.append(eval(neutralList[j][3]))
            xaves.append(sum(xs)/len(xs))
            yaves.append(sum(ys)/len(ys))

        return xaves, yaves


    def makePolar(self, ContourX, ContourY):
        mags = []
        for i in range(len(ContourX)):
            dist = math.sqrt((ContourX[i]-self.centerX)**2 + 
                             (ContourY[i]-self.centerY)**2)
            mags.append(dist)
        return mags

    def loadContours(self, wordList):
        '''takes a list of coords and returns contents as matrices of x and y
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

    def batchConvert2Polar(self, X, Y):
        M = []
        for i in range(len(X)):
            M.append(self.makePolar(X[i],Y[i]))
        return M

    def NeutralLinguagram(self, M, start=1):
        fakeX = []
        for i in range(len(M)):
            xs = []
            for j in range(1,33):
                xs.append(j)
            fakeX.append(xs)

        x1 = array(fakeX)
        y1 = array(M)
        Z = []
        for i in range(start, (len(M)+start)):
            zs = []
            for j in range(32):
                zs.append(i)
            Z.append(zs)
        z1 = array(Z)

        fig = p.figure()
        ax = Axes3D(fig)
        ax.plot_surface(z1, -x1, y1, rstride=1, cstride=1, cmap=cm.jet)
        ax.view_init(elev=25., azim=45.)
        p.show()

    def batchGetMinD(self, M, center):
        D = []
        for i in range(len(M)):
            D.append(self.subtractMinD(self.vertDist(M[i], center)))
        return D

    def subtractMinD(self, Contour):
        ds = []
        minD = 1000
        for i in range(len(Contour)):
            if abs(Contour[i]) < minD:
                minD = abs(Contour[i])
        for j in range(len(Contour)):
            if Contour[j] < 0:
                ds.append(Contour[j]+minD)
            else:
                ds.append(Contour[j]-minD)
        return ds

    def vertDist(self, Y1, Y2):
        ds = []
        for i in range(len(Y1)):
            ds.append(Y1[i]-Y2[i])
        return ds


    def main(self, contours, neutral):
        cx, cy = self.getNeutral(neutral)                                       # neutral needs to be a list here
        X, Y = self.loadContours(contours)

        cmags = self.makePolar(cx, cy)
        M = self.batchConvert2Polar(X, Y)

        D = self.batchGetMinD(M, cmags)
        self.NeutralLinguagram(D)





