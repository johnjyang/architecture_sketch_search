import os
import time
import pickle
import numpy as np
import pandas as pd
from numpy.linalg import norm
from tqdm import tqdm
from keras.models import load_model, Model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import keras.utils as image
from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tensorflow.keras.applications.resnet50 import ResNet50


# find Images in the Root Directiry and making list of those Images
def get_file_list(root_dir):

    file_list = []
    counter = 1
    extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.txt']

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))
                counter += 1

    file_list = sorted(file_list)

    return file_list


# define Function to create image embeddings
def create_single_image_embeddings(image_path, initialized_model):

    # preprocessing input Image
    input_shape = (224, 224, 3)
    img = image.load_img(image_path, target_size=(input_shape[0], input_shape[1]))  # reshape input image size into target size
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)

    # getting features from the Image
    features_array = initialized_model.predict(preprocessed_img)
    flattened_features_array = features_array.flatten()
    normalized_features_array = flattened_features_array / norm(flattened_features_array)

    return normalized_features_array


# creating embeddings for each image and saving them in a txt (temporary: future in db)
def create_images_embeddings_and_store_to_txt(list_of_image_paths, initialized_model, txt_storage_dir):

    total_images_count = len(list_of_image_paths)

    for i in range(total_images_count):

        # drop file path and type (.png)
        filename = list_of_image_paths[i].split("/")[-1]
        filename = filename[:-4]

        single_image_embedding = create_single_image_embeddings(list_of_image_paths[i], initialized_model)
        np.savetxt(f'''{txt_storage_dir}/{filename}.txt''', single_image_embedding)

        print(f'''{i} of {total_images_count}. {list_of_image_paths[i]}''')


def extract_embeddings_and_file_names_from_txt(txt_storage_dir, pickle_file_dir, include_drawings=False):

    embedding_filenames_list_from_txt = get_file_list(txt_storage_dir)  # length = 18918
    embeddings_list = []

    for f_index in range(len(embedding_filenames_list_from_txt)):

        if not include_drawings:
            if 'Drawings' not in embedding_filenames_list_from_txt[f_index]:
                embeddings_list.append(np.loadtxt(embedding_filenames_list_from_txt[f_index]))
        elif include_drawings:
            embeddings_list.append(np.loadtxt(embedding_filenames_list_from_txt[f_index]))

        print(f_index)

    print(len(embeddings_list))
    pickle.dump(embeddings_list, open(pickle_file_dir, 'wb'))


def create_image_embeddings_and_labels_df(embeddings_pickle_file_path, include_drawings=False):

    embeddings_list = pickle.load(open(embeddings_pickle_file_path, 'rb'))
    initial_file_list = get_file_list('arch_100k_dataset_raw_public_only')

    file_names_list = []
    for f_index in range(len(initial_file_list)):
        if not include_drawings:
            if 'Drawings' not in initial_file_list[f_index]:
                file_names_list.append(initial_file_list[f_index])
                continue
        elif include_drawings:
            file_names_list.append(initial_file_list[f_index])

    image_embeddings_and_labels_df = pd.DataFrame({'img_id': file_names_list, 'img_embs': embeddings_list})

    return image_embeddings_and_labels_df


def get_similar_images_df_from_path(image_path, initialized_model, degree_of_nn):

    start = time.time()
    embedded_image_vector = create_single_image_embeddings(image_path, initialized_model)

    similar_img_ids = t.get_nns_by_vector(embedded_image_vector, degree_of_nn)
    end = time.time()
    print(f'{(end - start) * 1000} ms')

    return image_embeddings_and_labels_df.iloc[similar_img_ids[1:]]


def get_similar_images_df_from_index(image_index, degree_of_nn):

    start = time.time()

    similar_img_ids = t.get_nns_by_item(image_index, degree_of_nn)
    end = time.time()
    print(f'{(end - start) * 1000} ms')

    return image_embeddings_and_labels_df.iloc[similar_img_ids[1:]]


def search_similar_images_by_path(query_image_path):

    def _get_high_quality_images_paths_from_similar_images_df(image_df):

        image_list = image_df['img_id'].to_list()

        full_image_paths = []

        for i in range(len(image_list)):

            image_name_parts = image_list[i].split('.')  # remove .png tail
            image_name = image_name_parts[0] + '.jpg'

            image_name_parts = image_name.split("/")
            image_name = image_name_parts[1]
            path = image_name

            if path not in full_image_paths:
                full_image_paths.append(path)

        return full_image_paths

    similar_images_df = get_similar_images_df_from_path(query_image_path, custom_model, 30)
    print(similar_images_df)
    similar_images_paths = _get_high_quality_images_paths_from_similar_images_df(similar_images_df)

    """
    # next_image_index = list(initial_similar_images_df.index.values)
    for i in range(len(similar_images_paths)):
        path = os.path.join('arch_100k_dataset_raw_public_only', similar_images_paths[i])
        next_similar_images_df = get_similar_images_df_from_path(path, custom_model, 5)
        similar_images_df = similar_images_df.append(next_similar_images_df)


        deep_image_index = list(next_similar_images_df.index.values)
        if len(deep_image_index) > 0:
            deep_similar_images_df = get_similar_images_df_from_index(deep_image_index[0], 3)
            total_similar_images_df = total_similar_images_df.append(deep_similar_images_df)
    """

    similar_images_paths = _get_high_quality_images_paths_from_similar_images_df(similar_images_df)

    return similar_images_paths


def plot_images(query_image_path, images_paths):

    # plot.
    plt.figure(figsize = (16, 9))
    plt.subplot(5, 6, 1)
    image = mpimg.imread(query_image_path)
    plt.imshow(image)
    plt.title('Sketch')
    plt.axis('off')

    if len(images_paths) > 29:
        plot_count = 29
    else:
        plot_count = len(images_paths)
    for i in range(plot_count):
        path = os.path.join('arch_100k_dataset_raw_public_only', images_paths[i])
        print(path)
        image = mpimg.imread(path)
        plt.subplot(5, 6, i + 2)
        plt.imshow(image)
        plt.title('Similar Image')
        plt.axis('off')

    plt.show()


# initialize model
# model = load_model("saved_models/keras_Resnet50_30_old")
# custom_model = Model(model.inputs, model.layers[-3].output)

model = ResNet50(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
custom_model = Model(model.inputs, model.layers[-2].output)

# create list of image files in dataset (organized by labels)
root_dir = 'arch_100k_dataset_raw_sketches_public_only'
sketches_images_filenames_list = get_file_list(root_dir)

# create image embeddings and store to txt (temporary)
embeddings_storage_dir = 'txt_embeddings_Resnet50_public'
if not os.path.exists(embeddings_storage_dir):
    os.mkdir(embeddings_storage_dir)
# this should be commented out most of the time.
# create_images_embeddings_and_store_to_txt(sketches_images_filenames_list, custom_model, embeddings_storage_dir)

# caking pickle file of filenames and features of each files for future references
pickle_dir = './embeddings_data/embeddings_sketches_Resnet50_public_nodrawings.pickle'
# extract_embeddings_and_file_names_from_txt(embeddings_storage_dir, pickle_dir, include_drawings=False)

# getting embeddings and embedded filenames (temporary: txt) from pickle files
image_embeddings_and_labels_df = create_image_embeddings_and_labels_df(pickle_dir, include_drawings=False)
print(image_embeddings_and_labels_df)

# create annoy tree
vector_length = len(image_embeddings_and_labels_df['img_embs'][0])
t = AnnoyIndex(vector_length, metric='euclidean')

for i in tqdm(range(len(image_embeddings_and_labels_df['img_embs']))):
    t.add_item(i, image_embeddings_and_labels_df['img_embs'][i])

_ = t.build(200)  # number of trees to build

# find similar images and plot
# for s in get_file_list('test_images'):
# for image_name in ['chameleon.png', 'light_show.jpg', 'void.jpg', 'truss.png']:
for image_name in ['orthogonal_sketch.jpg', 'cooper.jpg', 'building_interior.jpg', 'not_circle.jpg', 'overlaying_sq.png']:
    path = 'test_images/' + image_name
    plot_images(path, search_similar_images_by_path(path))
