
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


import os
import sys
import time
import getpass
import shutil
import constant_data as cd
from PIL import Image as im
from PIL import ImageDraw as idraw
from PIL import ImageFont as ifont

class Model_Modify_Gui(qw.QDialog):

    def __init__(self):
        super(Model_Modify_Gui, self).__init__()

        font = qg.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.exp_dir = ""
        self.un = getpass.getuser()
        self.del_list = []

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

        self.file_list = ModList(self)
        self.file_list.setObjectName("listWidget")
        self.file_list.setFont(font)
        self.verticalLayout.addWidget(self.file_list)

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

    ############## btn color_picker ##############

    def button_combine_clicked(self):
        self.file_list.combining_button_event(self.other_word.toPlainText(),
                                              self.del_list)
        self.other_word.setPlainText("")

    ############## btn color_picker ##############

    def color_picker_btn(self):

        color = qw.QColorDialog.getColor()
        if not color.isValid():
            return
        img = im.new("RGB", (300, 300), color.name())
        # img.save("C:\\temp\\" + color.name() + ".jpg")
        img.save("C:\\Users\\" + self.un + "\\AppData\\Local\\Temp\\" + color.name() + ".jpg")


        url = "C:\\Users\\" + self.un + "\\AppData\\Local\\Temp\\" + color.name() + ".jpg"
        self.file_list.contain.add(url)
        self.del_list.append(url)
        # print(url)

        icon = qg.QIcon(url)
        item = qw.QListWidgetItem(os.path.basename(url), self.file_list)
        item.setIcon(icon)
        self.file_list.addItem(item)


    ############## btn exp_path_btn ##############

    def exp_path_btn_clicked(self):

        self.exp_dir = qw.QFileDialog.getExistingDirectory(self, "選取資料夾", "C:\\Users\\" + self.un + "\\Desktop")

        print(self.exp_dir)

    ############## btn Create ##############

    def go_button_clicked(self):

        if self.exp_dir:
            if len(self.file_list.contain) > 0:

                ##### Create 註解.txt #####
                if self.other_word.toPlainText().strip():
                    now = (time.strftime("%Y%m%d%H%M%S", time.localtime()))
                    exp_txt = self.exp_dir + "\\" + self.un + "_註解_" + now + ".txt"
                    text = self.other_word.toPlainText()
                    with open(exp_txt, "w") as f:
                        f.write(text)

                ##### copy all selection to exp_patn #####
                for i in self.file_list.contain:
                    shutil.copy(i, self.exp_dir)

                ##### delete file in del_list #####
                if self.del_list:
                    for i in self.del_list:
                        os.remove(i)
                        self.del_list.remove(i)

                qw.QMessageBox.information(self, "warning", "Done!")
                self.close()
                os.startfile(self.exp_dir)

            else:
                qw.QMessageBox.information(self, "warning", "請先選取需要打包的圖片!")
        else:
            qw.QMessageBox.information(self, "warning", "請先選取輸出資料夾!")

    ############ UI CloseEvent ############
    def closeEvent(self, event):
        print("close!")
        if self.del_list:
            for i in self.del_list:
                try:
                    os.remove(i)
                except:
                    print("delete error!")

#####################################################################################################
class ModList(qw.QListWidget):

    def __init__(self, dialog):

        super(ModList, self).__init__(dialog)

        self.setAcceptDrops(True)
        self.setDragDropMode(qw.QAbstractItemView.DropOnly)
        self.setDefaultDropAction(qc.Qt.CopyAction)
        self.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)
        self.setIconSize(qc.QSize(cd.Data.ICON_DROP_START_SIZE, cd.Data.ICON_DROP_START_SIZE))
        self.contain = set()

    def slider_change_icon_size(self, size):

        self.setIconSize(qc.QSize(size, size))

    ############## btn combining selection ##############
    def combining_button_event(self, comb_filename, del_list):

        #### get combining image name ####
        if comb_filename.strip():
            comb_file = cd.Data.UserLocalTemp_Path + comb_filename.strip() + ".jpg"
            if os.path.isfile(comb_file):
                qw.QMessageBox.information(self, "warning", "此檔案名稱已存在!")
                return
        else:
            qw.QMessageBox.information(self, "warning", "請在註解處輸入合併圖片檔名(或註解)!")
            return

        if self.selectedItems():
            temp_len = 0
            if os.path.isfile(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg"):
                try:
                    os.remove(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg")
                except:
                    pass
            #### get combining image ####
            for i in self.selectedItems():

                if i.text()[-3:].lower() == "jpg" or i.text()[-3:].lower() == "png":

                    for j in self.contain:
                        if i.text() in j:
                            src_img = im.open(j)
                            ratio = 200 / src_img.size[1]
                            re_width = int(src_img.size[0]*ratio)
                            temp_len += int(src_img.size[0] * ratio)
                            re_img = src_img.resize((re_width, 200), im.BILINEAR)

                            if not os.path.isfile(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg"):
                                new_img = im.new("RGB", (temp_len, 200), "white")
                                new_img.paste(re_img, (0, 0))
                                new_img.save(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg", quality=80)

                            else:
                                add_img = im.open(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg")
                                new_img = im.new("RGB", (temp_len, 200), "white")
                                new_img.paste(add_img, (0, 0))
                                new_img.paste(re_img, (temp_len - re_width, 0))
                                new_img.save(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg", quality=80)

                shutil.copy(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg", comb_file)

            #### update file list contain ####
            for i in self.selectedItems():

                self.takeItem(self.row(i))
                temp_set = set()

                for j in self.contain:

                    if i.text() in j:
                        temp_set.add(j)

                self.contain.difference_update(temp_set)

            self.contain.add(comb_file)
            comb_icon = qg.QIcon(comb_file)
            item = qw.QListWidgetItem(os.path.basename(comb_file), self)
            item.setIcon(comb_icon)
            self.addItem(item)
            del_list.append(comb_file)
            del_list.append(cd.Data.UserLocalTemp_Path + "temp_combining_image.jpg")

        else:
            return

    ############## btn delete selection ##############
    def clear_button_event(self):

        if self.selectedItems():

            for i in self.selectedItems():

                self.takeItem(self.row(i))
                temp_set = set()

                for j in self.contain:

                    if i.text() in j:
                        temp_set.add(j)

                self.contain.difference_update(temp_set)

        else:
            return

    def dragEnterEvent(self, event):

        self.clear()
        event.setDropAction(qc.Qt.CopyAction)
        event.accept()

        for file in event.mimeData().urls():
            url = file.toLocalFile()
            self.contain.add(url)

        for i in self.contain:

            if os.path.isfile(i):
                icon = qg.QIcon(i)

            item = qw.QListWidgetItem(os.path.basename(i), self)
            item.setIcon(icon)
            self.addItem(item)


    def dragMoveEvent(self, event):

        event.setDropAction(qc.Qt.CopyAction)
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(qc.Qt.IgnoreAction)
        event.ignore()





if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = Model_Modify_Gui()
    ui.show()
    # ui.move(15, 125)

    sys.exit(app.exec_())