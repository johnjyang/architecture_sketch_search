import os
import shutil


def get_file_list(root_dir):

    file_list = []
    counter = 1
    extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".txt"]

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))
                counter += 1

    file_list = sorted(file_list)

    return file_list


# labels useful for classification
def organize_files_by_label(root_dir, destination_dir):

    file_names = get_file_list(root_dir)

    labels_list = []

    for name in file_names:

        name_parts = name.split(" ")
        if "Stairs" in name_parts:
            label = "Stairs"
        elif "Handrail" in name_parts:
            label = "Stairs"
        elif "Steel" in name_parts:
            label = "Steel"
        elif "Chair" in name_parts:
            label = "Chair"
        elif "Sofa" in name_parts:
            label = "Sofa"
        elif "Shelving" in name_parts:
            label = "Shelving"
        elif "Waterfront" in name_parts:
            label = "Waterfront"
        elif "Kitchen" in name_parts:
            label = "Kitchen"
        elif "Countertop" in name_parts:
            label = "Countertop"
        elif "Sink" in name_parts:
            label = "Sink"
        elif "Toilet" in name_parts:
            label = "Toilet"
        elif "Room" in name_parts:
            label = "Room"
        elif "Deck" in name_parts:
            label = "Deck"
        elif "Arch" in name_parts:
            if "Facade" in name_parts:
                label = "Facade"
            else:
                label = "Arch"
        elif "Cityscape" in name_parts:
            label = "Cityscape"
        elif "Balcony" in name_parts:
            label = "Balcony"
        elif "Interior" in name_parts:
            if "Windows" in name_parts:
                label = "Windows"
            elif "Closet" not in name_parts:
                if "Table" not in name_parts:
                    if "Bench" not in name_parts:
                        if "Door" not in name_parts:
                            label = "Interior Photography"
        elif "Exterior" in name_parts:
            if "Patio" not in name_parts:
                if "Fence" not in name_parts:
                    label = "Exterior Photography"
        else:
            label = name_parts[-2]

        if label not in labels_list:
            labels_list.append(label)

        destination_path = f"""./{destination_dir}/{label}"""
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        shutil.copy(name, destination_path)

    return None


def copy_dump_files(root_dir, destination_dir):

    file_names = get_file_list(root_dir)

    for name in file_names:
        destination_path = f"""./{destination_dir}/"""
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        shutil.copy(name, destination_path)


raw_data_dir = "arch_100k_dataset_raw/public_buildings_raw"
organized_data_dir = "arch_100k_dataset_raw_public_only"

copy_dump_files(raw_data_dir, organized_data_dir)
