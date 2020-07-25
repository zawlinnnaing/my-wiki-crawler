import os
import json
from collections import OrderedDict


def sort_meta_dict(input_dict: dict) -> OrderedDict:
    """
    Sorting Meta dictionary in result directory.
    @param input_dict:
    @return:
    """
    sorted_tuple = sorted(input_dict.items(), key=lambda item: int(item[0]))
    return OrderedDict(sorted_tuple)


class FileUtil:
    max_storage = 0
    actual_storage = 0

    def __init__(self, max_storage=1000):
        self.max_storage = max_storage

    @staticmethod
    def mkdir_if_not_exists(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    @staticmethod
    def save_to_txt_file(file_name: str, txt_iter: iter, output_dir="results"):
        txt_dir = os.path.join(os.getcwd(), output_dir)
        FileUtil.mkdir_if_not_exists(txt_dir)
        file_path = os.path.join(txt_dir, file_name)
        file_object = open(file_path, 'a')
        for line in txt_iter:
            file_object.write(line)
            file_object.write("\n")
        file_object.close()

    @staticmethod
    def save_meta_dict(data, output_dir="results"):
        meta_path = os.path.join(os.getcwd(), output_dir, 'meta.json')
        with open(meta_path, 'w') as fp:
            json.dump(sort_meta_dict(data), fp, ensure_ascii=False)

    @staticmethod
    def load_meta_dict(output_dir: str = "results") -> dict:
        """
        @param output_dir: Output directory which contains meta
        @return: ordered dictionary by key
        """
        meta_path = os.path.join(os.getcwd(), output_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as fp:
                return sort_meta_dict(json.load(fp))
        else:
            return OrderedDict()

    def add_storage(self, file_path):
        # Convert bytes to mega bytes
        file_size = os.path.getsize(file_path) / 1e+6
        print("file size:", file_size)
        self.actual_storage += file_size

    def check_storage(self):
        print("actual storage", self.actual_storage)
        return self.actual_storage < self.max_storage

    @staticmethod
    def delete_file(file_path: str):
        if os.path.exists(file_path):
            print("{} deleted.".format(file_path))
            os.remove(file_path)
