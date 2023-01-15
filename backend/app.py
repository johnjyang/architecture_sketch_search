import re, os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50

from models_for_deployment import create_image_embeddings_and_labels_df, build_annoy_tree

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
cors = CORS(app, resources={r"/api": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

# some import directories
root_dir = 'images_data/arch_100k_dataset_raw_sketches_public_only'
pickle_dir = 'embeddings_data/embeddings_sketches_Resnet50_public_nodrawings.pickle'
high_quality_dir = 'images_data/arch_100k_dataset_raw_public_only'

# initialize model
model = ResNet50(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
custom_model = Model(model.inputs, model.layers[-2].output)

# getting embeddings and embedded filenames (temporary: txt) from pickle files
image_embeddings_and_labels_df = create_image_embeddings_and_labels_df(pickle_dir, include_drawings=False)

# build annoy tree
annoy_tree = build_annoy_tree(image_embeddings_and_labels_df, 200)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/api", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def api():
    

    return jsonify(response=response)


@app.route("/admin", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def admin():

    return jsonify(response=response)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=('server.crt', 'server.key'))
    app.run(host="0.0.0.0", port=5000, debug=False)
