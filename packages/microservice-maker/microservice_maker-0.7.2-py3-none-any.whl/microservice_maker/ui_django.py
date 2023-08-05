# -*- coding: utf-8 -*-

##########################################################################
# Form generated from reading UI file 'teste.ui'
##
# Created by: Qt User Interface Compiler version 6.0.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##########################################################################
import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from microservice_maker.flask_maker import FlaskMaker
from microservice_maker.django_maker import (
    DjangoMaker,
    HERE
)


class UiMainUi(object):
    def setupUi(self, MainUi):
        if not MainUi.objectName():
            MainUi.setObjectName(u"MainUi")
        MainUi.resize(900, 600)
        MainUi.setWindowIcon(QIcon(os.path.join(HERE, "logo.py")))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(46, 52, 54, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(69, 78, 81, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(57, 65, 67, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(23, 26, 27, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(31, 35, 36, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush6)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        brush8 = QBrush(QColor(239, 239, 239, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        brush9 = QBrush(QColor(202, 202, 202, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush9)
        brush10 = QBrush(QColor(159, 159, 159, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush10)
        brush11 = QBrush(QColor(184, 184, 184, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush11)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush8)
        brush12 = QBrush(QColor(118, 118, 118, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush12)
        brush13 = QBrush(QColor(247, 247, 247, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush13)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush14 = QBrush(QColor(177, 177, 177, 255))
        brush14.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush14)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush13)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        MainUi.setPalette(palette)
        self.centralwidget = QWidget(MainUi)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(900, 600))
        self.centralwidget.setAutoFillBackground(True)
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(0, 0, 801, 591))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.nomeAPPLabel = QLabel(self.formLayoutWidget)
        self.nomeAPPLabel.setObjectName(u"nomeAPPLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nomeAPPLabel)

        self.nome_input = QLineEdit(self.formLayoutWidget)
        self.nome_input.setObjectName(u"nome_input")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nome_input)

        self.portaAPPLabel = QLabel(self.formLayoutWidget)
        self.portaAPPLabel.setObjectName(u"portaAPPLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.portaAPPLabel)

        self.porta_input = QLineEdit(self.formLayoutWidget)
        self.porta_input.setObjectName(u"porta_input")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.porta_input)

        self.bancoDeDadosPortaLabel = QLabel(self.formLayoutWidget)
        self.bancoDeDadosPortaLabel.setObjectName(u"bancoDeDadosPortaLabel")

        self.formLayout.setWidget(
            2, QFormLayout.LabelRole, self.bancoDeDadosPortaLabel)

        self.bd_porta_input = QLineEdit(self.formLayoutWidget)
        self.bd_porta_input.setObjectName(u"bd_porta_input")

        self.formLayout.setWidget(
            2, QFormLayout.FieldRole, self.bd_porta_input)

        self.pythonVersOLabel = QLabel(self.formLayoutWidget)
        self.pythonVersOLabel.setObjectName(u"pythonVersOLabel")

        self.formLayout.setWidget(
            3, QFormLayout.LabelRole, self.pythonVersOLabel)

        self.python_input = QLineEdit(self.formLayoutWidget)
        self.python_input.setObjectName(u"python_input")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.python_input)

        self.postgresUsuRioLabel = QLabel(self.formLayoutWidget)
        self.postgresUsuRioLabel.setObjectName(u"postgresUsuRioLabel")

        self.formLayout.setWidget(
            4, QFormLayout.LabelRole, self.postgresUsuRioLabel)

        self.user_input = QLineEdit(self.formLayoutWidget)
        self.user_input.setObjectName(u"user_input")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.user_input)

        self.postgresSenhaLabel = QLabel(self.formLayoutWidget)
        self.postgresSenhaLabel.setObjectName(u"postgresSenhaLabel")

        self.formLayout.setWidget(
            5, QFormLayout.LabelRole, self.postgresSenhaLabel)

        self.password_input = QLineEdit(self.formLayoutWidget)
        self.password_input.setObjectName(u"password_input")

        self.formLayout.setWidget(
            5, QFormLayout.FieldRole, self.password_input)

        self.postgresHostLabel = QLabel(self.formLayoutWidget)
        self.postgresHostLabel.setObjectName(u"postgresHostLabel")

        self.formLayout.setWidget(
            6, QFormLayout.LabelRole, self.postgresHostLabel)
        
        self.ServiceLabel = QLabel(self.formLayoutWidget)
        self.ServiceLabel.setObjectName(u"ServiceLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.ServiceLabel)

        self.service_type = QLineEdit(self.formLayoutWidget)
        self.service_type.setObjectName(u"service_type")

        self.formLayout.setWidget(
            7, QFormLayout.FieldRole, self.service_type)


        self.bd_input = QLineEdit(self.formLayoutWidget)
        self.bd_input.setObjectName(u"bd_input")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.bd_input)

        self.submitButton = QPushButton(self.formLayoutWidget)
        self.submitButton.setObjectName(u"submitButton")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.submitButton)

        MainUi.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainUi)
        self.submitButton.clicked.connect(self.make_request)
        QMetaObject.connectSlotsByName(MainUi)
    # setupUi

    def make_request(self):
        print("Request")
        user_args = {}
        if self.service_type.text() == "django":
            user_args["app_name"] = self.nome_input.text()
            user_args["app_port"] = self.porta_input.text()
            user_args["db_port"] = self.bd_porta_input.text()
            user_args["python_version"] = self.python_input.text()
            user_args["postgres_user"] = self.user_input.text()
            user_args["postgres_password"] = self.password_input.text()
            user_args["postgres_db"] = self.bd_input.text()
            user_args["path"] = QFileDialog.getExistingDirectory(
                self.formLayoutWidget,
                "select dir",
                "/home/victorhdcoelho/")
            print(user_args)
            dj = DjangoMaker(user_args)
            dj.run_subs_dockers()
        else:
            user_args["app_name"] = self.nome_input.text()
            user_args["app_port"] = self.porta_input.text()
            user_args["db_port"] = self.bd_porta_input.text()
            user_args["python_version"] = self.python_input.text()
            user_args["postgres_user"] = self.user_input.text()
            user_args["postgres_password"] = self.password_input.text()
            user_args["postgres_db"] = self.bd_input.text()
            user_args["path"] = QFileDialog.getExistingDirectory(
                self.formLayoutWidget,
                "select dir",
                "/home/victorhdcoelho/")
            print(user_args)
            fl = FlaskMaker(user_args)
            fl.run()

        sys.exit()

    def retranslateUi(self, MainUi):
        MainUi.setWindowTitle(
            QCoreApplication.translate(
                "MainUi", u"Django Maker", None))
        self.nomeAPPLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Nome APP", None))
        self.portaAPPLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Porta APP", None))
        self.bancoDeDadosPortaLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Banco de dados porta", None))
        self.pythonVersOLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Python Vers\u00e3o", None))
        self.postgresUsuRioLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Postgres Usu\u00e1rio", None))
        self.postgresSenhaLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Postgres Senha", None))
        self.postgresHostLabel.setText(
            QCoreApplication.translate(
                "MainUi", u"Postgres Host", None))
        self.submitButton.setText(
            QCoreApplication.translate(
                "MainUi", u"Submit", None))
    # retranslateUi
