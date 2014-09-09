# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importdialog.ui'
#
# Created: Wed Jul 16 09:16:17 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(782, 508)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEditbuffer = QtGui.QTextEdit(Dialog)
        self.textEditbuffer.setObjectName(_fromUtf8("textEditbuffer"))
        self.verticalLayout.addWidget(self.textEditbuffer)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonAbort = QtGui.QPushButton(Dialog)
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))
        self.horizontalLayout_2.addWidget(self.pushButtonAbort)
        self.pushButtonLoadFile = QtGui.QPushButton(Dialog)
        self.pushButtonLoadFile.setObjectName(_fromUtf8("pushButtonLoadFile"))
        self.horizontalLayout_2.addWidget(self.pushButtonLoadFile)
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.horizontalLayout_2.addWidget(self.pushButtonOK)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButtonAbort.setText(_translate("Dialog", "Abort", None))
        self.pushButtonLoadFile.setText(_translate("Dialog", "Load File", None))
        self.pushButtonOK.setText(_translate("Dialog", "Ok", None))

