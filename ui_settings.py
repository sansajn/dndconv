# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sun Sep 28 13:28:50 2014
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(400, 131)
        self.formLayoutWidget = QtGui.QWidget(Settings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 90))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditDir = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEditDir.setObjectName(_fromUtf8("lineEditDir"))
        self.horizontalLayout.addWidget(self.lineEditDir)
        self.pushButton = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEditBitrate = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEditBitrate.setObjectName(_fromUtf8("lineEditBitrate"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditBitrate)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEditFormat = QtGui.QLineEdit(self.formLayoutWidget)
        self.lineEditFormat.setObjectName(_fromUtf8("lineEditFormat"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditFormat)
        self.verticalLayoutWidget = QtGui.QWidget(Settings)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 381, 32))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line = QtGui.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.lineEditCmd = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEditCmd.setObjectName(_fromUtf8("lineEditCmd"))
        self.verticalLayout.addWidget(self.lineEditCmd)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Settings", None))
        self.label.setText(_translate("Settings", "Output directory:", None))
        self.lineEditDir.setText(_translate("Settings", "~/temp/extract_test", None))
        self.pushButton.setText(_translate("Settings", "...", None))
        self.label_2.setText(_translate("Settings", "Bitrate (kbps):", None))
        self.lineEditBitrate.setText(_translate("Settings", "192", None))
        self.label_3.setText(_translate("Settings", "Format (mp3, aac, ogg):", None))
        self.lineEditFormat.setText(_translate("Settings", "mp3", None))
        self.lineEditCmd.setText(_translate("Settings", "-vn", None))

