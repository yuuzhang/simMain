/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QComboBox *cmBox_RoutingName;
    QLineEdit *lnEdit_Prog;
    QPushButton *pBtn_file;
    QLabel *label;
    QSpinBox *spinBox_processes;
    QListWidget *listWidget_activeProg;
    QLabel *label_2;
    QLineEdit *lnEdit_loadStart;
    QLabel *label_3;
    QLineEdit *lnEdit_loadEnd;
    QLineEdit *lnEdit_loadStep;
    QLabel *label_4;
    QComboBox *cmBox_SimulationSpan;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QLabel *label_8;
    QLabel *label_9;
    QPushButton *pBtn_Run;
    QTextBrowser *QtxtBroOutput;
    QLabel *label_10;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(976, 661);
        QFont font;
        font.setFamily(QStringLiteral("Hei"));
        MainWindow->setFont(font);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        cmBox_RoutingName = new QComboBox(centralWidget);
        cmBox_RoutingName->setObjectName(QStringLiteral("cmBox_RoutingName"));
        cmBox_RoutingName->setGeometry(QRect(290, 100, 311, 25));
        lnEdit_Prog = new QLineEdit(centralWidget);
        lnEdit_Prog->setObjectName(QStringLiteral("lnEdit_Prog"));
        lnEdit_Prog->setGeometry(QRect(140, 30, 641, 25));
        pBtn_file = new QPushButton(centralWidget);
        pBtn_file->setObjectName(QStringLiteral("pBtn_file"));
        pBtn_file->setGeometry(QRect(780, 30, 61, 25));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(40, 30, 101, 21));
        spinBox_processes = new QSpinBox(centralWidget);
        spinBox_processes->setObjectName(QStringLiteral("spinBox_processes"));
        spinBox_processes->setGeometry(QRect(140, 190, 151, 21));
        listWidget_activeProg = new QListWidget(centralWidget);
        listWidget_activeProg->setObjectName(QStringLiteral("listWidget_activeProg"));
        listWidget_activeProg->setGeometry(QRect(140, 220, 781, 171));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(140, 70, 191, 21));
        lnEdit_loadStart = new QLineEdit(centralWidget);
        lnEdit_loadStart->setObjectName(QStringLiteral("lnEdit_loadStart"));
        lnEdit_loadStart->setGeometry(QRect(330, 70, 121, 25));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(460, 70, 21, 21));
        lnEdit_loadEnd = new QLineEdit(centralWidget);
        lnEdit_loadEnd->setObjectName(QStringLiteral("lnEdit_loadEnd"));
        lnEdit_loadEnd->setGeometry(QRect(490, 70, 121, 25));
        lnEdit_loadStep = new QLineEdit(centralWidget);
        lnEdit_loadStep->setObjectName(QStringLiteral("lnEdit_loadStep"));
        lnEdit_loadStep->setGeometry(QRect(660, 70, 121, 25));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(620, 70, 41, 21));
        cmBox_SimulationSpan = new QComboBox(centralWidget);
        cmBox_SimulationSpan->setObjectName(QStringLiteral("cmBox_SimulationSpan"));
        cmBox_SimulationSpan->setGeometry(QRect(290, 130, 311, 25));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(140, 100, 191, 21));
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(140, 130, 191, 21));
        label_7 = new QLabel(centralWidget);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(40, 190, 101, 21));
        label_8 = new QLabel(centralWidget);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(670, 140, 131, 51));
        QFont font1;
        font1.setPointSize(28);
        label_8->setFont(font1);
        label_9 = new QLabel(centralWidget);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(40, 220, 101, 21));
        pBtn_Run = new QPushButton(centralWidget);
        pBtn_Run->setObjectName(QStringLiteral("pBtn_Run"));
        pBtn_Run->setGeometry(QRect(40, 580, 131, 51));
        QFont font2;
        font2.setPointSize(22);
        pBtn_Run->setFont(font2);
        QtxtBroOutput = new QTextBrowser(centralWidget);
        QtxtBroOutput->setObjectName(QStringLiteral("QtxtBroOutput"));
        QtxtBroOutput->setGeometry(QRect(140, 400, 781, 161));
        label_10 = new QLabel(centralWidget);
        label_10->setObjectName(QStringLiteral("label_10"));
        label_10->setGeometry(QRect(810, 140, 121, 51));
        QPalette palette;
        QBrush brush(QColor(0, 0, 0, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush);
        QBrush brush1(QColor(86, 241, 148, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Button, brush1);
        QBrush brush2(QColor(198, 255, 221, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Light, brush2);
        QBrush brush3(QColor(142, 248, 184, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Midlight, brush3);
        QBrush brush4(QColor(43, 120, 74, 255));
        brush4.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Dark, brush4);
        QBrush brush5(QColor(57, 161, 99, 255));
        brush5.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Mid, brush5);
        palette.setBrush(QPalette::Active, QPalette::Text, brush);
        QBrush brush6(QColor(255, 255, 255, 255));
        brush6.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::BrightText, brush6);
        palette.setBrush(QPalette::Active, QPalette::ButtonText, brush);
        palette.setBrush(QPalette::Active, QPalette::Base, brush6);
        palette.setBrush(QPalette::Active, QPalette::Window, brush1);
        palette.setBrush(QPalette::Active, QPalette::Shadow, brush);
        QBrush brush7(QColor(170, 248, 201, 255));
        brush7.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::AlternateBase, brush7);
        QBrush brush8(QColor(255, 255, 220, 255));
        brush8.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::ToolTipBase, brush8);
        palette.setBrush(QPalette::Active, QPalette::ToolTipText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Button, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Light, brush2);
        palette.setBrush(QPalette::Inactive, QPalette::Midlight, brush3);
        palette.setBrush(QPalette::Inactive, QPalette::Dark, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::Mid, brush5);
        palette.setBrush(QPalette::Inactive, QPalette::Text, brush);
        palette.setBrush(QPalette::Inactive, QPalette::BrightText, brush6);
        palette.setBrush(QPalette::Inactive, QPalette::ButtonText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush6);
        palette.setBrush(QPalette::Inactive, QPalette::Window, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Shadow, brush);
        palette.setBrush(QPalette::Inactive, QPalette::AlternateBase, brush7);
        palette.setBrush(QPalette::Inactive, QPalette::ToolTipBase, brush8);
        palette.setBrush(QPalette::Inactive, QPalette::ToolTipText, brush);
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Button, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Light, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Midlight, brush3);
        palette.setBrush(QPalette::Disabled, QPalette::Dark, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Mid, brush5);
        palette.setBrush(QPalette::Disabled, QPalette::Text, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::BrightText, brush6);
        palette.setBrush(QPalette::Disabled, QPalette::ButtonText, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Window, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Shadow, brush);
        palette.setBrush(QPalette::Disabled, QPalette::AlternateBase, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::ToolTipBase, brush8);
        palette.setBrush(QPalette::Disabled, QPalette::ToolTipText, brush);
        label_10->setPalette(palette);
        label_10->setFont(font1);
        MainWindow->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "ndnSIM Simulation Main Controller-----2017-10-8", Q_NULLPTR));
        cmBox_RoutingName->setCurrentText(QString());
        pBtn_file->setText(QApplication::translate("MainWindow", "\346\265\217\350\247\210...", Q_NULLPTR));
        label->setText(QApplication::translate("MainWindow", "<html><head/><body><p>\344\273\277\347\234\237\346\211\247\350\241\214\347\250\213\345\272\217:</p></body></html>", Q_NULLPTR));
        label_2->setText(QApplication::translate("MainWindow", "<html><head/><body><p>InterestsPerSec---------From:</p></body></html>", Q_NULLPTR));
        label_3->setText(QApplication::translate("MainWindow", "<html><head/><body><p>To:</p></body></html>", Q_NULLPTR));
        label_4->setText(QApplication::translate("MainWindow", "<html><head/><body><p>Step:</p></body></html>", Q_NULLPTR));
        label_5->setText(QApplication::translate("MainWindow", "<html><head/><body><p>RoutingName:</p></body></html>", Q_NULLPTR));
        label_6->setText(QApplication::translate("MainWindow", "<html><head/><body><p>SimulationSpan:</p></body></html>", Q_NULLPTR));
        label_7->setText(QApplication::translate("MainWindow", "<html><head/><body><p>\350\277\233\347\250\213\346\225\260\351\207\217\351\231\220\345\210\266:</p></body></html>", Q_NULLPTR));
        label_8->setText(QApplication::translate("MainWindow", "<html><head/><body><p><span style=\" color:#4c8912;\">CPU\345\215\240\347\224\250:</span></p></body></html>", Q_NULLPTR));
        label_9->setText(QApplication::translate("MainWindow", "<html><head/><body><p>\345\275\223\345\211\215\350\277\220\350\241\214\350\277\233\347\250\213\357\274\232</p></body></html>", Q_NULLPTR));
        pBtn_Run->setText(QApplication::translate("MainWindow", "\345\274\200\345\247\213\344\273\277\347\234\237", Q_NULLPTR));
        label_10->setText(QApplication::translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600; color:#50a2e2;\">0%</span></p></body></html>", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
