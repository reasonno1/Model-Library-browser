import getpass

class Data:

    URL_START = r"file:///"

    KEY_WORDS_FILE = r"T:\Digicom\家具檢索\AI_Model_Library\lib_search_data\tag.txt"

    # SOURCE_PATH = r"D:\Working_File\test\model"

    SOURCE_PATH = r"T:\Digicom\家具檢索\AI_Model_Library\src_image"
    ICON_PATH = r"T:\Digicom\家具檢索\AI_Model_Library\resize_image"

    COM_MAT_PATH = r"T:\Digicom\家具檢索\AI_Model_Library\com_mat_image"
    ICON_MAT_PATH = r"T:\Digicom\家具檢索\AI_Model_Library\re_mat_image"

    ICON_IMAGE_SIZE_START = 128
    ICON_DROP_START_SIZE = 100
    ICON_DROP_MINIMUM = 100
    ICON_DROP_MAXIMUM = 300

    SPLASH_SCREEN = r"T:\Digicom\家具檢索\AI_Model_Library\lib_search_data\loading_splash_screen.png"
    NONE_EXIST_ICON = r"T:\Digicom\家具檢索\AI_Model_Library\lib_search_data\none exist_icon.png"

    AI_MODEL_LIB = r"T:\Digicom\RESOURSE\12_AI_Model_Library"
    AI_MATERIAL_LIB = r"T:\Digicom\RESOURSE\13_AI_Material_Library\all"

    CON_MSFILE = r"C:\temp\Con_Inherit_temp.ms"
    UserLocalTemp_Path = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Temp\\"

    MATERIAL_LIST = ["", "布料", "毛料", "玻璃/鏡子", "皮革", "金屬", "石材", "漆面", "塑膠/編織", "木料"]

    MATERIAL_COMP = {
        # "None": "",
        # "背景": "bac",
        # "布料": "clo",
        # "毛料": "fur",
        # "玻璃/鏡子": "gla",
        # "照明": "ill",
        # "皮革": "lea",
        # "金屬": "met",
        # "石材": "ore",
        # "漆面": "pai",
        # "塑膠": "pla",
        # "木料": "woo",
        "": "None",
        "bac": "背景",
        "clo": "布料",
        "fur": "毛料",
        "gls": "玻璃/鏡子",
        "gla": "玻璃/鏡子",
        "ill": "照明",
        "lea": "皮革",
        "met": "金屬",
        "ore": "石材",
        "pai": "漆面",
        "pla": "塑膠/編織",
        "woo": "木料",
    }



    def confile_content(self, path):

        content = """
        tempCon = %s
        con = containers.CreateInheritedContainer tempCon
        con.pos = [0,0,0]
        select con
        """ % (path)

        return content