#!/usr/bin/env python

__author__ = "Jeffrey R. Spies"
__copyright__ = "Copyright 2007-2010, Jeffrey R. Spies"
__license__ = "Apache License, Version 2.0"
__version__ = "0.2"
__maintainer__ = "Jeffrey R. Spies"
__email__ = "jspies@virginia.edu"
__status__ = "Beta"
__title__ = "Nullshop"

from PyQt4 import QtCore, QtGui
import Image
import sys, random, os, datetime

class Dispatch(QtGui.QMainWindow):
    # dispatchList = []
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setGeometry(50, 50, 400, 300)
        # self.undoStack = QtGui.QUndoStack()
        self.setWindowTitle(__title__ + " " + __version__)
        self.setAcceptDrops(True)
        
        #################################################################################
        # Menus
        #################################################################################
        
        self.menuFile = self.menuBar().addMenu("&File")
        
        actionConvertFiles = QtGui.QAction("&Convert Files", self,
            statusTip = "Convert Files",
            triggered=self.convertFilesFromDialog)
        
        actionQuit = QtGui.QAction("Q&uit", self, 
            shortcut="Ctrl+Q",
            statusTip="Exit the application",
            triggered=QtGui.qApp.quit)
        
        self.addActions(self.menuFile, [actionConvertFiles, actionQuit])
        
        #################################################################################
        # Widgets
        #################################################################################
        
        drop = QtGui.QLabel('Drop files here or "File/Convert Files..."'
            + '\n'
            + '\n' + 'Scrambled images will have "null" plus the date'
            + '\n' + 'appended to their file names in the same folder as'
            + '\n' + 'the original files. Images are saved in a lossless'
            + '\n' + 'data format (PNG) so as to not introduce noise'
            + '\n' + 'caused by "lossy" compression formats. Files are'
            + '\n' + 'dated for consistency and to ensure nothing is'
            + '\n' + 'overwritten; the exact shuffle is random, so it'
            + '\n' + 'would be impossible to recreate the image once lost.'
            + '\n'
            + '\n' + 'Visit http://people.virginia.edu/~js6ew/ for more info.'
        )
        drop.setAlignment(QtCore.Qt.AlignCenter)
        
        self.setCentralWidget(drop)
    
    #####################################################################################
    # Helper Functions
    #####################################################################################
    def addActions(self, menu, actions):
        for action in actions:
            if action is None:
                menu.addSeparator()
            else:
                menu.addAction(action)
    
    #####################################################################################
    # Menu Actions
    #####################################################################################
    def convertFilesFromDialog(self):
        for filename in QtGui.QFileDialog.getOpenFileNames(self):
            self.convert(str(filename))
    
    #####################################################################################
    # General Functions
    #####################################################################################    
    def convert(self, filename):
        base,ext = os.path.splitext(filename)
        im = Image.open(filename)
        pix = im.load()
        
        pixels = []
        for h in range(0, im.size[1]):
            for w in range(0, im.size[0]):
                pixels.append(pix[w,h])
        
        random.shuffle(pixels)
        im.putdata(pixels)
        new = base + '.null.' + datetime.datetime.now().strftime('%Y%M%d%H%M%S')
        im.save(new + '.png')
    
    #####################################################################################
    # Drop Handlers
    #####################################################################################
    
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        for i in event.mimeData().urls():
            filename = str(i.toString())
            filename = filename.replace('file://','')
            self.convert(filename)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(__title__ + " " + __version__)
    dispatch = Dispatch()
    dispatch.show()
    sys.exit(app.exec_())