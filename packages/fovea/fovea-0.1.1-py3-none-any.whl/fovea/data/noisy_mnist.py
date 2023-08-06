import torch
import torchvision
import numpy as np
import os
import math
from PIL import Image


def generate_dataset(
    dataset,
    output_size=64,
    patch_size=8,
    digit_ratio_range=(0.4, 0.6),
    aspect_ratio_range=(1 / 1.5, 1.5),
):

    """
    Args:
        dataset: MNIST dataset
        output_size : size of output images
        patch_size: size of patches for generating noises
        digit_ratio_range: digit_height / output_size
        aspect_ratio_range: digit_width / digit_height
    """
    import cv2

    images = []
    labels = []
    bboxes = []

    # generate dataset
    num_img = len(dataset)
    for i in range(num_img):

        if (i + 1) % 5000 == 0:
            print(f"processed {i+1}/{num_img} images")

        img = np.array(dataset[i][0])
        label = dataset[i][1]

        # random stretching

        digit_ratio = (digit_ratio_range[1] - digit_ratio_range[0]) * np.random.rand(1)[
            0
        ] + digit_ratio_range[0]
        aspect_ratio = (aspect_ratio_range[1] - aspect_ratio_range[0]) * np.random.rand(
            1
        )[0] + aspect_ratio_range[0]
        h = int(output_size * digit_ratio)
        w = min(int(h * aspect_ratio), output_size)
        img_stretch = cv2.resize(img, dsize=(w, h), interpolation=cv2.INTER_CUBIC)

        # generate noise
        noise = np.zeros((output_size, output_size), dtype=np.uint8)
        num_patch = math.ceil(output_size / patch_size)
        for j in range(num_patch * num_patch):

            # randomly sample an image and crop it
            rand_idx = np.random.randint(num_img)
            crop_index = np.random.randint(img.shape[0] - patch_size)
            sample_patch = np.array(dataset[rand_idx][0])[
                crop_index : crop_index + patch_size,
                crop_index : crop_index + patch_size,
            ]

            m = j // num_patch * patch_size
            n = j % num_patch * patch_size
            if (m + patch_size) > output_size:
                sample_patch = sample_patch[: output_size - m, :]
            if (n + patch_size) > output_size:
                sample_patch = sample_patch[:, : output_size - n]
            noise[
                m : min(m + patch_size, output_size),
                n : min(n + patch_size, output_size),
            ] = sample_patch

        # composite the image with noise
        if h == output_size:
            x = 0
        else:
            x = np.random.randint(0, output_size - h)
        if w == output_size:
            y = 0
        else:
            y = np.random.randint(0, output_size - w)

        bbox = [[x, y], [x + h, y + w]]
        img_coposite = noise
        img_coposite[bbox[0][0] : bbox[1][0], bbox[0][1] : bbox[1][1]] = img_stretch

        images.append(img_coposite)
        labels.append(label)
        bboxes.append(bbox)

    return images, labels, bboxes


def _get_file_name(is_train):
    return f'noisy_mnist_{"train" if is_train else "test"}.pt'


def save_dataset(data_root, is_train, save_dir, **configs):
    data_root = os.path.expanduser(data_root)
    raw_dataset = torchvision.datasets.MNIST(
        root=data_root, train=is_train, download=False
    )
    images, labels, bboxes = generate_dataset(raw_dataset, **configs)
    D = {}
    D["images"] = np.array(images, dtype=np.uint8)
    D["labels"] = np.array(labels, dtype=np.long)
    D["bboxes"] = np.array(bboxes, dtype=np.long)
    path = os.path.join(os.path.expanduser(save_dir), _get_file_name(is_train))
    torch.save(D, path)
    print("Saved to", path)


class NoisyMNIST(torchvision.datasets.VisionDataset):
    def __init__(
        self,
        root,
        train=True,
        include_bbox=False,
        transform=None,
        target_transform=None,
    ):
        """
        Args:
            include_bbox: True to have target as (label, bbox)
                False to just have `label` Long tensor as target
        """
        super().__init__(root, transform=transform, target_transform=target_transform)
        self.train = train  # training set or test set
        self.data_file = _get_file_name(train)
        D = torch.load(os.path.join(self.root, self.data_file))
        self.images = D["images"]
        self.labels = D["labels"]
        self.bboxes = D["bboxes"]
        self.include_bbox = include_bbox

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.images[index], int(self.labels[index])
        if self.include_bbox:
            target = (target, self.bboxes[index])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img, mode="L")
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.labels)


if __name__ == "__main__":
    data_root = "/vision/group/small"
    save_dataset(data_root, True, f"{data_root}")
    save_dataset(data_root, False, f"{data_root}")
