
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import os
import sys


class find_untag_ui(qw.QDialog):

    def __init__(self):
        super(find_untag_ui, self).__init__()

        font = qg.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        # self.exp_dir = ""
        # self.un = getpass.getuser()
        # self.del_list = []

        self.setObjectName("self")
        self.resize(500, 600)
        self.verticalLayout_All = qw.QVBoxLayout(self)
        self.verticalLayout_All.setObjectName("verticalLayout_2")

        self.setWindowFlags(self.windowFlags() | qc.Qt.WindowMinimizeButtonHint | qc.Qt.WindowMaximizeButtonHint)

        self.verticalLayout = qw.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_file_list = qw.QLabel(self)
        self.label_file_list.setFont(font)
        self.label_file_list.setObjectName("label_3")
        self.label_file_list.setText("Images List : ")
        self.verticalLayout.addWidget(self.label_file_list)

        self.other_word_lab = qw.QLabel(self)
        self.other_word_lab.setText("註解 : ")
        self.other_word_lab.setObjectName("other_txt_lab")
        self.verticalLayout.addWidget(self.other_word_lab)

        self.other_word = qw.QPlainTextEdit(self)
        self.other_word.setObjectName("other_word_txt")
        self.other_word.setMaximumHeight(80)
        self.other_word.setPlaceholderText("在此輸入 註解/說明 或是 合併圖片時的檔案名稱!")
        self.verticalLayout.addWidget(self.other_word)

        self.slider = qw.QSlider(self)
        self.slider.setMinimumSize(qc.QSize(0, 30))
        self.slider.setOrientation(qc.Qt.Horizontal)
        self.slider.setObjectName("horizontalSlider")
        self.slider.setMinimum(cd.Data.ICON_DROP_MINIMUM)
        self.slider.setMaximum(cd.Data.ICON_DROP_MAXIMUM)
        self.slider.setValue(cd.Data.ICON_DROP_START_SIZE)
        self.verticalLayout.addWidget(self.slider)
        self.slider.valueChanged.connect(lambda: self.file_list.slider_change_icon_size(self.slider.value()))

        self.horizontalLayout = qw.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)

        ################ btn ################

        self.button_del = qw.QPushButton(self)
        self.button_del.setMinimumSize(qc.QSize(0, 30))
        self.button_del.setFont(font)
        self.button_del.setObjectName("button_del")
        self.button_del.setText("Delete Selection")
        self.horizontalLayout.addWidget(self.button_del)
        self.button_del.clicked.connect(self.file_list.clear_button_event)

        self.button_color = qw.QPushButton(self)
        self.button_color.setMinimumSize(qc.QSize(0, 30))
        self.button_color.setFont(font)
        self.button_color.setObjectName("button_color")
        self.button_color.setText("Add Color Image")
        self.horizontalLayout.addWidget(self.button_color)
        self.button_color.clicked.connect(self.color_picker_btn)

        self.button_combine = qw.QPushButton(self)
        self.button_combine.setMinimumSize(qc.QSize(0, 30))
        self.button_combine.setFont(font)
        self.button_combine.setObjectName("button__combine")
        self.button_combine.setText("Combine Selection")
        self.horizontalLayout.addWidget(self.button_combine)
        self.button_combine.clicked.connect(self.button_combine_clicked)

        self.verticalLayout_All.addLayout(self.verticalLayout)
        self.horizontalLayout2 = qw.QHBoxLayout(self)
        self.horizontalLayout2.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.button_exp_path = qw.QPushButton(self)
        self.button_exp_path.setMinimumSize(qc.QSize(0, 40))
        self.button_exp_path.setFont(font)
        self.button_exp_path.setObjectName("button_exp_path")
        self.button_exp_path.setText("輸出資料夾")
        self.horizontalLayout2.addWidget(self.button_exp_path)
        self.button_exp_path.clicked.connect(self.exp_path_btn_clicked)

        self.button_go = qw.QPushButton(self)
        self.button_go.setMinimumSize(qc.QSize(0, 40))
        self.button_go.setFont(font)
        self.button_go.setObjectName("button_Go")
        self.button_go.setText("Create!!")
        self.horizontalLayout2.addWidget(self.button_go)

        self.button_go.clicked.connect(self.go_button_clicked)


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = find_untag_ui()
    ui.show()
    # ui.move(15, 125)

    sys.exit(app.exec_())