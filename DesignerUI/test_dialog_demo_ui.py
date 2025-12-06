# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_dialog_demo.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SimpleDialog(object):
    def setupUi(self, SimpleDialog):
        if not SimpleDialog.objectName():
            SimpleDialog.setObjectName(u"SimpleDialog")
        SimpleDialog.resize(1287, 978)
        self.verticalLayout = QVBoxLayout(SimpleDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(SimpleDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 16777186))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.pushButton = QPushButton(SimpleDialog)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 34, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_2 = QPushButton(SimpleDialog)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(SimpleDialog)

        QMetaObject.connectSlotsByName(SimpleDialog)
    # setupUi

    def retranslateUi(self, SimpleDialog):
        SimpleDialog.setWindowTitle(QCoreApplication.translate("SimpleDialog", u"Einfacher Dialog", None))
        self.label.setText(QCoreApplication.translate("SimpleDialog", u"Dies ist ein einfaches Beispiel-UI.", None))
        self.pushButton.setText(QCoreApplication.translate("SimpleDialog", u"Klick mich!", None))
        self.pushButton_2.setText(QCoreApplication.translate("SimpleDialog", u"Test", None))
    # retranslateUi

