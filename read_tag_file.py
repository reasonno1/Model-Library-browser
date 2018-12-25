def mot_tag(tag_file):
    metaData = {}

    with open(tag_file, 'r') as f:
        for line in f:
            temp_ary = line.strip("\n").replace(" ", "").split("-")
            tag_ary = temp_ary[1].split(",")
            for tag in tag_ary:
                # if ('mot'or'MOT') in tag:
                if ('MOT') in tag:
                    # metaData[temp_ary[0]] = tag_ary
                    print(tag)

    return metaData


def read_tag_file(tag_file):
    meta_data = {}

    with open(tag_file, 'r') as f:
        for line in f:
            temp_ary = line.strip("\n").replace(" ", "").split("-")

            key = (temp_ary[0].split(".")[0]).strip()
            tags = [i.strip() for i in temp_ary[1].split(",")]

            meta_data[key] = tags

            # metaData[temp_ary[0]] = temp_ary[1].split(",")

    return meta_data


def Main():
    tag_f = r"D:\CanPy\image_resize\tag_test.txt"
    metadata = mot_tag(tag_f)
    print(metadata)

if __name__ == '__main__':
    # Main()

    a = read_tag_file("tag.txt")
    print(a)
    print(a["FUT_ZA_017"])
