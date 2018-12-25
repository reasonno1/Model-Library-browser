import os
import multiprocessing as mp

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import metadata_search
import list_widget_item
import constant_data


class NameList(qw.QListWidget):


    icon_trigger = qc.pyqtSignal(list)

    def __init__(self, dialog):
        super().__init__(dialog)

        self.__output = ""
        self.selected = ""

        self.file_list = []
        self.list_type = ""
        self.list_type = ""

        self.setIconSize(qc.QSize(constant_data.Data.ICON_IMAGE_SIZE_START,
                                  constant_data.Data.ICON_IMAGE_SIZE_START))
        self.setIconSize(qc.QSize(266, 146))

        self.icon_trigger.connect(self.set_icon)


    def set_icon(self, li):

        for i in li:
            i[0].setIcon(i[1])

        print("UPDATE IMAGES")

    # @staticmethod
    def isEnglish(self, str):
        try:
            str.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    def generate_image_file_full_path(self, file_name):

        root = self.generate_root_by_type()

        full_path_01 = os.path.join(root[0], file_name + ".jpg")
        full_path_02 = os.path.join(root[0], file_name + ".JPG")

        if os.path.exists(full_path_01) and os.path.isfile(full_path_01):
            return full_path_01
        elif os.path.exists(full_path_02) and os.path.isfile(full_path_02):
            return full_path_02
        else:
            return None

    def generate_root_by_type(self):

        if self.list_type == "model":
            return constant_data.Data.SOURCE_PATH, constant_data.Data.ICON_PATH
        elif self.list_type == "material":
            return constant_data.Data.COM_MAT_PATH, constant_data.Data.ICON_MAT_PATH


    def search_folder(self):

        img_list = []
        root = self.generate_root_by_type()
        mat_dict = constant_data.Data.MATERIAL_COMP

        if self.list_type == "model":
            key_words_dictionary = metadata_search.key_words_list_read()
            tag_set = set()
            for i in key_words_dictionary.values():
                for j in i:
                    if j and (not self.isEnglish(j) or "_" in j) and not "無" in j:
                        tag_set.add(j)

        for i in os.listdir(root[0]):
            if "jpg" not in os.path.splitext(i)[1].lower():
                continue

            image_name = os.path.splitext(i)[0]
            full_path = os.path.join(root[1], "re_" + image_name + ".jpg")
            img_list.append(image_name)

            if not os.path.exists(full_path):
                print("icon file does not exist: {}".format(full_path))

            if self.list_type == "model":
                key_words = key_words_dictionary.get(image_name, [])
            else:
                # key_words = image_name
                material_tags_list = [mat_dict[image_name[:3]]]
                key_words = material_tags_list
                # print(key_words)

            item = list_widget_item.NameListWidgetItem(image_name, self, key_words)
            self.addItem(item)
            self.file_list.append(item)

        if self.list_type == "model":
            # for i in tag_set:
            #     print(i)
            return sorted(tag_set)


    def mouse_drag_action(self, path, item_name):

        root = self.generate_root_by_type()

        data = qc.QMimeData()
        data.setUrls([qc.QUrl(constant_data.Data.URL_START + path)])

        drag = qg.QDrag(self)
        drag.setMimeData(data)

        img = qg.QPixmap(os.path.join(root[1], "re_" + item_name + ".jpg"))
        drag.setDragCursor(img, qc.Qt.CopyAction)
        drag.exec_(qc.Qt.CopyAction)


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

        elif event.buttons() == qc.Qt.RightButton and self.list_type == "model":

            con_name = self.currentItem().text() + r"\CON_" + self.currentItem().text() + ".maxc"
            con_full_path = r"T:\Digicom\RESOURSE\12_AI_Model_Library" + "\\" + con_name
            if os.path.isfile(con_full_path):

                content = """
                cName = "CON_%s"
                check = getnodebyname cName
                if check==undefined then(
                    tempCon = @"%s"
                    con = containers.CreateInheritedContainer tempCon
                    con.pos = [0,0,0]
                    select con
                    max zoomext sel
                    )
                else (
                    print "con exist!"
                    select check
                    max zoomext sel
                    )""" % (self.currentItem().text(), con_full_path)

                with open(constant_data.Data.CON_MSFILE, 'w') as ms:
                    ms.write(content + '\n')
                try:
                    self.mouse_drag_action(constant_data.Data.CON_MSFILE, self.selectedItems()[0].text())
                except:
                    print("error!")

            else:
                qw.QMessageBox.information(self, "warning", "Container doesn't exist!")
                return


    def text_filtering(self, tags):

        input_tags = str(tags).lower()
        filter_tags = input_tags.replace("_", "")

        for j in range(0, len(self.file_list)):
            self.item(j).setHidden(False)

            if filter_tags:
                tags_input_list = filter_tags.split(" ")
                for l in tags_input_list:
                    if l:
                        if self.list_type == "model":
                            compare_text = self.item(j).text().strip().lower().replace("_", "")
                        else:
                            compare_text = self.item(j).text().strip().lower().replace("_", "")[3:]
                        have_tags = False

                        if l in compare_text:
                            break

                        if self.item(j).keywords:
                            for k in self.item(j).keywords:
                                if k:
                                    compare_tags = k.strip().lower().replace("_", "")
                                    if l in compare_tags:
                                        have_tags = True
                                        break
                                else:
                                    continue

                        if not have_tags:
                            self.item(j).setHidden(True)
                            break


    def text_filtering_mat(self, tag):

        mat_dict = constant_data.Data.MATERIAL_COMP

        for i in range(0, len(self.file_list)):
            self.item(i).setHidden(False)
            compare_text = self.item(i).text().strip().lower()[:3]
            if not mat_dict[tag] in compare_text:
                self.item(i).setHidden(True)


