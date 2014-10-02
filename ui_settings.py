# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Thu Oct  2 19:47:31 2014
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
        Settings.resize(400, 153)
        self.formLayoutWidget = QtGui.QWidget(Settings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 111))
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
        self.pushButtonOutDir = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButtonOutDir.setFlat(False)
        self.pushButtonOutDir.setObjectName(_fromUtf8("pushButtonOutDir"))
        self.horizontalLayout.addWidget(self.pushButtonOutDir)
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
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBoxOverwrite = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBoxOverwrite.setObjectName(_fromUtf8("comboBoxOverwrite"))
        self.comboBoxOverwrite.addItem(_fromUtf8(""))
        self.comboBoxOverwrite.addItem(_fromUtf8(""))
        self.comboBoxOverwrite.addItem(_fromUtf8(""))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxOverwrite)
        self.verticalLayoutWidget = QtGui.QWidget(Settings)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 120, 381, 32))
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
        self.pushButtonOutDir.setText(_translate("Settings", "...", None))
        self.label_2.setText(_translate("Settings", "Bitrate (kbps):", None))
        self.lineEditBitrate.setText(_translate("Settings", "192", None))
        self.label_3.setText(_translate("Settings", "Format (mp3, aac, ogg):", None))
        self.lineEditFormat.setText(_translate("Settings", "mp3", None))
        self.label_4.setText(_translate("Settings", "Overwrite:", None))
        self.comboBoxOverwrite.setItemText(0, _translate("Settings", "Yes", None))
        self.comboBoxOverwrite.setItemText(1, _translate("Settings", "No", None))
        self.comboBoxOverwrite.setItemText(2, _translate("Settings", "Skip", None))
        self.lineEditCmd.setText(_translate("Settings", "-vn", None))

