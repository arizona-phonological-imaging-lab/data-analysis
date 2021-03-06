#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import string
from math import ceil
import sys
import json
from PyQt4 import QtGui

class Converter():

    def main(self, folder, format):
        self.tracer_id = 'etc'                                              # etc == EdgeTrak Converter
        conFilePath, jpgPaths = self.read_folder_contents(folder)
        numFiles = self.read_con_file(conFilePath)
        if format == 'AT':                                                  # AutoTrace Manual Tracer format
            # Currently some issues rendering - suspect it has to do with
            # EdgeTrak needing a cropped version of our Ultrasound Image,
            # and therefore, the coordinates for ET won't be the same as
            # the uncropped image that the Manual Tracer requires
            self.resample_data(numFiles)#, splitCoords)
            self.print_AT_files(numFiles, folder, jpgPaths)#, splitCoords)
        if format == 'ET':                                                  # EdgeTrak format
            # TODO: Do we want to convert \italics{to} EdgeTrak?
            pass
        if format == 'AW':                                                  # APIL Web json format
            self.print_AW_files(numFiles,folder,jpgPaths)

    def read_folder_contents(self, folder):
        """ Reads in the contents of a folder and groups 
        the sorted .jpg paths together in a list, and creates an
        object for the  .con file. The folder should contain *only* the 
        relevant jpgs (tongue frames) and the single corresponding con file
        generated by EdgeTrak. """
        folder
        folderContents = os.listdir(folder)
        jpgPaths=[]
        for fileName in folderContents:                                         # this loop does the sorting of .con and .jpg files
            if '.con' in fileName:
                conFilePath = os.path.normpath(os.path.join(folder, fileName))
            if ".jpg" in fileName:
                self.img_type = '.jpg'
                jpgPaths.append(os.path.splitext(fileName)[0])
            elif fileName.endswith(".png"):                                     #Allow for finding .png files too
                self.img_type = '.png'
                jpgPaths.append(os.path.splitext(fileName)[0])
            else:
                pass
        jpgPaths = sorted(jpgPaths)                                             # sort the .jpg paths because the .con file columns 
                                                                                # are ordered according to the jpg filenames
        return conFilePath, jpgPaths
		
    def read_con_file(self, conFilePath):
        """Reads in a .con file, returns the list self.splitCoords,
        which is a list of the coordinates generated by EdgeTrak and then
        split according to the corresponding .jpg image"""
        conFile = open(conFilePath, 'r')                                        # read in the file
        conLines = conFile.readlines()                                          # create list with lines as elements
        conFile.close()
        numFiles = ((len(conLines[0].strip().split())) / 2)                     # count number of columns in file and divide by 2 
                                                                                # (since 2 columns to each image file)
        self.splitCoords = [[] for i in range(numFiles)]                        # create list to append paired coordinates for 
                                                                                # each image file
        for line in conLines:
            i=0
            coords = line.strip().split()                   
            for sublist in self.splitCoords:                                    # each sublist corresponds to an image file 
                                                                                # (tongue frame)
                sublist.append((coords[(2*i)], coords[(2*i)+1]))                # the input .con file has paired columns from left 
                i+=1                                                            # to right (1,2), (3,4), (5,6)..., and this assigns
                                                                                # each pair to a tuple
                                                                                # and the tuple to its own sublist on splitCoord
        return numFiles

    def resample_data(self, numFiles, resampleTo = 32):
    # def resample_data(self, numFiles, splitCoords, resampleTo = 32):
        """ Used to get the EdgeTrak data compatable with 
        AutoTrace, which handles 32 points per traced image. """
        for i in range(numFiles):
            origLength = len(self.splitCoords[i])                               # original length of the .con file columns 
            resampled = []                                                      # (ie the number of traced points)
            if  origLength > resampleTo:       
                        for j in range(resampleTo):
                            resampled.append(self.splitCoords[i][int(ceil(j * 
                                                    origLength / resampleTo))])         # walk down the array of tuples (coordinates) 
                                                                                        # in an evenly-spaced manner
                        self.splitCoords[i]=resampled
            else:
                pass
        # return splitCoords

    def print_AT_files(self, numFiles, folder, jpgPaths):#, splitCoords):
        """ Print out a new file for each .jpg tongue image, 
        using the filename of each .jpg to create the filename for the
        corresponding .txt file. """
        for fileNum in range(numFiles):
            print numFiles, jpgPaths
            outFile = open(os.path.join(folder,(str(                    # Manual tracer requires output to be in specific named format.
                jpgPaths[fileNum])+'{0}.{1}.traced.txt'.format(         # Must use 'etc' as initials when loading data in Manual tracer to view
                self.img_type,self.tracer_id))),'w')                                
                                                                        
            # outFile= open(folder + '/output_' +
            #               str(jpgPaths[fileNum]) + '.txt' , 'w')
            i=0

            for item in self.splitCoords[fileNum]:
                i+=1
                outFile.write(str(i) + '\t'  + str(item[0]) + 
                                  '\t' + str(item[1]) + '\n')                   # write line in the new file with tab delimiting
    

    def print_AW_files(self,numFiles,folder,jpgPaths):
        """Create a .json file for the APIL web tracer"""
        jsondata = {}
        jsondata['roi'] = "{\"srcX\":0,\"srcY\":0,\"destX\":720,\"destY\":480}"
        jsondata['tracer-id'] = self.tracer_id
        jsondata['subject-id'] = 'unknown'
        jsondata['project-id'] = 'unknown'
        jsondata['trace-data'] = {}

        for f in range(numFiles):#jpgPaths:
            img = jpgPaths[f]+self.img_type
            jsondata['trace-data'][img] = []
            for coord in self.splitCoords[f]:
                coord_unit = {'x':int(float(coord[0])),'y':int(float(coord[1]))}
                jsondata['trace-data'][img].append(coord_unit)


        writeFile = open(os.path.join(folder,"{0}_traces.json".format(self.tracer_id)),'w')
        tojson = json.JSONEncoder().encode(jsondata)
        writeFile.write(tojson)
        writeFile.close()






