# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QSplitter, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 850)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1400, 22))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.actionUiFontSize = QAction(MainWindow)
        self.actionUiFontSize.setObjectName(u"actionUiFontSize")
        self.menuSettings.addAction(self.actionUiFontSize)
        self.actionShortcutSettings = QAction(MainWindow)
        self.actionShortcutSettings.setObjectName(u"actionShortcutSettings")
        self.menuSettings.addAction(self.actionShortcutSettings)
        self.menuLanguage = QMenu(self.menuSettings)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuSettings.addMenu(self.menuLanguage)
        self.menubar.addAction(self.menuSettings.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.btnImport = QPushButton(self.centralwidget)
        self.btnImport.setObjectName(u"btnImport")

        self.toolbarLayout.addWidget(self.btnImport)

        self.btnImportPrompt = QPushButton(self.centralwidget)
        self.btnImportPrompt.setObjectName(u"btnImportPrompt")

        self.toolbarLayout.addWidget(self.btnImportPrompt)

        self.btnPrevious = QPushButton(self.centralwidget)
        self.btnPrevious.setObjectName(u"btnPrevious")

        self.toolbarLayout.addWidget(self.btnPrevious)

        self.btnNext = QPushButton(self.centralwidget)
        self.btnNext.setObjectName(u"btnNext")

        self.toolbarLayout.addWidget(self.btnNext)

        self.btnZoomIn = QPushButton(self.centralwidget)
        self.btnZoomIn.setObjectName(u"btnZoomIn")

        self.toolbarLayout.addWidget(self.btnZoomIn)

        self.btnZoomOut = QPushButton(self.centralwidget)
        self.btnZoomOut.setObjectName(u"btnZoomOut")

        self.toolbarLayout.addWidget(self.btnZoomOut)

        self.btnFit = QPushButton(self.centralwidget)
        self.btnFit.setObjectName(u"btnFit")

        self.toolbarLayout.addWidget(self.btnFit)

        self.btnSave = QPushButton(self.centralwidget)
        self.btnSave.setObjectName(u"btnSave")

        self.toolbarLayout.addWidget(self.btnSave)


        self.verticalLayout.addLayout(self.toolbarLayout)

        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.leftPanel = QWidget(self.mainSplitter)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftLayout = QVBoxLayout(self.leftPanel)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.labelImages = QLabel(self.leftPanel)
        self.labelImages.setObjectName(u"labelImages")

        self.leftLayout.addWidget(self.labelImages)

        self.imageList = QListWidget(self.leftPanel)
        self.imageList.setObjectName(u"imageList")

        self.leftLayout.addWidget(self.imageList)

        self.labelStats = QLabel(self.leftPanel)
        self.labelStats.setObjectName(u"labelStats")

        self.leftLayout.addWidget(self.labelStats)

        self.mainSplitter.addWidget(self.leftPanel)
        self.centerPanel = QWidget(self.mainSplitter)
        self.centerPanel.setObjectName(u"centerPanel")
        self.centerLayout = QVBoxLayout(self.centerPanel)
        self.centerLayout.setObjectName(u"centerLayout")
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.labelPreview = QLabel(self.centerPanel)
        self.labelPreview.setObjectName(u"labelPreview")

        self.centerLayout.addWidget(self.labelPreview)

        self.viewerContainer = QWidget(self.centerPanel)
        self.viewerContainer.setObjectName(u"viewerContainer")

        self.centerLayout.addWidget(self.viewerContainer)

        self.labelImageInfo = QLabel(self.centerPanel)
        self.labelImageInfo.setObjectName(u"labelImageInfo")

        self.centerLayout.addWidget(self.labelImageInfo)

        self.mainSplitter.addWidget(self.centerPanel)
        self.rightPanel = QWidget(self.mainSplitter)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightLayout = QVBoxLayout(self.rightPanel)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.labelPrompt = QLabel(self.rightPanel)
        self.labelPrompt.setObjectName(u"labelPrompt")

        self.rightLayout.addWidget(self.labelPrompt)

        self.promptFontSizeLayout = QHBoxLayout()
        self.promptFontSizeLayout.setObjectName(u"promptFontSizeLayout")
        self.labelPromptFontSize = QLabel(self.rightPanel)
        self.labelPromptFontSize.setObjectName(u"labelPromptFontSize")

        self.promptFontSizeLayout.addWidget(self.labelPromptFontSize)

        self.spinPromptFontSize = QSpinBox(self.rightPanel)
        self.spinPromptFontSize.setObjectName(u"spinPromptFontSize")
        self.spinPromptFontSize.setMinimum(8)
        self.spinPromptFontSize.setMaximum(48)
        self.spinPromptFontSize.setSingleStep(1)
        self.spinPromptFontSize.setValue(10)

        self.promptFontSizeLayout.addWidget(self.spinPromptFontSize)

        self.rightLayout.addLayout(self.promptFontSizeLayout)

        self.captionEditor = QTextEdit(self.rightPanel)
        self.captionEditor.setObjectName(u"captionEditor")

        self.rightLayout.addWidget(self.captionEditor)

        self.labelCaptionStatus = QLabel(self.rightPanel)
        self.labelCaptionStatus.setObjectName(u"labelCaptionStatus")

        self.rightLayout.addWidget(self.labelCaptionStatus)

        self.mainSplitter.addWidget(self.rightPanel)

        self.verticalLayout.addWidget(self.mainSplitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Image Caption Studio v1.0", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actionUiFontSize.setText(QCoreApplication.translate("MainWindow", u"\u754c\u9762\u5b57\u53f7...", None))
        self.actionShortcutSettings.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u6377\u952e...", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"\u8bed\u8a00", None))
        self.btnImport.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u56fe\u7247\u76ee\u5f55", None))
        self.btnImportPrompt.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165Prompt\u76ee\u5f55", None))
        self.btnPrevious.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u5f20", None))
        self.btnNext.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u5f20", None))
        self.btnZoomIn.setText(QCoreApplication.translate("MainWindow", u"\u653e\u5927", None))
        self.btnZoomOut.setText(QCoreApplication.translate("MainWindow", u"\u7f29\u5c0f", None))
        self.btnFit.setText(QCoreApplication.translate("MainWindow", u"\u9002\u5e94\u7a97\u53e3", None))
        self.btnSave.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58 Prompt", None))
        self.labelImages.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u5217\u8868", None))
        self.labelStats.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u6807\u6ce8\uff1a0 / 0", None))
        self.labelPreview.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9884\u89c8", None))
        self.labelImageInfo.setText(QCoreApplication.translate("MainWindow", u"\u5c1a\u672a\u52a0\u8f7d\u56fe\u7247", None))
        self.labelPrompt.setText(QCoreApplication.translate("MainWindow", u"Prompt \u6807\u6ce8", None))
        self.labelPromptFontSize.setText(QCoreApplication.translate("MainWindow", u"\u5b57\u53f7\uff1a", None))
        self.spinPromptFontSize.setSuffix(QCoreApplication.translate("MainWindow", u" pt", None))
        self.captionEditor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u56fe\u7247\u7684\u6587\u672c\u63cf\u8ff0...", None))
        self.labelCaptionStatus.setText(QCoreApplication.translate("MainWindow", u"\u672a\u6807\u6ce8", None))
    # retranslateUi

