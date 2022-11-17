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

    # Look for an existing, serialized feature vector
    dir_path = Path(settings.ANALYSIS_PICKLE_PATH,
                    'resnet18_features',
                    str(photo.map_square.number))
    dir_path.mkdir(parents=True, exist_ok=True)
    out_path = Path(dir_path, f'{photo.number}.pt')

    if out_path.exists():
        # don't recompute -- if you need to, delete the serialized version
        return None

    # Load the image using Pillow
    image = photo.get_image_data(use_pillow=True)

    if not image:
        return None

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

    # Create a vector of zeros that will hold our feature vector
    # NOTE(ra): this is a hack until I figure out what's going on: should be torch.zeros(512)
    # not (1, 512, 1, 512), but the vector I'm copying in is the wrong size...
    get_feature_vector = {'conv1': torch.zeros(1, 64, 112, 112),
                          'bn1': torch.zeros(1, 64, 112, 112),
                          'relu': torch.zeros(1, 64, 112, 112),
                          'maxpool': torch.zeros(1, 64, 56, 56),
                          'layer1': torch.zeros(1, 64, 56, 56),
                          'layer2': torch.zeros(1, 128, 28, 28),
                          'layer3': torch.zeros(1, 256, 14, 14),
                          'layer4': torch.zeros(1, 512, 7, 7),
                          'avgpool': torch.zeros(1, 512, 1, 512),
                          'fc': torch.zeros(1, 1000, 1, 1000)}

    feature_vector = get_feature_vector[layer_name]

    # Define a function that will copy the output of a layer
    def copy_data(_module, _input, output):
        feature_vector.copy_(output.data)

    # Attach that function to our selected layer
    hook = layer.register_forward_hook(copy_data)

    # Run the model on our transformed image
    model(image_tensor)

    # Detach our copy function from the layer
    hook.remove()

    # Serialize out the result
    torch.save(feature_vector, out_path)

    return None
