#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""
import csv
import os
import sys
from PyQt4 import QtGui, QtCore
import linguaGram as LG
import neutralSubtraction as NS
import edgetrak_converter as conv

class MainWindow(QtGui.QMainWindow):
    '''
    this is the main window which houses all others
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        center = MainWidget()
        self.setCentralWidget(center)

        # this is the dir where the icons for all the buttons are
        imgDir = 'imgDir/'

        # set up all the basic functions and 
        openAction = QtGui.QAction(QtGui.QIcon(imgDir + 'open_file.svg'), 
                                   'APIL Traces', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File(s)')
        openAction.triggered.connect(center.select_files)

        convertEdgeTrakAction = QtGui.QAction('EdgeTrak --> APIL', self)
        convertEdgeTrakAction.triggered.connect(center.convertEdgeTrak)

        exitAction = QtGui.QAction(QtGui.QIcon(imgDir + 'exit.svg'), 
                                   'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)

        self.statusBar()

        menubar = self.menuBar()
        importMenu = menubar.addMenu('&Open')
        importMenu.addAction(openAction)

        convertMenu = menubar.addMenu('&Convert')
        convertMenu.addAction(convertEdgeTrakAction)

        exitMenu = menubar.addMenu('&Exit')
        exitMenu.addAction(exitAction)


        self.setWindowTitle('Main window')
        self.setGeometry(0, 0, 400, 400)

        self.show()
        
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                               

class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        labelSelectFiles = QtGui.QLabel('Data Files:')
        self.editSelectFiles = QtGui.QTextEdit()
        btnGroup = self.createExclusiveGroup()
        btnViz = QtGui.QPushButton('Visualize')

        QtCore.QObject.connect(btnViz, QtCore.SIGNAL("clicked()"), 
                               self.checkOutBoxes)
        grid = QtGui.QGridLayout()

        grid.addWidget(labelSelectFiles, 1, 0)
        grid.addWidget(self.editSelectFiles, 2, 0, 1, -1)
        grid.addWidget(btnGroup, 9,0)
        grid.addWidget(btnViz, 10, 0, 1, -1)

        self.setLayout(grid) 
        self.show()
   

    def select_files(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, "Choose File(s)")
        for fileName in fileNames:
            self.editSelectFiles.append(str(fileName))

    def convertEdgeTrak(self):
        folder = str(QtGui.QFileDialog.getExistingDirectory(self, 
                               "Select folder containing *.con file + images")) # make dialog and select dir
        converter = conv.Converter()
        converter.main(folder)

    def createExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("Visualization Options")
        groupBox.setFlat(True)

        self.checkBox1 = QtGui.QRadioButton("Linguagram")
        self.checkBox2 = QtGui.QRadioButton("Neutral Subtraction")
        self.checkBox3 = QtGui.QRadioButton("Waveform")
        self.checkBox4 = QtGui.QRadioButton("Spectragram")
        
        box = QtGui.QGridLayout()
        box.addWidget(self.checkBox1, 1,0)
        box.addWidget(self.checkBox2, 1,1)
        box.addWidget(self.checkBox3, 2,0)
        box.addWidget(self.checkBox4, 2,1)

        # addStrech is nice for when window size changes
        box.setColumnStretch(0, 1)
        box.setColumnStretch(1, 1)

        groupBox.setLayout(box)

        return groupBox
    


    def traces_to_list(self,paths):
        ''' 
        INPUT: 
        a dir of unmerged trace files -or- a single merged trace file
        ''' 
        wordList = []
        # if the user has only loaded one file to vizualize,
        if len(paths)==1:
            # assume that file is a files of merged trace files
            with open(paths[0]) as f:
                dialect = csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
                r = csv.reader(f, dialect)
                for row in r:
                    wordList.append(row)
                    
        # if the user has loaded more than one file to vizualize,
        # then assume that the files are each a trace of a single frame
        elif len(paths)>1:
            for path in paths:
                with open(path) as f:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)
                    r = csv.reader(f, dialect)
                    for row in r:
                        wordList.append([path]+row)
                    
        return wordList

    def checkOutBoxes(self):
        if self.checkBox1.isChecked():
            try:
                paths = self.editSelectFiles.toPlainText().split('\n')
                wordList = self.traces_to_list(paths)
                LG.LinguaGram().main(wordList)
            except:
                QtGui.QMessageBox.warning(self, 'ERROR', 
                                "Make sure you have either:\n" +
                                "(a) multiple individual trace files\n" +
                                "or (b) a single file of many traces\n"+
                                "in APIL format (not EdgeTrak)")

        # this assumes the user loads 2 files, each file a merged set of traces,
        # one path should contain the string 'neutral'
        if self.checkBox2.isChecked():
            try:
                for path in self.editSelectFiles.toPlainText().split('\n'):
                    if 'neutral' in path:
                        neutral = self.traces_to_list([path])
                    else:
                        contours= self.traces_to_list([path])
                NS.NeutralSubtraction(contours, neutral)
            except:
                QtGui.QMessageBox.warning(self, 'ERROR', 
                                "Make sure you have exactly 2 files loaded:\n" +
                            "(1) neutral file and (1) contours file")
        if self.checkBox3.isChecked():
            pass
        if self.checkBox4.isChecked():
            pass

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
