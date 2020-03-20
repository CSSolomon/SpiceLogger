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



class LogEntriesList( QListView ):

	##  Class Constructor

	def __init__( self ):

		##  Call the parent constructor.

		super( LogEntriesList, self ).__init__()


		##  Set the model for this QListView.

		self.listModel = QStandardItemModel()

		self.setModel( self.listModel )


		##  Set the spacing between QListView list elements.

		self.setSpacing( 2 )



	##  Class Functions

	def processLogCategoryTreeCheckboxClick( self, selectedTreeNodes ):

		##  Clear out all old entries.

		self.listModel.removeRows( 0, self.listModel.rowCount() )


		##  Open the local authentication log file for reading only.

		localAuthenticationLog = open( "/var/log/auth.log", "r" )


		##  Sorts parsed log entries.

		for logEntry in localAuthenticationLog:

			if ( selectedTreeNodes[ 0 ][ 0 ] == 1 ) and ( "gdm-password:session" in logEntry ) and ( "session opened" in logEntry ):

				splitLogEntry = logEntry.rstrip().split()

				logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

				logEntryTime = splitLogEntry[ 2 ]

				logEntryHostname = splitLogEntry[ 3 ]

				logEntryUsername = splitLogEntry[ 10 ]

				listEntry = QStandardItem()

				listEntry.setBackground( QColor(0, 0, 255, 96) )

				listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tNew Session User Login\tUser: " + logEntryUsername +"\tHost: " + logEntryHostname )

				self.listModel.appendRow( listEntry )

			elif ( selectedTreeNodes[ 0 ][ 1 ] == 1 ) and ( "gdm-password" in logEntry ) and ( "gkr-pam" in logEntry ) and ( "unlocked login keyring" in logEntry ):

				splitLogEntry = logEntry.rstrip().split()

				logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

				logEntryTime = splitLogEntry[ 2 ]

				logEntryHostname = splitLogEntry[ 3 ]

				listEntry = QStandardItem()

				listEntry.setBackground( QColor(0, 0, 255, 48) )

				listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tExisting Session User Login\tHost: " + logEntryHostname )

				self.listModel.appendRow( listEntry )

			elif ( selectedTreeNodes[ 0 ][ 2 ] == 1 ) and ( "systemd-logind" in logEntry ) and ( "New seat" in logEntry ):

				splitLogEntry = logEntry.rstrip().split()

				logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

				logEntryTime = splitLogEntry[ 2 ]

				logEntryHostname = splitLogEntry[ 3 ]

				listEntry = QStandardItem()

				listEntry.setBackground( QColor(0, 255, 0, 96) )

				listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tSystem Power-On\tHost: " + logEntryHostname )

				self.listModel.appendRow( listEntry )

			elif ( selectedTreeNodes[ 0 ][ 3 ] == 1 ) and ( "systemd-logind" in logEntry ) and ( "System is powering down" in logEntry ):

				splitLogEntry = logEntry.rstrip().split()

				logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

				logEntryTime = splitLogEntry[ 2 ]

				logEntryHostname = splitLogEntry[ 3 ]

				listEntry = QStandardItem()

				listEntry.setBackground( QColor(0, 255, 0, 48) )

				listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tSystem Power-Off\tHost: " + logEntryHostname )

				self.listModel.appendRow( listEntry )

			elif ( "sudo" in logEntry ) and ( "PWD" in logEntry ) and ( "USER" in logEntry ) and ( "COMMAND" in logEntry ):

				if ( selectedTreeNodes[ 0 ][ 5 ] == 1 ) and ( "incorrect password" in logEntry ):

					splitLogEntry = logEntry.rstrip().split()

					logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

					logEntryTime = splitLogEntry[ 2 ]

					logEntryHostname = splitLogEntry[ 3 ]

					logEntryUsername = splitLogEntry[ 5 ]

					logEntryAttemptsNumber = splitLogEntry[ 7 ]

					splitLogEntryCommand = splitLogEntry[ 18: ]

					logEntryCommand = ""

					for commandSegment in splitLogEntryCommand:

						logEntryCommand = logEntryCommand + commandSegment + " "

					logEntryCommand = logEntryCommand[ 8: ]

					listEntry = QStandardItem()

					listEntry.setBackground( QColor(255, 0, 0, 96) )

					listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tFailed Sudo Command (" + logEntryAttemptsNumber + " Tries)\tUser: " + logEntryUsername +"\tHost: " + logEntryHostname + "\tCommand: " + logEntryCommand )

					self.listModel.appendRow( listEntry )

				elif ( selectedTreeNodes[ 0 ][ 4 ] == 1 ):

					splitLogEntry = logEntry.rstrip().split()

					logEntryDate = splitLogEntry[ 0 ] + " " + splitLogEntry[ 1 ]

					logEntryTime = splitLogEntry[ 2 ]

					logEntryHostname = splitLogEntry[ 3 ]

					logEntryUsername = splitLogEntry[ 5 ]

					splitLogEntryCommand = splitLogEntry[ 13: ]

					logEntryCommand = ""

					for commandSegment in splitLogEntryCommand:

						logEntryCommand = logEntryCommand + commandSegment + " "

					logEntryCommand = logEntryCommand[ 8: ]

					listEntry = QStandardItem()

					listEntry.setBackground( QColor(255, 0, 0, 48) )

					listEntry.setText( logEntryDate + "\t" + logEntryTime + "\tSuccessful Sudo Command\tUser: " + logEntryUsername +"\tHost: " + logEntryHostname + "\tCommand: " + logEntryCommand )

					self.listModel.appendRow( listEntry )


		##  Closes the open log file.

		localAuthenticationLog.close()

		return
