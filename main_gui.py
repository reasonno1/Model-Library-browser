import sys
import os
import multiprocessing as mp
import threading

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import list_widget
import model_modify_widget
import constant_data
import time


class MainGui(qw.QDialog):

    def __init__(self):
        super(MainGui, self).__init__()

        self.setObjectName("self")
        self.resize(850, 850)
        font = qg.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)

        self.verticalLayout_all = qw.QVBoxLayout(self)
        self.verticalLayout_all.setObjectName("verticalLayout_all")

        self.tabWidget = qw.QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(qc.QRect(0, 0, 850, 850))
        self.verticalLayout_all.addWidget(self.tabWidget)

        ##################### tab 1 #####################

        self.tab_mod = qw.QWidget()
        self.tab_mod.setObjectName("Searching Model")
        self.tabWidget.addTab(self.tab_mod, "Searching Model")

        self.verticalLayout_mod = qw.QVBoxLayout(self.tab_mod)
        self.verticalLayout_mod.setObjectName("verticalLayout_mod")

        self.setWindowFlags(self.windowFlags() | qc.Qt.WindowMinimizeButtonHint | qc.Qt.WindowMaximizeButtonHint)

        ####################### text input & clear btn #######################

        self.horizontal_text_mod = qw.QHBoxLayout(self.tab_mod)
        self.horizontal_text_mod.setObjectName("horizontal_text_mod")
        self.verticalLayout_mod.addLayout(self.horizontal_text_mod)

        self.lineEdit_name = qw.QLineEdit(self.tab_mod)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setPlaceholderText("Filtering")
        self.horizontal_text_mod.addWidget(self.lineEdit_name)

        filter_func = lambda: self.listWidget.text_filtering(
            self.lineEdit_name.text())
        self.lineEdit_name.textChanged.connect(filter_func)

        self.cleartext_btn = qw.QPushButton(self.tab_mod)
        self.cleartext_btn.setObjectName("cleartext_btn")
        self.cleartext_btn.clicked.connect(self.cleartext_btn_clicked)
        self.cleartext_btn.setText(" 清除 ")
        self.horizontal_text_mod.addWidget(self.cleartext_btn)

        ####################### combobox for model lib tags #######################

        self.Combo_modfilter = qw.QComboBox(self.tab_mod)
        self.Combo_modfilter.setObjectName("mod_filter")
        self.Combo_modfilter.setFont(font)
        self.Combo_modfilter.currentIndexChanged.connect(self.cb_modfilter_changed)
        self.verticalLayout_mod.addWidget(self.Combo_modfilter)

        self.horizontal_box = qw.QHBoxLayout(self.tab_mod)
        self.horizontal_box.setObjectName("horizontal_box")
        self.verticalLayout_mod.addLayout(self.horizontal_box)

        ####################### listWidget for model lib #######################

        self.listWidget = list_widget.NameList(self.tab_mod)
        self.listWidget.list_type = "model"
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFont(font)
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setSelectionMode(qw.QAbstractItemView.SingleSelection)

        self.verticalLayout_mod.addWidget(self.listWidget)
        self.model_tag_set = self.listWidget.search_folder()

        self.model_modify_btn = qw.QPushButton(self.tab_mod)
        self.model_modify_btn.setObjectName("model_modify_btn")
        self.model_modify_btn.clicked.connect(self.model_modify_btn_clicked)
        self.model_modify_btn.setText("  資料夾打包輸出 ")
        self.verticalLayout_mod.addWidget(self.model_modify_btn)

        ##################### tab 2 #####################

        self.tab_mat = qw.QWidget()
        self.tab_mat.setObjectName("Searching Material")
        self.tabWidget.addTab(self.tab_mat, "Searching Material")

        self.verticalLayout_mat = qw.QVBoxLayout(self.tab_mat)
        self.verticalLayout_mat.setObjectName("verticalLayout_mat")

        ####################### text_mat input & clear btn #######################

        self.horizontal_text_mat = qw.QHBoxLayout(self.tab_mat)
        self.horizontal_text_mat.setObjectName("horizontal_text")
        self.verticalLayout_mat.addLayout(self.horizontal_text_mat)

        self.lineEdit_name_mat = qw.QLineEdit(self.tab_mod)
        self.lineEdit_name_mat.setObjectName("lineEdit_name_tex")
        self.lineEdit_name_mat.setFont(font)
        self.lineEdit_name_mat.setPlaceholderText("Filtering")
        self.horizontal_text_mat.addWidget(self.lineEdit_name_mat)

        filter_func = lambda: self.listWidget_mat.text_filtering(
            self.lineEdit_name_mat.text())
        self.lineEdit_name_mat.textChanged.connect(filter_func)

        self.cleartext_mat_btn = qw.QPushButton(self.tab_mod)
        self.cleartext_mat_btn.setObjectName("cleartext_mat_btn")
        self.cleartext_mat_btn.clicked.connect(self.cleartext_mat_btn_clicked)
        self.cleartext_mat_btn.setText(" 清除 ")
        self.horizontal_text_mat.addWidget(self.cleartext_mat_btn)


        ####################### combobox for material lib tags #######################

        self.Combo_matfilter = qw.QComboBox(self.tab_mat)
        self.Combo_matfilter.setObjectName("mat_filter")
        self.Combo_matfilter.setFont(font)
        self.add_material_tag()
        self.Combo_matfilter.currentIndexChanged.connect(self.cb_matfilter_changed)
        self.verticalLayout_mat.addWidget(self.Combo_matfilter)

        ####################### listWidget for material lib #######################

        self.listWidget_mat = list_widget.NameList(self.tab_mat)
        self.listWidget_mat.list_type = "material"
        self.listWidget_mat.setObjectName("listWidget_mat")
        self.listWidget_mat.setFont(font)
        self.listWidget_mat.setSortingEnabled(True)
        self.listWidget_mat.setSelectionMode(qw.QAbstractItemView.SingleSelection)

        self.verticalLayout_mat.addWidget(self.listWidget_mat)
        self.listWidget_mat.search_folder()

    ##################### model_modify_btn_clicked fn #####################

    def model_modify_btn_clicked(self):

        model_modify_ui = model_modify_widget.Model_Modify_Gui()
        model_modify_ui.move(15, 125)
        model_modify_ui.show()

    ##################### clear text fn #####################

    def cleartext_mat_btn_clicked(self):

        self.lineEdit_name_mat.setText("")

    ##################### clear text fn #####################

    def cleartext_btn_clicked(self):

        self.lineEdit_name.setText("")

    ##################### model combobox fn #####################

    def add_model_tag(self, model_tag_set):
        count = 0
        for i in model_tag_set:
            self.Combo_modfilter.addItem(str(count))
            self.Combo_modfilter.setItemText(count, i)
            count += 1

    def cb_modfilter_changed(self):
        tag = self.Combo_modfilter.currentText()
        if tag and tag != "0":
            text = self.lineEdit_name.text() + tag + " "
            self.lineEdit_name.setText(text)

    ##################### material combobox fn #####################

    def add_material_tag(self):
        count = 0
        for i in constant_data.Data.MATERIAL_LIST:
            self.Combo_matfilter.addItem(str(count))
            self.Combo_matfilter.setItemText(count, i)
            count += 1

    def cb_matfilter_changed(self):
        tag = self.Combo_matfilter.currentText()
        if tag and tag != "0":
            text = self.lineEdit_name_mat.text() + tag + " "
            self.lineEdit_name_mat.setText(text)
            # self.listWidget_mat.text_filtering_mat(tag)

    ##################### list_widget threading #####################

class Worker(threading.Thread):

    def __init__(self, trigger, list_widget):
        super().__init__()

        self.trigger = trigger
        self.list_widget = list_widget

    def run(self):

        root = self.list_widget.generate_root_by_type()

        re = []
        temp = 0
        for i in range(self.list_widget.count()):
            full_path = os.path.join(root[1], "re_" + self.list_widget.item(i).text() + ".jpg")
            icon = qg.QIcon(full_path)
            re.append((self.list_widget.item(i), icon))
            temp += 1
            if temp == 150:
                self.trigger.emit(re)
                temp = 0
                re = []

        self.trigger.emit(re)



if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    splash_screen = qg.QPixmap(constant_data.Data.SPLASH_SCREEN)
    splash = qw.QSplashScreen(splash_screen, qc.Qt.WindowStaysOnTopHint)

    splash.show()

    app.processEvents()
    ui = MainGui()
    ui.show()
    splash.finish(ui)

    worker_model = Worker(ui.listWidget.icon_trigger, ui.listWidget)
    worker_model.start()


    worker_mat = Worker(ui.listWidget_mat.icon_trigger, ui.listWidget_mat)
    worker_mat.start()

    ui.add_model_tag(ui.model_tag_set)


    sys.exit(app.exec_())



