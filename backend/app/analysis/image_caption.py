"""

image_caption.py -
Analysis that attempts to generate a caption for an image
Could be used to capture relationships between objects and actions present in image

links:
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
- https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/text/image_captioning.ipynb#scrollTo=6HbD8n0w7d3F

"""
import os
import json

import tensorflow as tf

from django.conf import settings
from ..models import Photo
from .captioning.model import CNN_Encoder, RNN_Decoder

MODEL = Photo
MAX_CAPTION_LENGTH = 50
CAPTION_DATA_DIR = os.path.join(settings.ANALYSIS_DIR, "captioning")
VOCAB_PATH = os.path.join(CAPTION_DATA_DIR, "vocabulary.json")

# Model training parameters (Weights depend on the parameters being set as follows)
EMBEDDING_DIM = 256
UNITS = 512

def load_model():
    with open(VOCAB_PATH, 'r', encoding="utf-8") as file:
        vocabulary = json.load(file)
    
    encoder = CNN_Encoder(EMBEDDING_DIM)
    encoder.load_weights(os.path.join(CAPTION_DATA_DIR, f"encoder_cp-0020.ckpt"))
    decoder = RNN_Decoder(EMBEDDING_DIM, UNITS, len(vocabulary))
    decoder.load_weights(os.path.join(CAPTION_DATA_DIR, f"decoder_cp-0020.ckpt"))

    # Translators
    word_to_index = tf.keras.layers.StringLookup(
        mask_token="",
        vocabulary=vocabulary
    )
    index_to_word = tf.keras.layers.StringLookup(
        mask_token="",
        vocabulary=vocabulary,
        invert=True
    )

    return encoder, decoder, word_to_index, index_to_word


def extract_incv3_features(img):
    # Preprocess image
    proc_img = tf.keras.layers.Resizing(299, 299)(img)
    proc_img = tf.keras.applications.inception_v3.preprocess_input(proc_img)
    proc_img = tf.expand_dims(proc_img, 0)

    image_model = tf.keras.applications.InceptionV3(
        include_top=False,
        weights='imagenet'
    )
    new_input = image_model.input
    hidden_layer = image_model.layers[-1].output
    image_features_extract_model = tf.keras.Model(new_input, hidden_layer)
    return image_features_extract_model(proc_img)


def make_caption(image):
    encoder, decoder, word_to_index, index_to_word = load_model()
    hidden = decoder.reset_state(batch_size=1)
    
    incv3_features = extract_incv3_features(image)
    new_shape = (incv3_features.shape[0], -1, incv3_features.shape[3])
    features = encoder(tf.reshape(incv3_features, new_shape))
    dec_input = tf.expand_dims([word_to_index("<start>")], 0)

    result = []
    # Generate MAX_CAPTION_LENGTH words from image based on last word
    for i in range(MAX_CAPTION_LENGTH):
        predictions, hidden, _ = decoder(
            dec_input, features, hidden
        )

        # Generate next word
        predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
        predicted_word = tf.compat.as_text(index_to_word(predicted_id).numpy())

        if predicted_word == "<end>":
            return result

        result.append(predicted_word)
        dec_input = tf.expand_dims([predicted_id], 0)

    return result


def analyze(photo: Photo, src_dir=settings.LOCAL_PHOTOS_LOCATION):
    input_image = photo.get_image_data(src_dir=src_dir)
    if input_image is None:
        return ''
    caption_words = make_caption(input_image)
    return ' '.join(caption_words)
