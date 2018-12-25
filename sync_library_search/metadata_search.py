import pickle
import os

import constant_data


class MetaDataSearch:

    def __init__(self, image_file):

        if not os.path.exists(image_file):
            raise FileNotFoundError

        if not os.path.isfile(image_file):
            raise ValueError

        self.image_file = image_file

    def get_tags(self):

        start = b'<dc:subject>\n'.strip()
        compare_start = b'<rdf:li>'.strip()
        compare_end = b'</rdf:li>'.strip()
        end = b'</dc:subject>\n'.strip()
        bags_start = b'<rdf:Bag>\n'.strip()
        bags_end = b'</rdf:Bag>\n'.strip()

        # hierarchical_start = b'<lr:hierarchicalSubject>'
        # hierarchical_end = b'</lr:hierarchicalSubject>'

        f = open(self.image_file, "rb")
        result = b""
        tags = []
        for i in f:
            data = i.strip()
            result += data

        clean_data = result.strip().replace(b"\n", b"").replace(b" ", b"")
        if start in clean_data:
            extract_data_start = clean_data.split(start)

            for j in extract_data_start:
                if end in j:
                    extract_data_end = j.split(end)
                    if bags_start in extract_data_end[0] and bags_end in extract_data_end[0]:
                        extract_data_bags_start = extract_data_end[0].split(bags_start)

                        for k in extract_data_bags_start:
                            if compare_start in k and compare_end in k:
                                extract_data_compare_start = k.split(compare_start)

                                for l in extract_data_compare_start:

                                    if compare_end in l:
                                        data_clean = l.split(bags_end)

                                        data_capture = data_clean[0].replace(compare_end, b"")
                                        try:
                                            data_decode = data_capture.decode("utf-8")
                                            tags.append(data_decode)

                                        except UnicodeDecodeError:
                                            continue

                else:
                    continue

        f.close()
        return tags


def key_words_list_read():
    if not os.path.exists(constant_data.Data.KEY_WORDS_FILE):
        print("Dead Error")
        return

    with open(constant_data.Data.KEY_WORDS_FILE, "rb") as output:
        out = pickle.load(output, encoding="utf8")

    return out


def key_words_list_bake():
    if not os.path.exists(constant_data.Data.KEY_WORDS_FILE):
        print("Dead Error")
        return

    out_dictionary = {}

    for i in os.listdir(constant_data.Data.SOURCE_PATH):
        if os.path.splitext(i)[1].lower() == ".jpg":
            print(i)

            key = os.path.splitext(i)[0]
            tags = image_tags_search(os.path.join(constant_data.Data.SOURCE_PATH, i))

            out_dictionary.setdefault(key.strip(), tags)

    with open(constant_data.Data.KEY_WORDS_FILE, "wb") as output:
        pickle.dump(out_dictionary, output, pickle.HIGHEST_PROTOCOL)



def image_tags_search(image_file):
        # image_file_full_path = generate_image_file_full_path(image_file)
        # if image_file_full_path:

        image_metadata = MetaDataSearch(image_file)
        image_tags = image_metadata.get_tags()

        if image_tags:
            return image_tags
        else:
            return list()


# def generate_image_file_full_path(file_name):
#     out_path = ""
#     full_path_01 = os.path.join(constant_data.Data.SOURCE_PATH, file_name + ".jpg")
#     full_path_02 = os.path.join(constant_data.Data.SOURCE_PATH, file_name + ".JPG")
#
#     if os.path.exists(full_path_01) and os.path.isfile(full_path_01):
#         out_path = full_path_01
#     elif os.path.exists(full_path_02) and os.path.isfile(full_path_02):
#         out_path = full_path_02
#
#     return out_path

if __name__ == '__main__':
    print("start key words baking...")
    key_words_list_bake()

