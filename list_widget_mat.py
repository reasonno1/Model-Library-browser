import os
import multiprocessing as mp

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import metadata_search
import list_widget_item
import constant_data


class NameList_Mat(qw.QListWidget):


    icon_trigger = qc.pyqtSignal(list)

    def __init__(self, dialog):
        super().__init__(dialog)

        self.__output = ""
        self.selected = ""

        self.file_list = []

        self.name_len = 0
        self.tag_len = 0

        self.setIconSize(qc.QSize(266, 146))

        self.icon_trigger.connect(self.set_icon)


    def set_icon(self, li):

        for i in li:
            i[0].setIcon(i[1])

        print("UPDATE MAT IMAGES")

    @staticmethod
    def generate_image_file_full_path(file_name):
        full_path_01 = os.path.join(constant_data.Data.COM_MAT_PATH, file_name + ".jpg")
        full_path_02 = os.path.join(constant_data.Data.COM_MAT_PATH, file_name + ".JPG")

        if os.path.exists(full_path_01) and os.path.isfile(full_path_01):
            return full_path_01
        elif os.path.exists(full_path_02) and os.path.isfile(full_path_02):
            return full_path_02
        else:
            return None


    def mouse_drag_action(self, path, item_name):

        data = qc.QMimeData()
        data.setUrls([qc.QUrl(constant_data.Data.URL_START + path)])

        drag = qg.QDrag(self)
        drag.setMimeData(data)

        img = qg.QPixmap(os.path.join(constant_data.Data.ICON_MAT_PATH, "re_" + item_name + ".jpg"))
        drag.setDragCursor(img, qc.Qt.CopyAction)
        drag.exec_(qc.Qt.CopyAction)


    def search_folder_mat(self):

        img_list = []

        for i in os.listdir(constant_data.Data.COM_MAT_PATH):
            if "jpg" not in os.path.splitext(i)[1].lower():
                continue

            image_name = os.path.splitext(i)[0]
            full_path = os.path.join(constant_data.Data.ICON_MAT_PATH, "re_" + image_name + ".jpg")
            img_list.append(image_name)

            if not os.path.exists(full_path):
                print("icon file does not exist: {}".format(full_path))

            item = list_widget_item.NameListWidgetItem(image_name, self, image_name)
            self.addItem(item)
            self.file_list.append(item)

        # print(img_list)


    def mouseDoubleClickEvent(self, *args, **kwargs):
        if len(self.selectedItems()) == 1:
            item_path = self.generate_image_file_full_path(self.selectedItems()[0].text())

            if item_path:
                os.startfile(item_path)
            else:
                qw.QMessageBox.information(qw.QMessageBox(), "Information", "The image file dose not found!")

    def mouseMoveEvent(self, event):
        if event.buttons() == qc.Qt.LeftButton:
            if len(self.selectedItems()) == 0:
                event.ignore()
                return

            image_full_path = self.generate_image_file_full_path(self.selectedItems()[0].text())
            if not image_full_path:
                return

            self.mouse_drag_action(image_full_path, self.selectedItems()[0].text())


    def text_filtering_mat(self, tag):

        mat_dict = constant_data.Data.MATERIAL_COMP

        for i in range(0, len(self.file_list)):
            self.item(i).setHidden(False)
            compare_text = self.item(i).text().strip().lower()[:3]
            if not mat_dict[tag] in compare_text:
                self.item(i).setHidden(True)

