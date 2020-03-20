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



class LogCategoriesTree( QTreeView ):

	##  Class Constructor

	def __init__( self ):

		##  Call the parent constructor.

		super( LogCategoriesTree, self ).__init__()


		##  Set the model for this QTreeView.

		self.treeModel = QStandardItemModel()

		self.setModel( self.treeModel )


		##  Set up the headers for this QTreeView.

		self.treeModel.setHorizontalHeaderLabels( [ "Log Category", "Show?" ] )

		self.header().setSectionResizeMode( QtWidgets.QHeaderView.ResizeToContents )
		self.header().setStretchLastSection( False )
		self.header().setSectionResizeMode( 0, QtWidgets.QHeaderView.Stretch )


		##  Create list of all log categories.

		self.treeCategoriesList = [ [ "Local Authentication Logs", 
											"New Session User Logins", 
											"Existing Session User Logins", 
											"System Power-Ons", 
											"System Power-Offs", 
											"Successful Sudo Commands", 
											"Failed Sudo Commands" ] ]


		##  Create list to keep track of all active tree nodes (nodes added to the GUI).

		self.activeTreeNodes = []


		##  Create list to keep track of currently user-selected nodes.

		self.selectedTreeNodes = [ [ 0, 0, 0, 0, 0, 0, 0 ] ]


		##  Grab each root node (list of subnodes).

		for rootNode in self.treeCategoriesList:

			##  Helper list for the easy organization of a sublist to be appended to activeTreeNodes each iteration.

			tempListUnderConstruction = []


			##  Used to detect if the root node is currently being worked with.

			onFirstIndex = True


			##  Grab each subNode under the grabbed rootNode.

			for subNode in rootNode:

				##  Create a new text label (Log Category column) for the new tree node.

				newTreeNodeLabel = QStandardItem()
				newTreeNodeLabel.setText( subNode )
				newTreeNodeLabel.setSelectable( False )
				newTreeNodeLabel.setEditable( False )


				##  Create a new checkbox (Show? column) for the new tree node.

				newTreeNodeCheckbox = QStandardItem()
				newTreeNodeCheckbox.setCheckable( True )
				newTreeNodeCheckbox.setSelectable( False )
				newTreeNodeCheckbox.setEditable( False )


				##  Add the new tree node components to the temporary helper list being constructed.

				tempListUnderConstruction.append( [ newTreeNodeLabel, newTreeNodeCheckbox ] )


				##  If the new node is a root node, add it to the model.  Otherwise, add the node as a subnode of the current root node.

				if onFirstIndex == True:

					self.treeModel.appendRow( [ newTreeNodeLabel, newTreeNodeCheckbox ] )

					onFirstIndex = False

				else:

					tempListUnderConstruction[ 0 ][ 0 ].appendRow( [ newTreeNodeLabel, newTreeNodeCheckbox ] )
					

			##  Add the temporary helper list to the real active tree nodes list.

			self.activeTreeNodes.append( tempListUnderConstruction )



	##  Class Functions

	def processLogCategoryTreeCheckboxClick( self, checkbox ):

		rootNodeIndexCounter = 0

		for rootNode in self.activeTreeNodes:

			if checkbox == rootNode[ 0 ][ 1 ]:

				if checkbox.checkState() == QtCore.Qt.Checked:

					subNodeIndexCounter = 0

					for subNode in rootNode:

						self.selectedTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter ] = 1

						self.activeTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter ][ 1 ].setCheckState( QtCore.Qt.Checked )

						subNodeIndexCounter = subNodeIndexCounter + 1

				else:

					subNodeIndexCounter = 0

					for subNode in rootNode:

						self.selectedTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter ] = 0

						self.activeTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter ][ 1 ].setCheckState( QtCore.Qt.Unchecked )

						subNodeIndexCounter = subNodeIndexCounter + 1

			else:

				subNodeIndexCounter = 0

				for subNode in rootNode:

					if subNode[ 1 ] == checkbox:

						if checkbox.checkState() == QtCore.Qt.Checked:

							self.selectedTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter - 1 ] = 1

						else:

							self.selectedTreeNodes[ rootNodeIndexCounter ][ subNodeIndexCounter - 1 ] = 0

					subNodeIndexCounter = subNodeIndexCounter + 1

			rootNodeIndexCounter = rootNodeIndexCounter + 1

		return self.selectedTreeNodes
