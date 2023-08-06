"""
200 classes, each 500 training images, 100 validation images
"""
import os
import random
from tqdm import tqdm


def create_mini_imagenet(
    imagenet_folder,
    dest_folder,
    num_classes: int,
    training_images_per_class: int,
    seed: int = 1,
    dry_run: bool = False,
):
    """
    Assume that `imagenet_folder` has train/ and val/ subdirs
    """
    if dry_run:
        run = print
    else:
        run = os.system

    random.seed(seed)
    imagenet_folder = os.path.expanduser(imagenet_folder)
    dest_folder = os.path.expanduser(dest_folder)
    # subsample classes
    all_classes = [
        d for d in os.listdir(f"{imagenet_folder}/train") if d.startswith("n")
    ]
    print("ImageNet classes:", len(all_classes))

    classes = random.sample(all_classes, num_classes)

    for cls in tqdm(classes):
        imgs = [
            im
            for im in os.listdir(f"{imagenet_folder}/train/{cls}")
            if im.endswith(".JPEG")
        ]
        imgs = random.sample(imgs, training_images_per_class)
        run(f"mkdir -p {dest_folder}/train/{cls}")
        for im in imgs:
            run(f"cp {imagenet_folder}/train/{cls}/{im} {dest_folder}/train/{cls}/{im}")

    run(f"mkdir -p {dest_folder}/val/")
    for cls in classes:
        run(f"cp -rf {imagenet_folder}/val/{cls} {dest_folder}/val")
