import torch
from torch.utils.data import Dataset
from typing import Any, NoReturn, Optional, Generator, List, Tuple, Callable
import numpy as np
import os
from pathlib import Path
import random

def convert_pytorch_model_to_onnx(model: Any, sample_input_data: Any, path: Optional[str] = './model.onnx') -> NoReturn:
    torch.onnx.export(model, sample_input_data, path, output_names=['output'], input_names=['input'])


def get_data_from_numpy_files(folder: str, index: int, n_x: int) -> Tuple[np.ndarray]:
    result = tuple()
    corrected_folder = os.sep.join(folder.split('/')[:-1])

    second_num = str(index)
    for i in range(n_x):

        p = os.path.join(corrected_folder, 'x{}_{}.npy'.format(i, second_num))

        data = np.load(p)

        result += (data,)

    return result


def extract_num_from_filename(name: str) -> int:
    first = name.split('.np')[0]
    if not first or first == '':
        return 0
    second = first.split('_')[-1]
    if not second or second == '':
        return 0

    return int(second)


def calc_num_x(folder: str) -> int:
    files = os.listdir(folder)

    filtered_files = [f for f in files if '.np' in f]

    n = 3

    if len(filtered_files) == 0:
        raise ValueError('No files found downloaded!')

    while n > len(filtered_files):
        n = n - 1

    samples = [extract_num_from_filename(f) for f in random.sample(filtered_files, n)]
    n_x = -1
    for sample in samples:
        subset = [f for f in filtered_files if '_{}.np'.format(sample) in f]

        if n_x == -1:
            n_x = len(subset)
        elif n_x != len(subset):
            raise ValueError('Inconsistent number of data inputs!')

    return n_x


class ForefrontDataset(Dataset):
    num_folders: int
    data_dir: str
    dirs: List[str]
    transform: Callable
    n_x: int
    def __init__(self, transform: Callable = None):
        super(ForefrontDataset, self).__init__()

        self.data_dir = os.path.join(Path.home(), '.forefront', 'data')

        dirs = os.listdir(self.data_dir)

        filtered_dirs = [os.path.join(self.data_dir, d) for d in dirs if 'npy' in d or 'npz' in d]

        self.n_x = calc_num_x(self.data_dir)
        self.num_folders = len(filtered_dirs) // self.n_x
        self.dirs = filtered_dirs
        self.transform = transform


    def __len__(self):
        return self.num_folders

    def __getitem__(self, index):
        folder = self.dirs[index]

        data = get_data_from_numpy_files(folder, index, self.n_x)

        if self.transform is not None:
            data = self.transform(data)

        return data
