import os


def write_list_to_txt(list_to_write, txt_name):

    with open(txt_name + ".txt", "w") as txt:
        for item in list_to_write:
            txt.write("%s\n" % item)

    print(f"""Wrote {len(list_to_write)} items to '{txt_name}.txt'""")

    return None


def get_file_list(root_dir):

    file_list = []
    extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))

    file_list = sorted(file_list)

    return file_list


# all key words in labels
def get_labels(paths_list):

    labels_list = ["Living", "Dining", "Interior", "Exterior"]

    for path in paths_list:
        name = path.split("/")[-1]

        name_parts = name.split(" ")
        last_label = name_parts[-2]

        if last_label not in labels_list:
            labels_list.append(last_label)

    labels_list.sort()

    return labels_list


def get_architect_names(paths_list, labels_list):

    architects_list = []

    for path in paths_list:
        name = path.split("/")[-1]

        name_parts = name.split(" ")[:-1]

        for i in range(len(name_parts)):
            if name_parts[-1] in labels_list:
                name_parts.pop()

        architect_name = " ".join(name_parts)
        if architect_name not in architects_list:
            architects_list.append(architect_name)

    architects_list.sort()

    return architects_list


files = get_file_list("images_data/arch_100k_dataset_organized")
labels = get_labels(files)

print(labels)
print(len(labels))

architects = get_architect_names(files, labels)
print(architects)
print(len(architects))

# write_list_to_txt(labels, "labels")
# write_list_to_txt(architects, 'architects')
