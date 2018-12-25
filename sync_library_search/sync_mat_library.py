import os
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

font = PIL.ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20)
mat_image_path = r"T:\Digicom\RESOURSE\13_AI_Material_Library\all"
com_mat_image_path = r"D:\CanPy\sync_library_search\com_mat_image"
re_mat_image_path = r"D:\CanPy\sync_library_search\re_mat_image"
mat_lib = os.listdir(mat_image_path)

def mat_image_to2d(img):

    plan_img_name = os.path.splitext(img)[0] + "_2D" + os.path.splitext(img)[1]
    plan_img = os.path.join(mat_image_path, plan_img_name)

    if os.path.isfile(plan_img):
        return plan_img
    else:
        return

if __name__ == '__main__':

    for i in mat_lib:
        if os.path.splitext(i)[1].lower() == ".jpg" and os.path.splitext(i)[0][-1].upper() != "D":
            img1 = PIL.Image.open(os.path.join(mat_image_path, i))

            new_img = PIL.Image.new("RGB", (img1.size[0]+img1.size[0], img1.size[1]+40), "white")
            new_img.paste(img1, (0, 0))

            if mat_image_to2d(i) != None:
                img2 = PIL.Image.open(mat_image_to2d(i))
                new_img.paste(img2, (img2.size[0], 0))

            draw = PIL.ImageDraw.Draw(new_img)
            draw.text((10, img1.size[1]+10), i, font=font, fill=(0,0,0,0))

            # new_img.show()
            new_img.save(com_mat_image_path + "\\com_" + i)
            new_img.thumbnail((int(new_img.size[0])/3, int(new_img.size[1])/3))
            new_img.save(re_mat_image_path + "\\re_" + i)
            print("com_" + i)

    print("Finish!")

