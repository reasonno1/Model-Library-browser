

import os
import shutil
import time
import pickle

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import multiprocessing as mp
import metadata_search as ms



AI_Model_Library = r"T:\Digicom\RESOURSE\12_AI_Model_Library"
AI_Material_Library = r"T:\Digicom\RESOURSE\13_AI_Material_Library\all"

src_path = r"T:\Digicom\家具檢索\AI_Model_Library\src_image"
resize_path = r"T:\Digicom\家具檢索\AI_Model_Library\resize_image"
KEY_WORDS_FILE = r"T:\Digicom\家具檢索\AI_Model_Library\lib_search_data\tag.txt"
ratio = 128 / 720

font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20)
com_mat_image_path = r"T:\Digicom\家具檢索\AI_Model_Library\com_mat_image"
re_mat_image_path = r"T:\Digicom\家具檢索\AI_Model_Library\re_mat_image"



def key_words_list_bake(i):

    if os.path.splitext(i)[1].lower() == ".jpg":
        print(i)
        out_dict = {}
        key = os.path.splitext(i)[0]
        tags = ms.image_tags_search(os.path.join(src_path, i))
        out_dict.setdefault(key.strip(), tags)

        return out_dict

def sync_lib_image(file):
    resize_count = 0
    copy_count = 0
    update_count = 0

    temp = file.split(".")
    if temp[-1].lower() == "jpg":
        need_update = False
        src_time = os.path.getmtime(AI_Model_Library + "\\" + file)
        ###############################################################################
        if not os.path.isfile(resize_path + "\\" + "re_" + file):

            im = Image.open(AI_Model_Library + "\\" + file)
            new_im = im.resize((128, int(im.size[1] * ratio)), Image.BILINEAR)
            new_im.save(resize_path + "\\re_" + file, quality=70)
            resize_count += 1
            print("re_" + file)
        else:
            resize_time = os.path.getmtime(resize_path + "\\re_" + file)
            if resize_time <= src_time:
                need_update = True
                im = Image.open(AI_Model_Library + "\\" + file)
                new_im = im.resize((128, int(im.size[1] * ratio)), Image.BILINEAR)
                new_im.save(resize_path + "\\re_" + file, quality=70)
                update_count += 1
                print("re_" + file)
            else:
                print("re_" + file + ' file exist!')
        ###############################################################################
        if not os.path.isfile(src_path + '\\' + file):
            shutil.copy(AI_Model_Library + '\\' + file, src_path + '\\' + file)
            copy_count += 1
            print(file)
        else:
            if need_update:
                shutil.copy(AI_Model_Library + '\\' + file, src_path + '\\' + file)
                print(file)
            else:
                print(file + ' file exist!')

    return resize_count, copy_count, update_count

def mat_image_to2d(img):

    plan_img_name = os.path.splitext(img)[0] + "_2D" + os.path.splitext(img)[1]
    plan_img = os.path.join(AI_Material_Library, plan_img_name)

    if os.path.isfile(plan_img):
        return plan_img
    else:
        white_img = Image.new("RGB", (img.size[0], img.size[1]), "white")
        return white_img

def sync_mat_image(i):

    if os.path.splitext(i)[1].lower() == ".jpg" and os.path.splitext(i)[0][-1].upper() != "D":
        img1 = Image.open(os.path.join(AI_Material_Library, i))

        new_img = Image.new("RGB", (img1.size[0] + img1.size[0], img1.size[1] + 40), "white")
        new_img.paste(img1, (0, 0))

        if mat_image_to2d(i) != None:
            img2 = Image.open(mat_image_to2d(i))
            new_img.paste(img2, (img2.size[0], 0))

        draw = ImageDraw.Draw(new_img)
        draw.text((10, img1.size[1] + 10), i, font=font, fill=(0, 0, 0, 0))

        new_img.save(com_mat_image_path + "\\" + i)
        new_img.thumbnail((int(new_img.size[0]) / 3, int(new_img.size[1]) / 3))
        new_img.save(re_mat_image_path + "\\re_" + i)
        print("com_" + i)


def Main():

    tag_dict = {}
    sync_log = r"T:\Digicom\家具檢索\AI_Model_Library\lib_search_data\sync_log.txt"
    now = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    work_state = [0, 0, 0]
    model_lib = os.listdir(AI_Model_Library)
    mat_lib = os.listdir(AI_Material_Library)

    pool = mp.Pool(8)

    res = pool.map(sync_lib_image, model_lib)
    res_bake = pool.map(key_words_list_bake, model_lib)
    # pool.map(sync_mat_image, mat_lib)

    pool.close()
    pool.join()
    temp = 0
    for i in range(len(res)):
        work_state[0] += res[i][0]
        work_state[1] += res[i][1]
        work_state[2] += res[i][2]

    print('Resize Count : ' + str(work_state[0]))
    print('Copy Count : ' + str(work_state[1]))
    print('Update Count : ' + str(work_state[2]))


    for t in range(len(res_bake)):
        if res_bake[t] is not None:
            tag_dict.update(res_bake[t])
            temp += 1


    print(tag_dict)
    print(temp)
    print(len(tag_dict))


    with open(KEY_WORDS_FILE, "wb") as tag_file:
        pickle.dump(tag_dict, tag_file, pickle.HIGHEST_PROTOCOL)

    with open(sync_log, 'w') as log_file:
        log_file.write(now + "\n")
        log_file.write("Resize Count : " + str(work_state[0]) + "\n")
        log_file.write("Copy Count : " + str(work_state[1]) + "\n")
        log_file.write("Update Count : " + str(work_state[2]) + "\n")





if __name__ == '__main__':
    Main()


