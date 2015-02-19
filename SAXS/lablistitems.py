import os
import platform
import sys,json
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lablistactionitem import LablistActionItem
class Lablistitems(QObject):
	def __init__(self,listlayout):
		super(Lablistitems,self).__init__()
		self.checklist=json.load(open(os.path.dirname(__file__)+os.sep+"checklist.json"))
		self.listlayout=listlayout
		self.progressitem=0
		self.actionwidgets=[]
		for item in self.checklist:
			itemwidget=LablistActionItem(item)
			self.actionwidgets.append(itemwidget)
			self.listlayout.addWidget(itemwidget)
		self.actionwidgets[0].show()
		self.next=1
		self.nextbutton=QPushButton("Next")
		self.nextbutton.hide()
		self.listlayout.addWidget(self.nextbutton)
		self.listlayout.addStretch()
		self.connect(self.nextbutton, SIGNAL("pressed()"),self.shownextitem)
	def shownextitem(self):
		self.actionwidgets[self.next].show()
		self.next+=1
		if self.next>=len(self.actionwidgets):
			self.nextbutton.hide()
	def shownextbutton(self):
		if self.next<len(self.actionwidgets):
			self.nextbutton.show()