#!/usr/bin/env python3



##  SpiceLogger - A Free, Open-Source Ubuntu Log Analyzer
##  Written in Python 3.x and PyQt5.

##  Copyright (C) 2020  PumpkinSpiceLinux


##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.

##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <https://www.gnu.org/licenses/>.



import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src import LogCategoriesTree
from src import LogEntriesList



class SpiceLogger( QWidget ):

	##  Class Constructor

	def __init__( self ):

		##  Call the parent constructor.

		super( SpiceLogger, self ).__init__()


		##  Set the application window's title.

		self.setWindowTitle( "SpiceLogger - Free Open-Source Ubuntu Log Analyzer" )


		##  Set the initial dimensions and position of the application window.

		screenDimensions = QDesktopWidget().screenGeometry()

		centeredXPosition = screenDimensions.width() / 4
		centeredYPosition = screenDimensions.height() / 4
		centeredWidth = screenDimensions.width() / 2
		centeredHeight = screenDimensions.height() / 2

		self.setGeometry( centeredXPosition, centeredYPosition, centeredWidth, centeredHeight )


		##  Set up the default application window layout.

		self.windowLayout = QHBoxLayout()

		self.setLayout( self.windowLayout )


		##  Create a new QSplitter for the window.

		self.windowSplitter = QSplitter( Qt.Horizontal )


		##  Construct a new LogCategoryTree for the left-side of the window.

		self.logCategoriesTree = LogCategoriesTree.LogCategoriesTree()


		##  Construct a new LogEntriesList for the right-side of the window.

		self.logEntriesList = LogEntriesList.LogEntriesList()


		##  Add all GUI elements to the application window.

		self.windowLayout.addWidget( self.windowSplitter )
		self.windowSplitter.addWidget( self.logCategoriesTree )
		self.windowSplitter.addWidget( self.logEntriesList )


		##  Set the initial sizes of both sides of the windowSplitter (based on a percent 1-100).

		self.windowSplitter.setSizes( [ ( self.size().width() / 100 ) * 35, ( self.size().width() / 100 ) * 65 ] )


		##  Set logEntriesList to call checkbox click processing function whenever logCategoriesTree has a checkbox checked.

		self.logCategoriesTree.treeModel.itemChanged.connect( self.processLogCategoryTreeCheckboxClick )



	##  Class Functions

	def processLogCategoryTreeCheckboxClick( self, checkbox ):

		selectedTreeNodes = self.logCategoriesTree.processLogCategoryTreeCheckboxClick( checkbox )

		self.logEntriesList.processLogCategoryTreeCheckboxClick( selectedTreeNodes )

		return



##  Application Initialization Code

if __name__ == "__main__":

	application = QApplication( sys.argv )
	applicationWindow = SpiceLogger()
	applicationWindow.show()
	sys.exit( application.exec_() )
