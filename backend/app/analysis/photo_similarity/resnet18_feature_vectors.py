"""
resnet18_feature_vectors.py
"""
from pathlib import Path

import torch
from torchvision import models
from torchvision import transforms
from torch.autograd import Variable

from django.conf import settings

from app.models import Photo


def analyze(photo: Photo):
    """
    Produce a feature vector for this Photo and serialize it out to disk

    Totally based on https://github.com/christiansafka/img2vec/
    and the accompanying article.
    """
    # Load the image using Pillow
    image = photo.get_image_data(use_pillow=True)

    if not image:
        raise ValueError(f"No image exists for {photo}")

    # Load the pretrained model, set to evaluation mode, and select the desired layer
    model = models.resnet18(pretrained=True)
    model.eval()
    layer_name = 'avgpool'
    layer = model._modules.get(layer_name)  # pylint: disable=protected-access

    # Transform the image and save it to a PyTorch Variable
    scale = transforms.Resize((224, 224))
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    to_tensor = transforms.ToTensor()
    image_tensor = Variable(normalize(to_tensor(scale(image))).unsqueeze(0))
    feature_vector = torch.zeros(512)

    # Define a function that will copy the output of a layer
    def copy_data(_module, _input, output):
        feature_vector.copy_(output.data.reshape(output.data.size(1)))

    # Attach that function to our selected layer
    hook = layer.register_forward_hook(copy_data)

    # Run the model on our transformed image
    model(image_tensor)

    # Detach our copy function from the layer
    hook.remove()

    # Save the tensor as a list
    return feature_vector.tolist()
