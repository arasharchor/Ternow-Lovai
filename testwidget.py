# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TestWidget(object):
    def setupUi(self, TestWidget):
        TestWidget.setObjectName("TestWidget")
        TestWidget.resize(1920, 1080)
        TestWidget.setStyleSheet("background: url(:/Users/christiannauck/Test.jpg)")

        self.retranslateUi(TestWidget)
        QtCore.QMetaObject.connectSlotsByName(TestWidget)

    def retranslateUi(self, TestWidget):
        _translate = QtCore.QCoreApplication.translate
        TestWidget.setWindowTitle(_translate("TestWidget", "TestWidget"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TestWidget = QtWidgets.QWidget()
    ui = Ui_TestWidget()
    ui.setupUi(TestWidget)
    TestWidget.show()
    sys.exit(app.exec_())

