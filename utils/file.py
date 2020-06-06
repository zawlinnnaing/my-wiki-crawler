import os
import json
from collections import OrderedDict


class FileUtil:
    max_storage = 0
    actual_storage = 0

    def __init__(self, max_storage=1000):
        self.max_storage = max_storage

    @staticmethod
    def mkdir_if_not_exists(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def save_to_txt_file(self, file_name, txt_iter: iter, output_dir="results"):
        txt_dir = os.path.join(os.getcwd(), output_dir)
        FileUtil.mkdir_if_not_exists(txt_dir)
        file_path = os.path.join(txt_dir, file_name)
        file_object = open(file_path, 'a')
        for line in txt_iter:
            file_object.write(line)
            file_object.write("\n")
        file_object.close()
        self.add_storage(file_path)

    @staticmethod
    def save_meta_dict(self, data, output_dir="results"):
        meta_path = os.path.join(os.getcwd(), output_dir, 'meta.json')
        with open(meta_path, 'w') as fp:
            json.dump(data, fp, sort_keys=True)

    @staticmethod
    def load_meta_dict(output_dir: str = "results") -> dict:
        meta_path = os.path.join(os.getcwd(), output_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as fp:
                return OrderedDict(sorted(json.load(fp).items()))
        else:
            return OrderedDict()

    def add_storage(self, file_path):
        # Convert bytes to mega bytes
        file_size = os.path.getsize(file_path) / 1000
        self.actual_storage += file_size

    def check_storage(self):
        return self.actual_storage < self.max_storage

    @staticmethod
    def delete_file(file_path: str):
        if os.path.exists(file_path):
            print("{} deleted.".format(file_path))
            os.remove(file_path)
