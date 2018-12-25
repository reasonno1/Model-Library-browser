
import os
import shutil
import time
import pickle

import multiprocessing as mp
import metadata_search as ms

AI_Model_Library = r"T:\Digicom\RESOURSE\12_AI_Model_Library"
AI_Material_Library = r"T:\Digicom\RESOURSE\13_AI_Material_Library\all"

src_path = r"V:\資料庫\3D圖鑑-資料庫\家具檢索\AI_Model_Library\src_image"
resize_path = r"V:\資料庫\3D圖鑑-資料庫\家具檢索\AI_Model_Library\resize_image"
untag_path = r"D:\CanPy\sync_library_search\temp"

name_tags = ['can', 'canchen', 'rick', 'rickhsu', 'rozy', 'rozychiu', 'grace', 'gracetseng',
             'ashe', 'ashetoung', 'cl', 'cohloelin', 'leven', 'levenhsu', 'yuzang', 'yuzhenchen',
             'chinminshie']

def key_words_list_bake(i):

    if os.path.splitext(i)[1].lower() == ".jpg":
        out_dict = {}
        key = os.path.splitext(i)[0]
        tags = ms.image_tags_search(os.path.join(src_path, i))

        have_name = False
        for i in tags:
            if i.lower() in name_tags:
                have_name = True
                break

        if not have_name:
            out_dict.setdefault(key.strip(), tags)
            print(out_dict)
            return out_dict

def Main():

    model_lib = os.listdir(AI_Model_Library)

    pool = mp.Pool(8)
    res_bake = pool.map(key_words_list_bake, model_lib)
    pool.close()
    pool.join()



    # for t in range(len(res_bake)):
    #     if res_bake[t] is not None:
    #         print(res_bake[t])




if __name__ == '__main__':
    Main()


